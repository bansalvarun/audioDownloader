# Audio Downloader

This is a python Script which uses google api to search videos for the keyword and download the audio of the respective video using pafy library.

Instructions for setup
------------

- Clone the project

        git clone https://github.com/bansalvarun/audioDownloader.git 
        cd audioDownloader

- Install the project's runtime requirements

        pip install -r requirements.txt

- Get your Developer key from https://cloud.google.com/console and add it in the scipt in DEVELOPER_KEY variable of the script
  - Create a new project, name it whatever you want.
  - Go to credentials in APIs& auth, add a API Key(Browser Key) 
  - Set DEVELOPER_KEY to the API key value from the APIs & auth
  - Please ensure that you have enabled the YouTube Data API for your project.


- Run the script 

        python songsDownloader.py
        

    * On running, script prompts the user to enter keyword to search 
    * It will give user the search result
    * Succesful downloads are stored in the relative folder 'downloads'
    * To set max-search results run 
            
            python songsDownloader.py --max-results value
            
            value: maximum number of results you want
    

Issues
------------

Please report any bugs or requests that you have using the GitHub issue tracker!


**Author is not liable for any misuse; Use carefully!
