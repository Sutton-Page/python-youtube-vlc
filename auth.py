from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request
import os
import pickle
import api_funcs
from api_funcs import *



credentials = gen_creds()


youtube = build('youtube','v3',credentials=credentials)

channel = youtube.subscriptions().list(part='snippet',mine=True,
                                      order='alphabetical',maxResults=50)

res = channel.execute()

subscription_data = extract_api_data(res,dev=True)

channel_id = subscription_data[0]['channel_id']

playlists = youtube.playlists().list(part='snippet',channelId=channel_id,
                                    maxResults=50)

playlist_result = playlists.execute()


playlist_data = extract_api_data(playlist_result,dev=True)

# playlist videos test

playlist_id = playlist_data[0]['playlist_id']

play_videos = youtube.playlistItems().list(part='snippet',playlistId=playlist_id,
                                          maxResults=50)

playlist_videos = play_videos.execute()

parsed_playlist_videos = extract_api_data(playlist_videos,video_data=True,dev=True)





 
