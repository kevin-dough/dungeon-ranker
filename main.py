#importing libraries for webpage, api, data files, and more math operations
from flask import Flask, redirect, url_for, render_template, request
import aboutdata, featuredstats, requests, math, methods

app = Flask(__name__)

#Mojang API and SkyCrypt API were used in the making of this project.

#route for homepage
@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        username = request.form.get('username')
        print("LOG > form received")
        message = ""
        try:
            lastprofile = methods.lastprofile_cutename(username)
            url = "/stats/" + username + "/" + lastprofile
            print("LOG > loading url")
            return redirect(url)
        except:
            message = "no skyblock profiles"
        return render_template("index.html", featuredata=featuredstats.featuredata())
    return render_template("index.html", featuredata=featuredstats.featuredata())


@app.route('/stats/<username>/<profile>', methods=['GET', 'POST'])
def stats(username, profile):

    #Mojang API https://api.mojang.com
    mcdata = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
    uuid = mcdata["id"]
    formattedusername = mcdata["name"]

    #SkyCrypt API https://sky.shiiyu.moe/api/v2/
    skycryptprofile = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()

    print("LOG > API set")

    #guild info
    profiles = skycryptprofile["profiles"]
    firstprofile = list(profiles.keys())[0]

    try:
        name = profiles[firstprofile]["data"]["guild"]["name"]
        tag = profiles[firstprofile]["data"]["guild"]["tag"]
        level = profiles[firstprofile]["data"]["guild"]["level"]
        rank = profiles[firstprofile]["data"]["guild"]["rank"]
        members = profiles[firstprofile]["data"]["guild"]["members"]
        exist = "block"
    except:
        name = "N/A"
        tag = "N/A"
        level = "N/A"
        rank = "N/A"
        members = "N/A"
        exist = "none"

    guild = {"name": name, "tag": tag, "level": level, "rank": rank, "members": members, "exist": exist}

    print("LOG > guild info loaded")

    #profiles list
    profilelist=[]

    for i in profiles.keys():
        # print(profiles[i]["cute_name"])
        profilelist.append(profiles[i]["cute_name"])

    skycryptdungeons = requests.get(f"https://sky.shiiyu.moe/api/v2/dungeons/{username}/{profile}").json()
    try:
        catalvl = skycryptdungeons["dungeons"]["catacombs"]["level"]["level"]
    except:
        catalvl = 0

    try:
        secrets = skycryptdungeons["dungeons"]["secrets_found"]
    except:
        secrets = 0

    class_weight = {}
    weights = skycryptprofile["profiles"][methods.lastprofile_id(username)]["data"]["weight"]["senither"]["dungeon"]
    total_weight = round((weights["total"]), 2)
    catacombs_weight = round((weights["dungeons"]["catacombs"]["weight"]), 2)
    catacombs_weight_of = round((weights["dungeons"]["catacombs"]["weight_overflow"]), 2)

    for i in weights["classes"]:
        class_weight["{}_weight".format(i)] = round((weights["classes"][i]["weight"]), 2)
        class_weight["{}_weight_of".format(i)] = round((weights["classes"][i]["weight_overflow"]), 2)

    #lists to fill out
    floors = [1, 2, 3, 4, 5, 6, 7]
    mins = []
    secs = []
    completions = []

    #procedure to find fastest time and completions for each floor
    def floordata(n, timeoption, catatype):
        fvm = ""
        if catatype=="f":
            fvm = "catacombs"
        if catatype=="m":
            fvm = "master_catacombs"

        if timeoption=="s+":
            try:
                ftime = (skycryptdungeons["dungeons"][fvm]["floors"][f"{n}"]["stats"]["fastest_time_s_plus"])/1000
                fmin = math.floor(ftime/60)
                fsec = math.ceil(ftime - 60*fmin)
                mins.append(fmin)
                secs.append(fsec)
            except:
                mins.append("?")
                secs.append("?")
        elif timeoption=="s":
            try:
                ftime = (skycryptdungeons["dungeons"][fvm]["floors"][f"{n}"]["stats"]["fastest_time_s"])/1000
                fmin = math.floor(ftime/60)
                fsec = math.ceil(ftime - 60*fmin)
                mins.append(fmin)
                secs.append(fsec)
            except:
                mins.append("?")
                secs.append("?")

    print("LOG > floordata loaded")

    def floorcompletions(n, catatype):
        fvm = ""
        if catatype=="f":
            fvm = "catacombs"
        if catatype=="m":
            fvm = "master_catacombs"

        try:
            fcompletions = skycryptdungeons["dungeons"][fvm]["floors"][f"{n}"]["stats"]["tier_completions"]
            completions.append(fcompletions)
        except:
            completions.append("N/A")

    for n in floors:
        floordata(n, 's', 'f')
    for n in floors:
        floordata(n, 's+', 'f')
    for n in floors:
        floordata(n, 's', 'm')
    for n in floors:
        floordata(n, 's+', 'm')
    for n in floors:
        floorcompletions(n, 'f')
    for n in floors:
        floorcompletions(n, 'm')

    print("LOG > floorcompletions loaded")

    #procedure to calculate score to give to user based on catacombs level and secrets
    def calculate_score(catalvl, secrets):
        global catalvlscore, secretsscore, bonus, total

        if catalvl>=38:
            temp2 = catalvl-38
            catabonus = math.floor((temp2))
            catalvlscore = 150
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

    print("LOG > score calculated")

    # print(mins)
    # print(secs)
    print("LOG > data being sent")
    #sending all the variables to the webpage
    return render_template(
        "stats.html",
        username=formattedusername,
        profile=profile,
        uuid=uuid,

        guild=guild,
        profilelist=profilelist,

        catalvl=catalvl, secrets=secrets, total_weight=total_weight,
        catacombs_weight=catacombs_weight, catacombs_weight_of=catacombs_weight_of, class_weight=class_weight,
        secretsscore = secretsscore, bonus=bonus, catalvlscore=catalvlscore, total=total,
        scoreimage=getscoreimage(total),
        sf1min=mins[0], sf1sec=secs[0], spf1min=mins[7], spf1sec=secs[7],
        sf2min=mins[1], sf2sec=secs[1], spf2min=mins[8], spf2sec=secs[8],
        sf3min=mins[2], sf3sec=secs[2], spf3min=mins[9], spf3sec=secs[9],
        sf4min=mins[3], sf4sec=secs[3], spf4min=mins[10], spf4sec=secs[10],
        sf5min=mins[4], sf5sec=secs[4], spf5min=mins[11], spf5sec=secs[11],
        sf6min=mins[5], sf6sec=secs[5], spf6min=mins[12], spf6sec=secs[12],
        sf7min=mins[6], sf7sec=secs[6], spf7min=mins[13], spf7sec=secs[13],

        sm1min=mins[14], sm1sec=secs[14], spm1min=mins[21], spm1sec=secs[21],
        sm2min=mins[15], sm2sec=secs[15], spm2min=mins[22], spm2sec=secs[22],
        sm3min=mins[16], sm3sec=secs[16], spm3min=mins[23], spm3sec=secs[23],
        sm4min=mins[17], sm4sec=secs[17], spm4min=mins[24], smf4sec=secs[24],
        sm5min=mins[18], sm5sec=secs[18], spm5min=mins[25], smf5sec=secs[25],
        sm6min=mins[19], sm6sec=secs[19], spm6min=mins[26], smf6sec=secs[26],
        sm7min=mins[20], sm7sec=secs[20], spm7min=mins[27], smf7sec=secs[27],

        f1completions=completions[0], m1completions=completions[7],
        f2completions=completions[1], m2completions=completions[8],
        f3completions=completions[2], m3completions=completions[9],
        f4completions=completions[3], m4completions=completions[10],
        f5completions=completions[4], m5completions=completions[11],
        f6completions=completions[5], m6completions=completions[12],
        f7completions=completions[6], m7completions=completions[13]
    )

