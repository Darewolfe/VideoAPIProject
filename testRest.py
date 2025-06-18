import requests

BASE = "http://127.0.0.1:5000/"

# data = [{"likes": 70, "name": "John", "views": 1000},
#         {"likes": 1000, "name": "Ashley", "views": 50000},
#         {"likes": 500, "name": "Michael", "views": 30000}]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())

# input()
# response = requests.get(BASE + "video/0")
# print(response.json())
response = requests.patch(BASE + "video/2", {"views": 10000})
print(response.json())