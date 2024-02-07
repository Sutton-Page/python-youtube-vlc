from googleapiclient.discovery import build
from api_funcs import *


creds = gen_creds()
api_client = build('youtube','v3',credentials=creds)
subscription_query = api_client.subscriptions().list(part='snippet',mine=True,
                                                  maxResults=50)


subscription_data = subscription_query.execute()
channel_data = extract_content_data(subscription_data,'channel')

# grabbing playlists of first subscription channel
test_channel_id = channel_data[list(channel_data.keys())[0]]['id']
playlist_query = api_client.playlists().list(part='snippet',
                                             channelId=test_channel_id,
                                             maxResults=50)
playlist_data = playlist_query.execute()
