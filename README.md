<h1 align="center">Hypixel Player Status Checker</h1>

<div align="center">
  <img src="/static/images/banner.jpg">
  <p align="center">
	  <b>Receive a rank based on your dungeons stats!</b> <br>
	  <sub>Special thanks to Kian Kishimoto for helping with the first version of this project.</sub>
  </p>
</div>

## Features

### Viewing Stats
Type your username or someone else's username into this search bar.

<img src="/static/images/search_box.png">

Your last played profile will be used. Below the search bar are contributors and special people.

When your stats load, they will look something like this.

<img src="/static/images/sample_stats.png">

The left box shows catacombs level, secrets count, dungeons Senither weight, floor completions, and best times for each floor.

To switch between S and S+ and also between catacombs and master mode catacombs, you can use the two sliders above the right box.

<img src="/static/images/switching_modes.png">

### Calculating the Score
The score given is on the right box in the stats page.

The `secrets` and the `catacombs level` scores are both out of `150`. To get a full score in each section, `12,000 secrets` and `catacombs 38` are needed. Every catacombs level over `catacombs 38` will be awarded `1` bonus point. Every `5,000` secrets over `12,000 secrets` will be awarded 1 bonus point.

### Checking Essence
Locate `essence` on the navigation bar.

Use this search bar to view how much of each essence a certain player has. Inventory API must be on.

<img src="/static/images/essence.png">

## Technologies Used

This project uses the `Mojang API` to convert usernames to UUIDs and also format usernames (capitalized letters).

For the Hypixel Skyblock stats, the project uses the `SkyCrypt API`.

## Key Code Snippets

### Last Profile `cute_name` and `profile_id`

These two methods will return either the `cute_name` of the player's last played profile or their `profile_id`. The only paramater is the player's username. The `cute_name` is the fruit associated with the profile. For example, Apple or Orange or Pear.

```python
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
```
