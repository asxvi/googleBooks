import requests
import pandas as pd
import json


def printData():
    print(f"Title: {title}")
    print(f"Categories: {', ' .join(categories)}")
    print(f"Authors: {', ' .join(authors)}")
    print(f"Price: {price} {currencyType}")
    # print(f"Currency: {currencyType}")
    
    print(f"eBook: {isEbook}")
    print(f"epub: {isEpub}")
    print(f"pdf: {isPDF}")
    print(f"selfLink: {selfLink}")
    print("\n")

myKey = "AIzaSyCv96E3WC4c1cycIyp0ywBzLihuM0BOVWE"

# separate query with +
query = "data+engineering"
author = ""

url = (f"https://www.googleapis.com/books/v1/volumes?q={query}+inauthor:{author}&key={myKey}")

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # formatted as {kind, id, etag, selflink} and {volumeInfo/ , layerInfo/ , saleInfo/ , accessInfo/}
    for item in data['items']:
        #.get() method is used to retrieve the value associated with a key in a dictionary.
        # Safer than direct index ([]) bc it allows default rv if key not present
        selfLink = item.get('selfLink', {})

        title = item['volumeInfo'].get('title', {"No Title info"})
        authors = item['volumeInfo'].get('authors', {"No Author info"})
        description = item['volumeInfo'].get('description', {})


        # volume info ** 
        # struggling to flatten categories but want to add
        #categories = item.get('volumeInfo', {}).get('categories', {})

        imageLinks = item['volumeInfo'].get('imageLinks', {})
        smallImage = imageLinks.get('thumbnail', {})
        largeImage = imageLinks.get('extraLarge', {})

        # 'saleInfo' - not every book has a price so we cant nested search for it. Have to split into parent category then actual value
        isEbook = item['saleInfo'].get('isEbook', {})
        listPrice = item['saleInfo'].get('listPrice', {})
        price = listPrice.get('amount', 'NA')
        currencyType = listPrice.get('currencyCode', '')


        # 'acccessInfo'
        isEpub = item['accessInfo']['epub'].get('isAvailable', {})
        isPDF = item['accessInfo']['pdf'].get('isAvailable', {})

        # printData()


# #  Print some of the information returned (like book titles and authors)
#     print("Books found:")
#     for item in data['items']:
#         volume_info = item.get("volumeInfo", {})

#         title = item['volumeInfo'].get('title', 'No title available')
#         authors = item['volumeInfo'].get('authors', ['No authors available'])
#         # selfLink = item['selfLink'].get('selfLink', ['No self link avaliable'])
#         description = volume_info.get("description", "No description available")
#         print(f"Title: {title}")
#         print(f"Authors: {', '.join(authors)}\n")
#         # print(f"Self Link: {selfLink}\n")
#         print(f"Description: {description}\n")
else:
    print(f"Request failed with status code {response.status_code}")

