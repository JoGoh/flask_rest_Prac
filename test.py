import requests

BASE = "http://127.0.0.1:5000/"

#kinda like instantiating it
# response = requests.put(BASE + "video/3", {"likes":10, "name": "Me", "views": 100000})
# print(response.json())
# input() #get input to "pause it"
# response = requests.get(BASE + "video/3")
# print(response.json())
# input() #get input to "pause it"

#update id 3
response = requests.patch(BASE + "video/3", {"likes":10000, "name": "Me", "views": 100000})
print(response.json())
input() #get input to "pause it"
response = requests.get(BASE + "video/3")
print(response.json())
input() #get input to "pause it"

response = requests.patch(BASE + "video/2", {})
print(response.json())

##################
# put and delete
##################
# data = [{"likes":10000, "name": "Me1", "views": 100000},
#         {"likes":20000, "name": "Me2", "views": 100000},
#         {"likes":30000, "name": "Me3", "views": 100000}]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), {"likes":10, "name": "Me", "views": 100000})
#     print(response.json())

# input()

# response = requests.delete(BASE + "video/0")
# print(response) #defined in main, no json return syntax