@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/about")
def about():
    #uses lists and definitions from aboutdata.py file to display data on webpage
    return render_template("about.html", groupdatalist=aboutdata.groupdata())

@app.route('/essence', methods=['GET', 'POST'])
def essence():
    if request.method=='POST':
        username = request.form.get('username')
        print("LOG > form received")
        try:
            skycryptprofiledata = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
            profiles = skycryptprofiledata["profiles"]
            lastprofile = methods.lastprofile_id(username)
        except:
            message = "no skyblock profiles"
            return render_template("essence.html", message=message)

        message = undead = wither = dragon = spider = ice = gold = diamond = ""
        try:
            undead = profiles[lastprofile]["raw"]["essence_undead"]
            wither = profiles[lastprofile]["raw"]["essence_wither"]
            dragon = profiles[lastprofile]["raw"]["essence_dragon"]
            spider = profiles[lastprofile]["raw"]["essence_spider"]
            ice = profiles[lastprofile]["raw"]["essence_ice"]
            gold = profiles[lastprofile]["raw"]["essence_gold"]
            diamond = profiles[lastprofile]["raw"]["essence_diamond"]
        except:
            message = "turn on inv api or something"

        return render_template("essence.html",
                               undead=undead,
                               wither=wither,
                               dragon=dragon,
                               spider=spider,
                               ice=ice,
                               gold=gold,
                               diamond=diamond,
                               message=message)

    return render_template("essence.html")


if __name__ == "__main__":
    app.run(debug=True)