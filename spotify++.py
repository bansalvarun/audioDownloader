##########################################
##########################################
########@author Varun Bansal##############
###@Email 'varun13168@iiitd.ac.in'########
##########################################
##########################################

import csv
import string
import pafy #library to download mp3 of a video
import os
import sys
from os import listdir
from os.path import isfile, join
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
#################################################Global Variables############################################

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "REPLACE_ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# csv file downloaded from https://rawgit.com/watsonbox/exportify/master/exportify.html
songsCSV = "*.csv"
# file to maintain previous downloads
downloadedTXT = "puraneDownloads.txt"
# store list of downloaded songs in ram
prevDownloaded = []
# store songs that are not previously downloaded and are in the csv file
toBeDownloaded = set([])
# set of songs successfully downloaded in current session
successfullyDownloaded = set([])
# set of songs unsuccessful in downloading process
unsuccessfulDownloads = set([])
#Directory for downloaded songs
downloadDirectory = "downloads/"
#total data downloaded in current session
totalDownload = 0
#files in downloadDirectory
onlyfiles = []
#############################################################################################################

#setPuraneGane will read the text file having list of previosuly data files and store it in the ram
def setPuraneGane():
  global prevDownloaded
  with open(downloadedTXT, 'w+') as f:
    for line in f:
      prevDownloaded.append(line)
  prevDownloaded = set(prevDownloaded)

#setToBeDownloaded will read csv files and check if the song is not downloaded before, if not, it will be added in the toBeDownloaded set
def setToBeDownloaded():  
  global toBeDownloaded
  global songsCSV
  with open(songsCSV) as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
      break;
    for row in spamreader:
      s = ', '.join(row)
      # print s
      s = s.split(',')
      final = ""
      for i in range(1, len(s)-5):
        s[i] = string.replace(s[i], '"', '')
        final  = final  + s[i] + " "
      final = final.decode('unicode_escape').encode('ascii','ignore')
      if final not in prevDownloaded:
        toBeDownloaded.add(final)

#youtube_search will search for the given term according to the argument strings and return the list of videos from search result
def youtube_search(options):
  #copied from samples given by google developers API python
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
      videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
  return videos
  
def songsInDownloadDir():
  global onlyfiles
  global downloadDirectory
  if not os.path.exists(downloadDirectory):
    os.makedirs(downloadDirectory)
  onlyfiles = [ f.split('.')[0] for f in listdir(downloadDirectory) if isfile(join(downloadDirectory,f)) ]

#downloadSong downloads the song of 0th index from the videos list, it takes two parameters list of videos and searchTerm
def downloadSong(videos, searchTerm):
  global successfullyDownloaded
  global unsuccessfulDownloads
  global downloadDirectory
  global totalDownload
  try:
    url = "https://www.youtube.com/watch?v=" + videos[0].split()[-1][1:-1]
    video = pafy.new(url)
    song = video.getbestaudio()
    songname = song.title  
    songname = songname.split('.')[0]
    songname = string.replace(songname, '/', '_') 
    songname = songname.decode('unicode_escape').encode('ascii','ignore')

    print "name:",songname
    if songname in onlyfiles:
      print "File with the same name already present in folder downloads"
    else:  
      print "Title:", video.title
      print "Size :", round(song.get_filesize()/(1024.0*1024), 2), "MB"
      print "Downloading Audio...\n"
      totalDownload+=round(song.get_filesize()/(1024.0*1024), 2)
      filename = song.download(quiet=False, filepath=downloadDirectory)
      successfullyDownloaded.add(searchTerm)
      print "\nDownload Successful!\n"
  
  except:
    e = sys.exc_info()[0]
    unsuccessfulDownloads.add(searchTerm)
    print "\n*****************Download of ", searchTerm, "is unsuccessful!******************"
    print "Reason is here!"
    print e

#updateDownloadedTXT appends the search terms which have been downloaded successfully in the current session    
def updateDownloadedTXT():  
  global downloadedTXT
  global successfullyDownloaded
  with open(downloadedTXT, 'a') as f:
    for i in successfullyDownloaded:
      f.write(i)
      f.write('\n')

