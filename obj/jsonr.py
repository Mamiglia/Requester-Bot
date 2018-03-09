import json

a = "data/lang.json"

with open(a, 'r', encoding="utf8") as j:
    p = json.load(j)
