import json


f = open("result.json")
data = json.load(f)
print(data["2099"])