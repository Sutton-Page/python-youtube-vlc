
from googleapiclient.discovery import build

# important data
api_key = "AIzaSyD2YfOBTjcQKJ0WK-PsY90_9syiAv78s48"
base_youtube_url='https://www.youtube.com/watch?v='
youtube = build('youtube','v3',developerKey=api_key)


#search = youtube.search().list(part='snippet',type='video',order='date',channelId="UCaWd5_7JhbQBe4dknZhsHJg",
#                               maxResults=50)

search = youtube.search().list(part='snippet',type='video',q='ign',
                               maxResults=50)

result = search.execute()

total_item_len = len(result['items'])-1

next_search_token = result['nextPageToken']

search_results = []

start_index = 0

while start_index <=total_item_len:

    holder = {}

    item = result['items'][start_index]

    item_title = item['snippet']['title']

    item_image = item['snippet']['thumbnails']['medium']['url']

    item_id = item['id']['videoId']

    item_url = base_youtube_url+item_id

    holder['title'] = item_title

    holder['image_url'] = item_image

    holder['url'] = item_url

    search_results.append(holder)

    start_index+=1

    