#configure me sets you ready to go for the applications for the first time      
def configureMe():
    global DEVELOPER_KEY
    global songsCSV
    global downloadDirectory
    if DEVELOPER_KEY=="REPLACE_ME":
      print "Hello!"
      print "I am sorry but you few steps away from downloading your songs."
      print "You need to add developer key to use google youtube api which will later let you download the song."
      print "******Instructions to get developer key******"
      print "- Get your Developer key from https://cloud.google.com/console and add it in the scipt in DEVELOPER_KEY variable of the script"
      print "- Create a new project, name it whatever you want."
      print "- Go to credentials in APIs& auth, add a API Key(Browser Key) "
      print "- Set DEVELOPER_KEY to the API key value from the APIs & auth"
      print "- Please ensure that you have enabled the YouTube Data API for your project."
      DEVELOPER_KEY = raw_input("Please enter developer Key: ")
    while(1):
      print "You DEVELOPER_KEY:", DEVELOPER_KEY
      print "Your csv file:", songsCSV
      print "Your downloads folder:", downloadDirectory
      print ""      
      print "1. Update csv file name downloaded from extractify"
      print "2. Update downloads folder"
      print "3. I am ready, let's download songs!"
      print "4. Update Developer Key"
      doNow = raw_input("******Give me your command, sir :>")
      if(doNow=='1'):
        print "Please download your playlist csv file from 'rawgit.com/watsonbox/exportify/master/exportify.html'"
        print "You will have to log in with your spotify account, it will show you all your playlists, downlad the csv file for which one you want the songs be downloaded."
        print "Now Please enter the relative (wrt this file) or absolute path of the csv file you downloaded!"
        songsCSV = raw_input()
      elif(doNow=='2'):
        print "Please enter the relative (wrt this file) or absolute path where you want to create the download folder."
        print "Songs previously present in the folder won't be downloaded again, so you are advised to keep your folder same."
        downloadDirectory = raw_input()
      elif(doNow=='3'):
        break
      elif(doNow=='4'):
        print "******Instructions to get developer key******"
        print "- Get your Developer key from https://cloud.google.com/console and add it in the scipt in DEVELOPER_KEY variable of the script"
        print "- Create a new project, name it whatever you want."
        print "- Go to credentials in APIs& auth, add a API Key(Browser Key) "
        print "- Set DEVELOPER_KEY to the API key value from the APIs & auth"
        print "- Please ensure that you have enabled the YouTube Data API for your project."
        DEVELOPER_KEY = raw_input("Please enter developer key:>")
      else:
        print "Give me valid input!"
    print ""
    print "You DEVELOPER_KEY:>", DEVELOPER_KEY
    print "Your csv file:>", songsCSV
    print "Your downloads folder:>", downloadDirectory
        
      
print "Hello User!"
if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=1)
  args = argparser.parse_args()
  configureMe()
  #Reading previosuly downloaded songs list
  setPuraneGane()
  #settings songs present in directory
  songsInDownloadDir()

  # print "ONLY FILES"
  # for i in onlyfiles:
  #   print i  
  # print "ONLY FILES"

  #Getting the list of songs need to be downloaded in this session
  setToBeDownloaded()
  print "Total songs to be downloaded:", len(toBeDownloaded)
  #variable to maintain burrent download number
  current_num = 1    
  for searchTerm in toBeDownloaded:
    print "\nDownloading", current_num, "/", len(toBeDownloaded)
    print searchTerm
    args.q = searchTerm
    try:
      videos = youtube_search(args)
    except:
      e = sys.exc_info()[0]
      print "You have probably not addded yout youtube api properly, try checking your google api or contact author!"
      print e
      unsuccessfulDownloads.add(searchTerm)
    downloadSong(videos, searchTerm)
    current_num+=1
  print "Total download size in this session:", totalDownload, "MB\n"
  if len(unsuccessfulDownloads)>0:
    print "Following videos could not be downloaded:"
    for i in unsuccessfulDownloads:
      print ":<<",i
  
 
 
 
 
print "Bye See You Soon!"
 
 
 