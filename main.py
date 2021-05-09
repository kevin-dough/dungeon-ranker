from flask import Flask, redirect, url_for, render_template, request
import aboutdata, requests, math

app = Flask(__name__)



@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    global username, profilename
    username = "username"
    profilename = "profile"
    uuid = "52c66d0a-ad76-42df-aa23-0d9cb75832ea"
    scoreimage = "s+"
    if request.method=='POST':
        username = request.form.get('username')
        profilename = request.form.get('cute_name')
        mcdata = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
        uuid = mcdata["id"]
        skycryptdata = requests.get(f"https://sky.shiiyu.moe/api/v2/dungeons/{username}/{profilename}").json()
        skycryptprofiledata = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
        formattedusername = mcdata["name"]
        catalvl = skycryptdata["dungeons"]["catacombs"]["level"]["level"]
        secrets = skycryptdata["dungeons"]["secrets_found"]
        try:
            weight = round((skycryptdata["dungeons"]["dungeonsWeight"]), 2)
        except:
            weight = "N/A"


        floors = [1, 2, 3, 4, 5, 6, 7]
        mins = []
        secs = []
        completions = []

        def floordata(n):
            try:
                ftime = (skycryptdata["dungeons"]["catacombs"]["floors"][f"{n}"]["stats"]["fastest_time_s_plus"])/1000
                fmin = math.floor(ftime/60)
                fsec = math.ceil(ftime - 60*fmin)
                mins.append(fmin)
                secs.append(fsec)
            except:
                mins.append("?")
                secs.append("?")

            try:
                fcompletions = skycryptdata["dungeons"]["catacombs"]["floors"][f"{n}"]["stats"]["tier_completions"]
                completions.append(fcompletions)
            except:
                completions.append("N/A")

        for n in floors:
            floordata(n)




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

        return render_template(
            "index.html",
            username=formattedusername,
            profilename=profilename,
            uuid=uuid,
            catalvl=catalvl,
            secrets=secrets,
            weight=weight,

            secretsscore = secretsscore,
            bonus=bonus,
            catalvlscore=catalvlscore,
            total=total,
            scoreimage=getscoreimage(total),

            f1min=mins[0],
            f1sec=secs[0],
            f1completions=completions[0],

            f2min=mins[1],
            f2sec=secs[1],
            f2completions=completions[1],

            f3min=mins[2],
            f3sec=secs[2],
            f3completions=completions[2],

            f4min=mins[3],
            f4sec=secs[3],
            f4completions=completions[3],

            f5min=mins[4],
            f5sec=secs[4],
            f5completions=completions[4],

            f6min=mins[5],
            f6sec=secs[5],
            f6completions=completions[5],

            f7min=mins[6],
            f7sec=secs[6],
            f7completions=completions[6],

        )
    return render_template("index.html", username=username, profilename=profilename, uuid=uuid, scoreimage=scoreimage)

@app.route("/help", methods=['GET', 'POST'])
def help():
    if request.method=='POST':
        username = request.form.get('username')
        skycryptprofiledata = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
        profiles = skycryptprofiledata["profiles"]
        profilelist = []
        for i in profiles.keys():
            print(profiles[i]["cute_name"])
            profilelist.append(profiles[i]["cute_name"])
        print(profilelist)
        profilelistlength = len(profilelist)
        profilelistformatted = ""
        for b in range(profilelistlength):
            profilelistformatted = profilelistformatted + profilelist[b] + " "
        return render_template("help.html", profiles=profilelistformatted)
    return render_template("help.html")

@app.route("/about")
def about():
    return render_template("about.html", groupdatalist=aboutdata.groupdata())

@app.route('/testapi', methods=['GET', 'POST'])
def testapi():
    if request.method=='POST':
        usernamee = request.form.get('username')
        mcdata = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{usernamee}").json()

        formattedusername1 = mcdata["name"]
        skycryptprofiledata = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{usernamee}").json()
        profile_id = skycryptprofiledata["profiles"]["profile_id"]
        cute_name = skycryptprofiledata["profiles"][f"{profile_id}"]["cute_name"]
        print(cute_name)
        return render_template("testapi.html", username=formattedusername1)
    return render_template("testapi.html")

if __name__ == "__main__":
    app.run(debug=True)