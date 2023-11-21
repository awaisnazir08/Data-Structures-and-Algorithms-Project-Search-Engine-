import json

with open("./nela-gt-2022/newsdata/21stcenturywire.json", "r") as f:
    data = json.load(f)
print(len(data))

# for d in data:
#     print(d.get("id"))
    # del d['author']
    # print(f"{d['url']}\n\n")
    # print("\n\n")