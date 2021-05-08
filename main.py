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
    if request.method=='POST':
        username = request.form.get('username')
        profilename = request.form.get('cute_name')
        print(username)
        print(profilename)
        mcdata = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
        #print(mcdata)
        uuid = mcdata["id"]
        skycryptdata = requests.get(f"https://sky.shiiyu.moe/api/v2/dungeons/{username}/{profilename}").json()
        #print(skycryptdata)
        showData()

        catalvl = skycryptdata["dungeons"]["catacombs"]["level"]["level"]
        secrets = skycryptdata["dungeons"]["secrets_found"]
        weight = round((skycryptdata["dungeons"]["dungeonsWeight"]), 2)
        floors = [1, 2, 3, 4, 5, 6, 7]
        mins = []
        secs = []
        completions = []
        for n in floors:
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



        return render_template(
            "index.html",
            username=username,
            profilename=profilename,
            uuid=uuid,
            catalvl=catalvl,
            secrets=secrets,
            weight=weight,


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
    return render_template("index.html", username=username, profilename=profilename, uuid=uuid)

def showData():
    print("Hi i am " + username)
    uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
    #put a buncha stuff there cuz yea and store all the values from the json data in variables here

@app.route("/about")
def about():
    return render_template("about.html", groupdatalist=aboutdata.groupdata())

@app.route("/testapi")
def testapi():
    return render_template("testapi.html")

if __name__ == "__main__":
    app.run(debug=True)