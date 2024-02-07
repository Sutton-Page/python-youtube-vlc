from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import json
import os
import pickle

test_video_id = "f3bVM2mxh4k"

# Cred Path must end in \\cred\\

def gen_creds(project_path=None):
    
    if project_path == None:
        project_path = os.path.abspath(os.getcwd())

    if os.path.exists(project_path) == True:

        if project_path.endswith('\\') == False:
            project_path+='\\'

        pickle_cred = project_path+"cred\\token.pickle"
        credentials = None

        if os.path.exists(pickle_cred) == True:
            
            with open(pickle_cred,'rb') as token:
                credentials = pickle.load(token)

            if credentials.valid == False or credentials.expired == True:
                print('Renewing credentials')
                credentials.refresh(Request())
                return credentials

            else:
                return credentials 

        else:

            scope = "https://www.googleapis.com/auth/youtube.readonly"
            flow = InstalledAppFlow.from_client_secrets_file('client_secert.json',
                                                 scopes=[scope])

            flow.run_local_server(port=8080,prompt='consent',authorization_prompt_message='')
            credentials = flow.credentials
            os.mkdir(project_path+"cred\\")
            with open(pickle_cred,'wb') as f:
                print("Saving credentials to a file")
                pickle.dump(credentials,f)
                return credentials

    else:
        print("Project Path does not exist")


# data_type
# channel
# playlist
# search_results (Must be plural) 
# video_data
# playlist_item (for videos from playlist)
def extract_content_data(content_data,data_type=None,dict_key='title'):

    data_holder = {}
    content_id = None
    content_type = None

    if content_data['items']!=None:

        for item in content_data['items']:
            thumbnail = None

            try:
                snip = item.get('snippet')
                thumbnail = snip.get('thumbnails').get('medium').get('url')

            except AttributeError:
                pass

            # geting data
            title = snip.get('title')
            description = snip.get('description')
            if data_type == 'channel':

                try:
                    inline_resource_channel_dict = snip.get('resourceId')

                    # must be content_id as I use it later
                    content_id = inline_resource_channel_dict.get('channelId')

                except AttributeError:
                    content_id = item['id']

            if data_type == 'playlist':
                content_id = item.get('id')
                playlist_channel_id = snip.get('channelId')

            if data_type == 'playlist_item':
                inline_resource_video_dict = snip.get('resourceId')
                content_id = inline_resource_video_dict.get('videoId')

            if data_type == 'search_results':
                id_div = item.get('id')
                id_div_kind = id_div.get('kind')
                id_type = id_div_kind.split("#")[1]
                content_id = id_div.get(id_type+"Id")
                content_type = id_type

            format_dict = {}
            if data_type =='video_data':

                stat = item.get('statistics')
                stat_keys = list(stat.keys())
                channel_id = snip.get('channelId')

                for key in stat_keys:
                    format_dict[key] = stat[key]

                pubdate = snip.get('publishedAt')
                format_dict['pubdate'] = pubdate
                format_dict['channelId'] = channel_id

            format_dict['description'] = description
            format_dict['thumbnail'] = thumbnail
            if data_type == 'playlist':
                format_dict['channel_id'] = playlist_channel_id

            if content_type!=None:
                format_dict['type'] = content_type
                
            if dict_key == 'id':
                format_dict['title'] = title
                data_holder[content_id] = format_dict

            else:
                format_dict['id'] = content_id

                # Put in place to remove private videos (results)
                #if title!="Private video":

                if title == "Private video":
                    title = '[Error Private Video cannot select] '
                
                data_holder[title] = format_dict

        return data_holder


# checks for update and updates local json file
# returns a list of new subscription ids

def check_for_subscription_update(youtube_api,local_user_data_path):

    if os.path.exists(local_user_data_path) == True:

        # loading in local user data
        file_handle = open(local_user_data_path,'r')
        local_user_data = json.load(file_handle)
        local_subscription_ids = list(local_user_data['channels'].keys())

        # loading subscription data from internet
        subscription_query = youtube_api.subscriptions().list(part='snippet',mine=True,maxResults=50)
        internet_data = subscription_query.execute()
        parsed_internet_data = extract_content_data(internet_data,'channel',dict_key='id')

    # Checking keys ( New subscriptions )
        new_subscription_ids = []
        for key in parsed_internet_data.keys():
            if local_subscription_ids.__contains__(key) == False:
                new_subscription_ids.append(key)

        for key in new_subscription_ids:
            local_user_data['channels'][key] = parsed_internet_data[key]

        update_file_handle = open(local_user_data_path,'w')
        json_formated_data = json.dumps(local_user_data)
        update_file_handle.write(json_formated_data)
        update_file_handle.close()
        return new_subscription_ids
        
    else:
        print('Please provide valid local user data file path')
    
 






                    

            
