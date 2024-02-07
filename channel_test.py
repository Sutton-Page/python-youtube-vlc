from googleapiclient.discovery import build

# important urls
api_key = "AIzaSyD2YfOBTjcQKJ0WK-PsY90_9syiAv78s48"
base_youtube_url='https://www.youtube.com/watch?v='

# accessing the youtube api
youtube = build('youtube','v3',developerKey=api_key)
mojo_channel_key="UCaWd5_7JhbQBe4dknZhsHJg"
channel_search = youtube.search().list(part='snippet',type='channel',q='watchmojo',maxResults=20)
res = channel_search.execute()
