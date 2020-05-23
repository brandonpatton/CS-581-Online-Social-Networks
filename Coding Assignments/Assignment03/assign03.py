#  I pledge my honor that I have abided by the Stevens Honor System
#  Author:  Brandon Patton 
#  Assignment 03 - Using the Google APIs to access YouTube Data
#  assign03.py searches YouTube for videos matching a search term

# To run from terminal window:   python3 assign03.py 

from apiclient.discovery import build      # use build function to create a service object

import unidecode   #  need for processing text fields in the search results

import sys, csv

# put your API key into the API_KEY field below, in quotes
API_KEY = "AIzaSyAebR-xqwPccUQ08CQw494MFP2n_9KkAfA"

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version

top5Viewed = []
top5LikeP = []
top5DislikeP = []
#  function youtube_search retrieves the YouTube records

def youtube_search(s_term, s_max):
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)

    search_response = youtube.search().list(q=s_term, part="id,snippet", maxResults=s_max).execute()

    collection = []
    
    # search for videos matching search term;
    
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  
            videoId = search_result["id"]["videoId"]
            video_response = youtube.videos().list(id=videoId,part="statistics").execute()
            for video_results in video_response.get("items",[]):
                viewCount = video_results["statistics"]["viewCount"]
                if 'likeCount' not in video_results["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_results["statistics"]["likeCount"]
                if 'dislikeCount' not in video_results["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_results["statistics"]["dislikeCount"]
                if 'commentCount' not in video_results["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_results["statistics"]["commentCount"]
            top5Viewed.append([title, videoId, int(viewCount)])
            top5LikeP.append([title, videoId, int(likeCount)/int(viewCount)])
            top5DislikeP.append([title, videoId, int(dislikeCount)/int(viewCount)])
            collection.append([title, videoId, str(viewCount), str(likeCount), str(dislikeCount), str(commentCount)])   
    return collection

def top5collection(collection):
    #Creates a top 5 list by using a running max/top video
    top5 = []
    count = 0
    while(count < 5):
        top = [None, None, 0]
        for video_info in collection:
            if(video_info[2] > top[2] and not(video_info in top5)):
                top = video_info
        top5.append(top)
        count += 1
    return top5


def rowWriter(lst, fd):
    #Writes rows for (nested) lists
    for i in lst:
        w = csv.writer(fd)
        w.writerow(i)

def printAll(lst): 
    for i in lst:
        print(str(i))

# main routine
    
def main():
    search_term = "baby"
    search_max = 20
    search_results = youtube_search(search_term, search_max)

    with open('output.csv', 'w', newline='\n') as fd:
        headers = ["title" , "tvideoId" , "tviewCount" , "likeCount" , "dislikeCount" , "commentCount"] 
        
        w = csv.writer(fd)
        w.writerow(headers)
        #search results to 'output.csv'
        rowWriter(search_results, fd)
        #analysis to 'output.csv'
        w.writerow('')
        w.writerow(["title" , "videoId" , "viewCount"])
        rowWriter(top5collection(top5Viewed), fd)
        w.writerow('')
        w.writerow(["title" , "videoId" , "likeCount/viewCount"])
        rowWriter(top5collection(top5LikeP), fd)
        w.writerow('')
        w.writerow(["title" , "videoId" , "dislikeCount/viewCount"])
        rowWriter(top5collection(top5DislikeP), fd)

        print("Search term: " + str(search_term))
        print("Search Max: " + str(search_max) + '\n')

        #analysis to console
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Analysis ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        print("------------------------------------------------------------------------ Top 5 Highest Views ------------------------------------------------------------------------")
        print("Format: [title, videoId, viewCount]")
        
        printAll(top5collection(top5Viewed))
        print("------------------------------------------------------------------------ Top 5 Like Percentage ------------------------------------------------------------------------")
        print("Format: [title, videoId, likeCount/viewCount]")
        printAll(top5collection(top5LikeP))
        print("------------------------------------------------------------------------ Top 5 Dislike Percentage ------------------------------------------------------------------------")
        print("Format: [title, videoId, dislikeCount/viewCount]")
        printAll(top5collection(top5DislikeP))


if __name__ == "__main__":
    main()