
#this is data that will be used in the about page which will be displayed with a jinja loop

def person1():
    name = "person1"
    color = "#ff458a"
    firstname = "person"
    ign = "CrazyUdon"
    social1 = "https://github.com/"
    social2 = "https://www.instagram.com/"
    info = {"name": name, "color": color, "firstname": firstname, "ign": ign, "social1": social1, "social2": social2}
    return info

def person2():
    name = "person2"
    color = "#1bc725"
    firstname = "person"
    ign = "sea7wa"
    social1 = "https://github.com/"
    social2 = "https://www.instagram.com/"
    info = {"name": name, "color": color, "firstname": firstname, "ign": ign, "social1": social1, "social2": social2}
    return info

def groupdata():
    return [person1(), person2()]