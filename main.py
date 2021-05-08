from flask import Flask, redirect, url_for, render_template, request
import aboutdata, requests

app = Flask(__name__)



@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])


def home():
    global username, profilename
    username = "username"
    profilename = "profile"
    if request.method=='POST':
        username = request.form.get('username')
        profilename = request.form.get('cute_name')
        print(username)
        print(profilename)
        data = requests.get(f"https://sky.shiiyu.moe/api/v2/dungeons/{username}/{profilename}").json()
        print(data)
        showData()
        return render_template("index.html", username=username, profilename=profilename)
    return render_template("index.html", username=username, profilename=profilename)

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