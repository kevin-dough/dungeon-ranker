#importing libraries for webpage, api, data files, and more math operations
from flask import Flask, redirect, url_for, render_template, request
import aboutdata, requests, math

app = Flask(__name__)

#Mojang API and SkyCrypt API were used in the making of this project.


#route for homepage
@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    #get form data on "help!" page where user can find the name of their profile by inputting their username
    if request.method=='POST':
        username = request.form.get('username')
        skycryptprofiledata = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
        profiles = skycryptprofiledata["profiles"]
        #creates a list of their profiles based on API data
        profilelist = []
        for i in profiles.keys():
            print(profiles[i]["cute_name"])
            profilelist.append(profiles[i]["cute_name"])
        print(profilelist)
        #formats profilelist to display on webpage
        profilelistlength = len(profilelist)
        profilelisttemp = ""
        for b in range(profilelistlength):
            if b == profilelistlength-1:
                profilelisttemp = profilelisttemp + profilelist[b]
            else:
                profilelisttemp = profilelisttemp + profilelist[b] + ", "
        profilelistformatted = "Profiles: " + profilelisttemp
        return render_template("index.html", profiles=profilelistformatted)
    return render_template("index.html")


@app.route('/stats/<username>/<profile>', methods=['GET', 'POST'])
def stats(username, profile):
        fastesttime = "splus" #add a switch

        #Mojang API https://api.mojang.com
        mcdata = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
        uuid = mcdata["id"]
        formattedusername = mcdata["name"]

        #SkyCrypt API https://sky.shiiyu.moe/api/v2/
        skycryptprofile = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()

        #guild info
        profiles = skycryptprofile["profiles"]
        firstprofile = list(profiles.keys())[0]

        name = profiles[firstprofile]["data"]["guild"]["name"]
        tag = profiles[firstprofile]["data"]["guild"]["tag"]
        level = profiles[firstprofile]["data"]["guild"]["level"]
        rank = profiles[firstprofile]["data"]["guild"]["rank"]
        members = profiles[firstprofile]["data"]["guild"]["members"]
        guild = {"name": name, "tag": tag, "level": level, "rank": rank, "members": members}

        skycryptdungeons = requests.get(f"https://sky.shiiyu.moe/api/v2/dungeons/{username}/{profile}").json()
        catalvl = skycryptdungeons["dungeons"]["catacombs"]["level"]["level"]
        secrets = skycryptdungeons["dungeons"]["secrets_found"]
        #try to find dungeon weight through api; if unable to find set variable weight to N/A
        try:
            weight = round((skycryptdungeons["dungeons"]["dungeonsWeight"]), 2)
        except:
            weight = "N/A"

        #lists to fill out
        floors = [1, 2, 3, 4, 5, 6, 7]
        mins = []
        secs = []
        completions = []

        #procedure to find fastest time and completions for each floor
        def floordata(n, timeoption):
            if timeoption=="s+":
                try:
                    ftime = (skycryptdungeons["dungeons"]["catacombs"]["floors"][f"{n}"]["stats"]["fastest_time_s_plus"])/1000
                    fmin = math.floor(ftime/60)
                    fsec = math.ceil(ftime - 60*fmin)
                    mins.append(fmin)
                    secs.append(fsec)
                except:
                    mins.append("?")
                    secs.append("?")
            elif timeoption=="s":
                try:
                    ftime = (skycryptdungeons["dungeons"]["catacombs"]["floors"][f"{n}"]["stats"]["fastest_time_s"])/1000
                    fmin = math.floor(ftime/60)
                    fsec = math.ceil(ftime - 60*fmin)
                    mins.append(fmin)
                    secs.append(fsec)
                except:
                    mins.append("?")
                    secs.append("?")

            try:
                fcompletions = skycryptdungeons["dungeons"]["catacombs"]["floors"][f"{n}"]["stats"]["tier_completions"]
                completions.append(fcompletions)
            except:
                completions.append("N/A")

            print(mins)
            print(secs)
            print(completions)

        #user can choose between s+ and s, which will be used to determine fastest time for s/s+
        if fastesttime=="splus":
            for n in floors:
                floordata(n, 's+')
        elif fastesttime=="s":
            for n in floors:
                floordata(n, 's')




        #procedure to calculate score to give to user based on catacombs level and secrets
        def calculate_score(catalvl, secrets):
            global catalvlscore, secretsscore, bonus, total

            if catalvl>=38:
                temp2 = catalvl-38
                catabonus = math.floor((temp2))
            else:
                catalvlscore = math.floor((catalvl/38)*150)
                catabonus = 0

            if secrets>=12000:
                temp = secrets-12000
                secretsscore = 150
                secretbonus = math.floor(temp/5000)
            else:
                secretsscore = math.floor((secrets/12000)*150)
                secretbonus = 0

            bonus = catabonus + secretbonus
            total = catalvlscore + secretsscore + bonus

            return catalvlscore, secretsscore, bonus, total

        #procedure to select a certain image based on the score the user recieves
        def getscoreimage(total):
            global scoreimage
            scoreimage = "s+"
            if total <= 99:
                scoreimage = "d"
            elif total in range(100, 160):
                scoreimage = "c"
            elif total in range(160, 230):
                scoreimage = "b"
            elif total in range(230, 270):
                scoreimage = "a"
            elif total in range(270, 300):
                scoreimage = "s"
            elif total >= 300:
                scoreimage = "s+"
            return scoreimage

        calculate_score(catalvl, secrets)
        #sending all the variables to the webpage
        return render_template(
            "stats.html",
            username=formattedusername,
            profile=profile,
            uuid=uuid,

            guild=guild,

            catalvl=catalvl, secrets=secrets, weight=weight,
            secretsscore = secretsscore, bonus=bonus, catalvlscore=catalvlscore, total=total,
            scoreimage=getscoreimage(total),
            f1min=mins[0], f1sec=secs[0], f1completions=completions[0],
            f2min=mins[1], f2sec=secs[1], f2completions=completions[1],
            f3min=mins[2], f3sec=secs[2], f3completions=completions[2],
            f4min=mins[3], f4sec=secs[3], f4completions=completions[3],
            f5min=mins[4], f5sec=secs[4], f5completions=completions[4],
            f6min=mins[5], f6sec=secs[5], f6completions=completions[5],
            f7min=mins[6], f7sec=secs[6], f7completions=completions[6],

        )

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/about")
def about():
    #uses lists and definitions from aboutdata.py file to display data on webpage
    return render_template("about.html", groupdatalist=aboutdata.groupdata())


if __name__ == "__main__":
    app.run(debug=True)