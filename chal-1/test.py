import requests
import secrets
BASE = "http://127.0.0.1:5000/"

#an array of jsons for creation of multiple tags via post if wanted
linux_data = {"name": "linux",
        "contents": "I'd just like to interject for a moment. What you're referring to as Linux is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux..."}

print("\nMaking post request(s)...")
post_url = BASE + "tags/linux"
print("Calling POST", post_url)
response = requests.post(post_url, linux_data) #first tag is linux
print(response.json())
# for i in range(len(data)):
#     #generate token for each data
#     post_url = BASE + "tags/" + data[i]["name"]
#     print("Calling POST", post_url)
#     response = requests.post(post_url, data[i]) #first tag is linux
#     print(response.json())

print("\nMake a get request for the linux tag...")
get_url = BASE + "tags/linux"
print("Calling GET", get_url)
response = requests.get(get_url)
print(response.json())


print("\nMake a patch request to update the linux tag...")
patch_token = input("Enter the token of the tag you want to update: ")
patch_url = BASE + "tags/linux" + patch_token
print("Calling PATCH", patch_url)
response = requests.patch(patch_url, )
print(response.json())

print("\nDelete linux tag...")
delete_token = input("Enter the token of the tag you want to delete: ")
delete_url = BASE + "tags/linux/" + delete_token
print("Calling DELETE", delete_url)
response = requests.delete(delete_url)
print(response.json())

print("\nMake a get request for the linux tag after its deletion...")
get_url = BASE + "tags/linux"
print("Calling GET", get_url)
response = requests.get(get_url)
print(response.json())


# print("Delete the linux tag")
# delete_url = Base
# print("")
{'name': 'linux', 'contents': "I'd just like to interject for a moment. What you're referring to as Linux is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux...", 'token': 'fwBeB_Lrd2Yvwmb-TQ4d'}
