import json

a = "data/lang.json"
# change if you need to move it or rename it

with open(a, 'r', encoding="utf8") as j:
    p = json.load(j)
# connect to the json file
