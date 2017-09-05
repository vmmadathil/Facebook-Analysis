import json, datetime, requests
import pandas as pd

# Get FB API information
with open("FBInfo.txt") as f:
    APP_ID = f.readline().rstrip()
    APP_SECRET = f.readline().rstrip()

# Set Global Constants
LIMIT = 100
BASE_URL = "https://graph.facebook.com/v2.10/"
COLUMNS = ["created_time", "message", "from", "id"]

# Scrape a page for posts
def scrapePage(data,page_id,access_token):
    # Start scraping the page
    print("{} : Scraping Posts From Page {} ...\n".format(datetime.datetime.now(),page_id))

    # GET request
    parameters = "?access_token=" + access_token + "&limit=" + str(LIMIT)
    getPosts = requests.get(BASE_URL + page_id + "/posts" + parameters)
    posts = getPosts.json()['data']

    # For each post get the comments
    count = 0
    for post in posts:
        data  = getCommentsFromPost(data,post,access_token)
    return data

# Get the comments from a specific post 
def getCommentsFromPost(data,post,access_token):
    # GET request
    parameters = "?access_token=" + access_token + "&limit=" + str(LIMIT)
    getComments = requests.get(BASE_URL + post['id'] + "/comments" + parameters)
    comments = getComments.json()['data']
    # Append all comments
    dataToAdd = pd.DataFrame(comments,columns=COLUMNS)
    data = data.append(dataToAdd,ignore_index=True)
    return data

if __name__ == '__main__':
    # Create the data frame
    data = pd.DataFrame(columns=COLUMNS)
    access_token = APP_ID + "|" + APP_SECRET

    # What page do we want to run
    page_id = "367963843082"

    # Start the scraping
    data = scrapePage(data,page_id, access_token)
    listOfNames = []
    listOfNameIDs = []
    for entry in data['from']:
        listOfNames.append(entry['name'])
        listOfNameIDs.append(str(entry['id']))

    data['User'] = pd.Series(listOfNames)
    data['User_ID'] = pd.Series(listOfNameIDs,dtype=str)
    del data['from']

    # From here use awk to re-order columns or rename column names
    # Use bash to sort or get unique names etc
    # Send the pandas data frame to the clustering part of the code

    # Export the table
    print("Completed scraping. Exporting DataFrame...")
    filename = page_id + "_facebook_comments.csv"
    data.to_csv(filename, index=True, encoding='utf-8')
    print("Exported!")
