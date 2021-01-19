"""
Author: Nguyen Le
Date: 1/18/2021
ACM Development Challenge

Challenge 0: 
Write a script in a language of your choice that interacts with the following API (CRUD operations)
API: https://us-central1-acm-core.cloudfunctions.net/challenge
"""

import requests

#--START---------------------CRUD FUNCTIONS---------------------
def post(url, myObj):
    response = requests.post(url, json = myObj)
    return response.json()

def get(url):
    response = requests.get(url)
    return response.json()

def patch(url, myObj):
    response = requests.patch(url, json = myObj)
    return get(url) #return the full content after update

def delete(url):
    response = requests.delete(url)
    return response.ok, response.status_code



#--END---------------------CRUD FUNCTIONS---------------------

#main program
def main():
    url = 'https://us-central1-acm-core.cloudfunctions.net/challenge/tags/linux'
    myObj = {
        "name": "linux",
        "contents": "I'd just like to interject for a moment. What you're referring to as Linux is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux..."
    }
    
    #POST request
    print("\n---1) Making a POST request to create a linux tag...\n")
    post_response = post(url, myObj) #get json response from post request
    print(post_response)
    
    #GET request
    print("\n\n---2) Making a GET request to return a linux tag...\n")
    url_with_token = url + '/' + post_response['token'] #append token to url
    get_response = get(url_with_token)                  #get json response from get request
    print(get_response)
    
    #PATCH request
    update_data = { 'contents': 'Something else' }
    print("\n\n---3) Making a PATCH request to update a linux tag...\n")
    patch_response = patch(url_with_token, update_data) #make a patch request to update "contents"
    print(patch_response)                               #print the full updated content
    
    #DELETE request
    print("\n\n---4) Making a DELETE request to delete a linux tag...\n")
    delete_response = delete(url_with_token)             #get status code whether a delete request was sucessful
    if(delete_response[0]):
        print(delete_response[1], "OK")                  #to match with the expected output specified in the challenge
    else:
        print("DELETE request failed:", delete_response) #delete request fails, prints status code


    
if __name__ == "__main__":
    main()


