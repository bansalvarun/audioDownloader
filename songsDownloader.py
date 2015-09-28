#library to download mp3 of a video
import pafy

# to download in a folder
import os
from os import listdir
from os.path import isfile, join

# library for youtube api
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "REPLACE_ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()
  videos = []
  # Add each result to the appropriate list, and then display the lists of
  # matching videos
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
  return videos
  # videoUrl =  videos[0].split()[-1][1:-1];
  # return videoUrl

def downloadSong(videos, i):
  url = "https://www.youtube.com/watch?v=" + videos[i].split()[-1][1:-1]
  # print i, url
  video = pafy.new(url)
  print video.title
  s = video.getbestaudio()
  print "Size is: ", round(s.get_filesize()/(1024.0*1024), 2), "MB"
  format = str(s)
  format = "." + format.split('@')[0].split(':')[1]
  directory = "downloads/"
  
  if not os.path.exists(directory):
    os.makedirs(directory)
  onlyfiles = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
  if s.title+"format" in onlyfiles:
    print "File with the same name already present in folder downloads"
    print "Enter other index number or exit by -1"
  else:  
    # print "Downloading Audio..."
    filename = s.download(quiet=False, filepath=directory)
    print "\nDownload Succcessful!\n"
    

if __name__ == "__main__":
# def main():
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=10)
  while(1):
    print "Please enter the search keyword or string or any google search you wanna do for a video OR enter 'exit' to exit"
    searchTerm = raw_input()
    if searchTerm == "exit":
      break;
    else:
      args = argparser.parse_args()
      args.q = searchTerm
      # print type(args)
      # print args
      url = ""
      videos = youtube_search(args)
      print "-1 to Search again"
      for i in range(len(videos)):
        try:
          print i , videos[i]
        except UnicodeEncodeError, e:
          print "INVALID Video, Please don't try to download this url"
      if(len(videos)>1):
        print "Please give me the index number from above to download or -1 to exit:"
        while(1):
          i = input()
          if(i>=0 and i< len(videos)):
            try:
              downloadSong(videos, i)
              break
            except UnicodeEncodeError, e:
              print "Invalid video, try any other index number,  Please don't try to download this url again -.-"
          elif i==-1:
            break  
          else:
            print "Please enter a valid index number from", 0, "to", len(videos)-1
      else:
        print "Downloading Video.."
        downloadSong(videos, 0)
