import requests

def lastprofile_cutename(username):
    skycryptprofiledata = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
    profiles = skycryptprofiledata["profiles"]
    lastprofile = ""
    lastsave = 0
    for i in profiles.keys():
        if (profiles[i]["last_save"] > lastsave):
            lastsave = profiles[i]["last_save"]
            lastprofile = profiles[i]["cute_name"]
    return lastprofile

def lastprofile_id(username):
    skycryptprofiledata = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
    profiles = skycryptprofiledata["profiles"]
    lastprofile = ""
    lastsave = 0
    for i in profiles.keys():
        if (profiles[i]["last_save"] > lastsave):
            lastsave = profiles[i]["last_save"]
            lastprofile = profiles[i]["profile_id"]
    return lastprofile