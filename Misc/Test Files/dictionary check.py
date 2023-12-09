import json

inverted_index = "Inverted_Index/inverted_index.json"

with open (inverted_index, 'r') as file:
    data = json.load(file)

    if "10172" in data["word_ID"]:
        print("yes")
    # for word_id in data["word_ID"]:
    #     print(word_id)
    # # i = 1
    # for dat in data:
    #     print(dat)
    #     # if i==1:
    #     #     break

# from collections import defaultdict

# hello = defaultdict(list)
# print(hello)
# hello["orange"].append({87})
# print(hello)


# # import json
# # with open("Lexicon.json", 'r') as file:
# #     data = json.load(file)

# # # h = 405
# # if "youtube" in data:
# #     print("yes")
# # else:
# #     print("no")
# h = 6
# h = str(h)
# print(type(h))

# i = 1
# for key in data:
#     value = data[key]
#     print(f"Key: {key}, Value: {value}")
#     if i ==1:
#         break