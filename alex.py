import requests
import pandas as pd
import json


def printData():
    print(f"isbn: {isbn}")
    print(f"Title: {title}")
    # print(f"Categories: {', ' .join(categories)}")
    print(f"Authors: {', ' .join(authors)}")
    print(f"Price: {price} {currencyType}")
    # print(f"Currency: {currencyType}")
    
    print(f"date: {date}")
    print(f"pageCount: {pageCount}")
    print(f"eBook: {isEbook}")
    print(f"epub: {isEpub}")
    print(f"pdf: {isPDF}")
    print(f"selfLink: {selfLink}")
    print("\n")

myKey = "AIzaSyCv96E3WC4c1cycIyp0ywBzLihuM0BOVWE"

# define query #-- make function
query = "data+engineering"
author = ""

url = (f"https://www.googleapis.com/books/v1/volumes?q={query}+inauthor:{author}&key={myKey}")

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # formatted as {kind, id, etag, selflink} and {volumeInfo/ , layerInfo/ , saleInfo/ , accessInfo/}
    for item in data.get('items', 'No data on Item'):
        
        #.get() method is used to retrieve the value associated with a key in a dictionary.
        # Safer than direct index ([]) bc it allows default rv if key not present
        selfLink = item.get('selfLink', "N/A")

        # volumeInfo ** 
         # struggling to flatten categories but want to add
         
        volumeInfo = item.get('volumeInfo', {})

        title = volumeInfo.get('title', "N/A")
        authors = volumeInfo.get('authors', [])
        description = volumeInfo.get('description', "N/A")
        date = volumeInfo.get('publishedDate', "N/A")
        # categories = item.get('volumeInfo', {}).get('categories', {})
        
        industryIdentifier = volumeInfo.get('industryIdentifiers', [])
        isbn = industryIdentifier[0].get('identifier', {}) 

        pageCount = volumeInfo.get('pageCount', None)

        imageLinks = volumeInfo.get('imageLinks', "N/A")
        smallImage = imageLinks.get('thumbnail', "N/A")
        largeImage = imageLinks.get('extraLarge', "N/A")

        # 'saleInfo' - not every book has a price so we cant nested search for it. Have to split into parent category then actual value
        saleInfo = item.get('saleInfo', {})
        isEbook = saleInfo.get('isEbook', False)

        listPrice = saleInfo.get('listPrice', {})
        price = listPrice.get('amount', None)
        currencyType = listPrice.get('currencyCode', 'N/A')

        # 'acccessInfo'
        acccessInfo = item.get('accessInfo', {})
        isEpub = acccessInfo.get('epub', {}).get('isAvailable', False)
        isPDF = acccessInfo.get('pdf', {}).get('isAvailable', False)

        printData()
else:
    print(f"Request failed with status code {response.status_code}")

