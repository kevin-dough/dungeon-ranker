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


        f1time = (skycryptdata["dungeons"]["catacombs"]["floors"]["1"]["stats"]["fastest_time_s_plus"])/1000
        f1min = math.floor(f1time/60)
        f1sec = math.ceil(f1time - 60*f1min)

        f2time = (skycryptdata["dungeons"]["catacombs"]["floors"]["2"]["stats"]["fastest_time_s_plus"])/1000
        f2min = math.floor(f2time/60)
        f2sec = math.ceil(f2time - 60*f2min)

        f3time = (skycryptdata["dungeons"]["catacombs"]["floors"]["3"]["stats"]["fastest_time_s_plus"])/1000
        f3min = math.floor(f3time/60)
        f3sec = math.ceil(f3time - 60*f3min)

        f4time = (skycryptdata["dungeons"]["catacombs"]["floors"]["4"]["stats"]["fastest_time_s_plus"])/1000
        f4min = math.floor(f4time/60)
        f4sec = math.ceil(f4time - 60*f4min)

        f5time = (skycryptdata["dungeons"]["catacombs"]["floors"]["5"]["stats"]["fastest_time_s_plus"])/1000
        f5min = math.floor(f5time/60)
        f5sec = math.ceil(f5time - 60*f5min)

        f6time = (skycryptdata["dungeons"]["catacombs"]["floors"]["6"]["stats"]["fastest_time_s_plus"])/1000
        f6min = math.floor(f6time/60)
        f6sec = math.ceil(f6time - 60*f6min)

        f7time = (skycryptdata["dungeons"]["catacombs"]["floors"]["7"]["stats"]["fastest_time_s_plus"])/1000
        f7min = math.floor(f7time/60)
        f7sec = math.ceil(f7time - 60*f7min)


        f1completions = skycryptdata["dungeons"]["catacombs"]["floors"]["1"]["stats"]["tier_completions"]
        f2completions = skycryptdata["dungeons"]["catacombs"]["floors"]["2"]["stats"]["tier_completions"]
        f3completions = skycryptdata["dungeons"]["catacombs"]["floors"]["3"]["stats"]["tier_completions"]
        f4completions = skycryptdata["dungeons"]["catacombs"]["floors"]["4"]["stats"]["tier_completions"]
        f5completions = skycryptdata["dungeons"]["catacombs"]["floors"]["5"]["stats"]["tier_completions"]
        f6completions = skycryptdata["dungeons"]["catacombs"]["floors"]["7"]["stats"]["tier_completions"]
        f7completions = skycryptdata["dungeons"]["catacombs"]["floors"]["6"]["stats"]["tier_completions"]
        return render_template(
            "index.html",
            username=username,
            profilename=profilename,
            uuid=uuid,
            catalvl=catalvl,
            secrets=secrets,
            weight=weight,

            f1min=f1min,
            f1sec=f1sec,
            f1completions=f1completions,

            f2min=f2min,
            f2sec=f2sec,
            f2completions=f2completions,

            f3min=f3min,
            f3sec=f3sec,
            f3completions=f3completions,

            f4min=f4min,
            f4sec=f4sec,
            f4completions=f4completions,

            f5min=f5min,
            f5sec=f5sec,
            f5completions=f5completions,

            f6min=f6min,
            f6sec=f6sec,
            f6completions=f6completions,

            f7min=f7min,
            f7sec=f7sec,
            f7completions=f7completions
        )
    return render_template("index.html", username=username, profilename=profilename, uuid=uuid)

def showData():
    print("Hi i am " + username)
    #put a buncha stuff there cuz yea and store all the values from the json data in variables here

@app.route("/about")
def about():
    return render_template("about.html", groupdatalist=aboutdata.groupdata())

@app.route("/testapi")
def testapi():
    return render_template("testapi.html")

if __name__ == "__main__":
    app.run(debug=True)