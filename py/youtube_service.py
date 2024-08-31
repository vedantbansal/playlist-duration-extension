from googleapiclient.discovery import build
import re
from datetime import timedelta
import json

class yt_service_impl:

    def __init__(self, playlistId):
        self.playlistId = playlistId
        #get current working directory
        cwd = '/'.join(__file__.split('/')[:-1])
        self.get_api_key(f"{cwd}/secrets.json")
        self.build_service()

    #Fetch the api key from secrets.json
    def get_api_key(self, json_file):
        try: 
            with open(json_file) as file:
                file = json.load(file) 
                self.api_key  = file["api-key"]

        except: 
            print("Unable to retrieve api key")
            exit()

    def build_service(self):
        #Create a service object
        self.service = build('youtube','v3',developerKey = self.api_key)

        #regex to parse hours, minutes and seconds
        self.hours_pattern = re.compile(r'(\d+)H')
        self.minutes_pattern = re.compile(r'(\d+)M')
        self.seconds_pattern = re.compile(r'(\d+)S')

        self.total_seconds = 0
 
    #Get a list containing all the ids in playlist
    def get_total_videoID(self):
        
        #To iterate over pages
        nextPageToken = None    
        self.total_vidID = []

        while True:
            #Request data of playlist. 
            request = self.service.playlistItems().list(
                part = 'contentDetails',
                playlistId = self.playlistId,
                maxResults = 100,
                pageToken= nextPageToken
            )
            response = request.execute()

            #list of 50 video ids
            vid_id = [item['contentDetails']['videoId'] for item in response['items'] ] 
            self.total_vidID += vid_id

            #Increase pagetoken
            nextPageToken = response.get('nextPageToken')

            #Checks if next page is present, if not, breaks while loop
            if not nextPageToken:
                break

    def calculate_duration(self):
        self.get_total_videoID()
        for id in range(0,len(self.total_vidID),50):

            #Requesting data of video
            vid_id = self.total_vidID[id:id+50]
            vid_request = self.service.videos().list(
                part = 'contentDetails',
                id = ','.join(vid_id)
            )

            vid_response = vid_request.execute()

            #iterate over each data of each video
            for item in vid_response['items']:
                duration = item['contentDetails']['duration'] # duration of a video

                #parsing time of video using above regex
                hours = self.hours_pattern.search(duration)
                minutes = self.minutes_pattern.search(duration)
                seconds = self.seconds_pattern.search(duration)

                #if some value is not present it changes it to 0
                hours = int(hours.group(1)) if hours else 0
                minutes = int(minutes.group(1)) if minutes else 0
                seconds = int(seconds.group(1)) if seconds else 0
                
                #convert duration to seconds and sums it
                video_secs= timedelta(
                    hours = hours,
                    minutes=minutes,
                    seconds=seconds
                ).total_seconds()
                
                #sum of videos
                self.total_seconds += int(video_secs)
            
        duration = self.parse_seconds()
        return {"hours": duration[0], "minutes":duration[1], "seconds": duration[2]}

    def parse_seconds(self):
        minutes, seconds = divmod(self.total_seconds, 60)
        hours, minutes = divmod(minutes, 60)

        return [hours, minutes, seconds]

