import requests
import pandas as pd
import json
from dotenv import load_dotenv
import os


def printData():
    # print(f"isbn: {isbn}")
    # print(f"Title: {title}")
    # print(f"Categories: {unique_categories}")
    # print(f"Authors: {unique_authors}")
    # print(f"Price: {price} {currencyType}")
    # # print(f"Currency: {currencyType}")
    # print(f"date: {date}")
    # print(f"pageCount: {pageCount}")
    # print(f"eBook: {isEbook}")
    # print(f"epub: {isEpub}")
    # print(f"pdf: {isPDF}")
    # print(f"selfLink: {selfLink}")
    print("\n")

load_dotenv()       
api_key = os.getenv('GOOGLE_BOOKS_API_KEY')


def fetchData(query="", author="", maxResults = 40, batch_size=120):

    # https://developers.google.com/books/docs/v1/using#st_params
    # "When creating a query, list search terms separated by a '+', in the form q=term1+term2_term3"
    startIndex = 0
    all_books = []
    while startIndex <= batch_size:
        url = (f"https://www.googleapis.com/books/v1/volumes?q={query}+inauthor:{author}&startIndex={startIndex}&maxResults={maxResults}&key={api_key}")

        startIndex += maxResults
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json() 

            # formatted as {kind, id, etag, selflink} and {volumeInfo/ , layerInfo/ , saleInfo/ , accessInfo/}
            for item in data.get('items', {}):
                #.get() method is used to retrieve the value associated with a key in a dictionary.
                # Safer than direct index ([]) bc it allows default rv if key not present- this allows for default error handling
                selfLink = item.get('selfLink', "N/A")

                # 'volumeInfo'
                ''' 
                API ISSUE? : for some reason when I directly call to get the categories via API call, the call only returns 1 category, the first one.
                For example:  
                    categories = volumeInfo.get('categories', [])
                should return what the selfLink returns: 3 rows of categories in a dict. Instead it only return 1 only 1 value. This can be seen also by 
                directly printing our data: 'print(data)'. Maybe I am just a noob... but this confuses me and makes me reconsider only using selfLink
                '''
                data_selfLink = requests.get(selfLink)
                data_full = (data_selfLink).json()

                # getting unique categories was harder than expected lol
                volumeInfo2 = data_full.get('volumeInfo', {})
                categories = volumeInfo2.get('categories', [])
                unique_categories = set()
                for category in categories:
                    parts = category.split('/')
                    for cat in parts:
                        unique_categories.add(cat.strip())

                volumeInfo = item.get('volumeInfo', {})
                title = volumeInfo.get('title', "N/A")
                authors = volumeInfo.get('authors', [])
                unique_authors = set()
                for author in authors:
                    unique_authors.add(author.strip())

                description = volumeInfo.get('description', "N/A")
                date = volumeInfo.get('publishedDate', "N/A")
                
                
                industryIdentifier = volumeInfo.get('industryIdentifiers', {})
                isbn = industryIdentifier[0].get('identifier', {}) if industryIdentifier else "N/A"
                pageCount = volumeInfo.get('pageCount', None)

                imageLinks = volumeInfo.get('imageLinks', {})
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


                all_books.append({
                            'isbn':isbn,
                            'title':title,
                            'description':description,
                            'author':unique_authors,
                            'category':unique_categories,
                            'date':date,
                            'pageCount':pageCount,
                            'price': price,
                            'currency': currencyType,
                            'smallImage':smallImage,
                            'largeImage':largeImage,
                            'isEbook':isEbook,
                            'isEpub':isEpub,
                            'isPDF':isPDF
                })
        else:
            print(f"Request failed with status code {response.status_code}")
    
    return all_books



alex = fetchData(query="data+engineering", maxResults=4, batch_size= 9)

for tom in alex:
    print(tom)
    print("\n")