
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import urllib
import io
from urllib import request
import tkinter as tk
import PIL
from PIL import Image
from PIL import ImageTk
import api_funcs
from api_funcs import *

# For testing purposes
import os
import shutil

def subscriptions_menu_loop(youtube_api,print_messages):

    # Making request to API to get user subscriptions and parsing returned json
    user_subscription_data = youtube_api.subscriptions().list(part='snippet',mine=True,maxResults=25).execute()
    parsed_user_subscription_data = extract_content_data(user_subscription_data,'channel')

    # getting next page token if the user has more than 25 channel subscriptions
    try:
        next_page_token = user_subscription_data['nextPageToken']
    except KeyError:
        next_page_token = None
    
    # Adding message to print_messages array 
    subscription_number = len(list(parsed_user_subscription_data.keys()))
    subscrition_number_string = "You have subscribed to  "+str(subscription_number)+" channels"
    print_messages.insert(1,subscrition_number_string)

    # Grabbing Youtube api object to pass to Menu_Loop
    api_object = youtube_api.subscriptions()
    api_args = {'part':'snippet','mine':True,'maxResults':25}

    # starting loop
    Content_Loop = Menu_Loop(parsed_user_subscription_data,next_page_token,print_messages,api_object,api_args)
    Content_Loop.start_loop(youtube_api,'channel','channel')



def channel_menu_loop(youtube_api_handle,channel_id):

    channel_data = youtube_api_handle.channels().list(part='snippet,contentDetails',id=channel_id).execute()
    parsed_data = extract_content_data(channel_data,'channel')
    channel_title = list(parsed_data.keys())[0]
    channel_description = parsed_data[channel_title]['description']
    channel_thumbnail = parsed_data[channel_title]['thumbnail']

    # Special channel data
    channel_creation_date = channel_data['items'][0]['snippet']['publishedAt']
    #[0]['publishedAt']

    # grabbing channel videos

    # Channel upload playlist id
    channel_uploads_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    channel_video_data = youtube_api_handle.playlistItems().list(part='snippet',playlistId=channel_uploads_id,maxResults=25).execute()

    #channel_video_data = youtube_api_handle.search().list(part='snippet',channelId=channel_id,
                                                        #  order='date',maxResults=25).execute()
    parsed_channel_video_data = extract_content_data(channel_video_data,'playlist_item')
    result_titles = list(parsed_channel_video_data.keys())

    ############################################
    newest_video_data = parsed_channel_video_data[result_titles[0]]

    # Print data
    messages = []
    spacer = '------------------------------------'
    messages.append(spacer)
    messages.append('Location://Channel-Menu')
    messages.append('Channel: '+channel_title)
    messages.append('Created: '+channel_creation_date)
    messages.append('Type [c] to see channel thumbnail')
    messages.append(spacer)
    messages.append("Newest Video: "+result_titles[0])
    messages.append("Type [n] to select newest channel video")
    messages.append("Type [t] to see newest video thumbnail")
    messages.append(spacer)
    messages.append("Other options:")
    messages.append("Type [v] to list channel videos")
    messages.append("Type [p] to list channel playlist")
    messages.append("Type [b] to go back ")
    messages.append(spacer)

    ################

    while True:

        terminal_size = shutil.get_terminal_size().columns
        for message in messages:
            print(message)

        user_choice = input()

        if user_choice == 'c':
            req = urllib.request.urlopen(channel_thumbnail)
            data = req.read()

            # Generate popup menu to display image 
            main = tk.Tk()
            title_lab = tk.Label(main,text="Title: "+channel_title)
            image = PIL.Image.open(io.BytesIO(data))
            image_item = PIL.ImageTk.PhotoImage(image)
            image_label = tk.Label(main,image=image_item)
            title_lab.pack(side='top')
            image_label.pack(side='top')
            main.mainloop()
            
        if user_choice == 'n':
            print("Changing to video menu")
            new_channel_video_id = parsed_channel_video_data[result_titles[0]]['id']
            video_menu_loop(youtube_api_handle,new_channel_video_id)

        if user_choice == 't':
            new_channel_video_thumbnail_url = parsed_channel_video_data[result_titles[0]]['thumbnail']
            req = urllib.request.urlopen(new_channel_video_thumbnail_url)
            data = req.read()

            # Generating popup window with image and information
            main = tk.Tk()
            title_lab = tk.Label(main,text="Title: "+result_titles[0])
            image = PIL.Image.open(io.BytesIO(data))
            image_item = PIL.ImageTk.PhotoImage(image)
            image_label = tk.Label(main,image=image_item)
            title_lab.pack(side='top')
            image_label.pack(side='top')
            main.mainloop()

        if user_choice == 'p':
            channel_playlist_data = youtube_api_handle.playlists().list(part='snippet',channelId=channel_id,
                                                                 maxResults=25).execute()
            parsed_channel_playlist_data = extract_content_data(channel_playlist_data,'playlist')
            next_page_token = None

            try:
                next_page_token = channel_playlist_data['nextPageToken']

            except KeyError:
                pass
            
            # Adding messages to print to print array
            print_messages = []
            print_messages.append('-----------------------')
            print_messages.append('Channel Playlists')
            print_messages.append('Type playlist index to choose playlist')

            # Organizing data to pass back to main loop
            api_stub = youtube_api_handle.playlists()
            api_args = {'part':'snippet','channelId':channel_id,'maxResults':25}
            test_loop = Menu_Loop(parsed_channel_playlist_data,next_page_token,print_messages,api_stub,api_args)
            test_loop.start_loop(youtube_api_handle,'playlist_menu','playlist')

        if user_choice == 'v':
            # channel_video_data
            # parsed_video_data
            ### Creating unique menu loop

            try:
                next_page_token = channel_video_data['nextPageToken']

            except KeyError:
                next_page_token = None

            api_stub = youtube_api_handle.playlistItems()
            api_args = {'part':'snippet','playlistId':channel_uploads_id,'maxResults':25}

            # Adding messages to print to print_messages array
            print_messages = []
            print_messages.append('Location://Channel//Video//Menu')
            print_messages.append('Videos from the channel '+channel_title)
            print_messages.append('enter a video index to select it')

            # Grading data to pass back to main loop
            test_loop = Menu_Loop(parsed_channel_video_data,next_page_token,print_messages,api_stub,api_args)
            test_loop.start_loop(youtube_api_handle,'playlist_item','video')

        if user_choice == 'b':
            print("going to previous menu or ending script")
            break



def search_menu_loop (youtube_api_handle):

    # Bug with channel search will add back later
    # For now just removing reference to channel search in print messages
    while True:
        terminal_size = shutil.get_terminal_size().columns
        search_type_choices = {'a': '','v':'video','p':'playlist'}

        # Adding messsage to message array
        messages = []
        messages.append("--------------------------------------------")
        messages.append("Location://Menu//Search")
        messages.append("Set Search type: all (a) , video (v), playlist (p)")
        messages.append("type [b] to go to previous menu. during testing this close to script")

        # printing it out
        for message in messages:
            print(message.center(terminal_size))

        user_search_type_choice = input()
        if list(search_type_choices.keys()).__contains__(user_search_type_choice) == True:
            print("Please enter search query ")
            user_search_query = input()
            inital_search_query = youtube_api_handle.search().list(part='snippet',q=user_search_query,
                                                                   type=search_type_choices[
                                                                       user_search_type_choice],maxResults=25)

            search_result_data = inital_search_query.execute()
            parsed_search_data = extract_content_data(search_result_data,'search_results')

            # remove later
            next_page_token = search_result_data['nextPageToken']

            # add message to print messages array
            print_messages = []
            print_messages.append('Location://Menu//Search')
            print_messages.append('Search Results')
            print_messages.append("--------------------------")

            # Setting up api to sent to while loop
            api_sub = youtube_api_handle.search()
            api_args = {'part':'snippet','q':user_search_query,'type':search_type_choices[user_search_type_choice],'maxResults':25}
            test_loop = Menu_Loop(parsed_search_data,next_page_token,print_messages,api_sub,api_args)
            result_type = search_type_choices[user_search_type_choice]

            # last argument of start_loop message must be True
            test_loop.start_loop(youtube_api_handle,'search_results',None,True)

        if user_search_type_choice == 'b':
               print("going to previous menu or ending script")
               break


def video_menu_loop(youtube_api_handle,video_id):
    base_video_url =" https://www.youtube.com/watch?v="
    video_query = youtube_api_handle.videos().list(part='snippet,statistics',id=video_id)
    video_data = video_query.execute()
    parsed_data = extract_content_data(video_data,'video_data')
    video_title = list(parsed_data.keys())[0]
    description = parsed_data[video_title].pop('description')
    thumb_url = parsed_data[video_title].pop('thumbnail')

    # used to remove none value
    none_video_id = parsed_data[video_title].pop('id')
    
    # important for later when I create channel menu
    channel_id = parsed_data[video_title].pop('channelId')

    # grabbing channel title
    channel_query = youtube_api_handle.channels().list(part='snippet',id=channel_id)
    channel_data = channel_query.execute()
    parsed_channel_data = extract_content_data(channel_data)

    # important for later when I create channel menu
    channel_title = list(parsed_channel_data.keys())[0]

    ################################################
    while True:

        terminal_size = shutil.get_terminal_size().columns
        print("---------------------------------------------")
        print("Location://Video-Menu")
        title_string = 'Title:'+video_title
        print(title_string)
        channel_string = 'Channel:'+channel_title
        print(channel_string)
        inner_dict = parsed_data[video_title]

        for key in inner_dict.keys():
            combined_message = key+": "+inner_dict[key]
            print(combined_message)

        print("Type [s] to see video thumbnail")
        print("Type [p] to play video")
        print("Type [b] to go back")
        user_input = input()

        if user_input == 'p':
            video_command = 'vlc '+base_video_url+video_id
            os.system(video_command)
            continue

        if user_input == 's':
            req = urllib.request.urlopen(thumb_url)
            data = req.read()
            main = tk.Tk()
            title_lab = tk.Label(main,text="Title: "+video_title)
            image = PIL.Image.open(io.BytesIO(data))
            image_item = PIL.ImageTk.PhotoImage(image)
            image_label = tk.Label(main,image=image_item)
            title_lab.pack(side='top')
            image_label.pack(side='top')
            main.mainloop()

        if user_input == 'b':
            print("------------------------------")
            print('going to previous menu or ending script')
            break

        else:
            if user_input!='s':
                print("------------------------")
                print("please input valid option")

        
def playlist_menu_loop(playlist_title,playlist_id,youtube_api_handle):
    playlist_items_query = youtube_api_handle.playlistItems().list(part='snippet',
                                                            playlistId=playlist_id,
                                                            maxResults=25)
    playlist_video_data = playlist_items_query.execute()

    # grabbing playlist channel title
    playlist_channel_query = youtube_api_handle.playlists().list(part='snippet',id=playlist_id,
                                                                 maxResults=1)
    playlist_channel_data = playlist_channel_query.execute()
    parsed_playlist_channel_data = extract_content_data(playlist_channel_data,'playlist',dict_key='id')
    playlist_channel_id = parsed_playlist_channel_data[playlist_id]['channel_id']
    channel_query = youtube_api_handle.channels().list(part='snippet',id=playlist_channel_id)
    channel_data = channel_query.execute()
    parsed_channel_data = extract_content_data(channel_data,'channel')
    channel_keys = list(parsed_channel_data.keys())

    # important information for the future
    playlist_channel_title = channel_keys[0]
    playlist_channel_id = parsed_channel_data[channel_keys[0]]['id']
    parsed_video_data = extract_content_data(playlist_video_data,'playlist_item')

    # adding messages to print messages array
    print_messages = []
    print_messages.append('Location://Playlist//Menu')
    print_messages.append('Channel:'+playlist_channel_title)
    print_messages.append('Playlist: '+playlist_title)

    try:
        next_page_token = playlist_video_data['nextPageToken']
    except KeyError:
        next_page_token = None

    api_stub = youtube_api_handle.playlistItems()
    api_args = {'part':'snippet','playlistId':playlist_id,'maxResults':25}
    test_loop = Menu_Loop(parsed_video_data,next_page_token,print_messages,api_stub,api_args)
    test_loop.start_loop(youtube_api_handle,'playlist_item','video')

# use ** to pass dictionary as paramaters and values
# check for and handle TypeError


class Menu_Loop:

    def __init__(self,parsed_inital_data,next_page_token,print_messages,youtube_api_object,youtube_api_args):
        self.youtube_api = youtube_api_object,
        self.inital_data = parsed_inital_data,
        self.youtube_query_args = youtube_api_args
        self.page_token = next_page_token
        self.print_messages = print_messages

        # class specific values
        self.current_page_index = 0
        self.data_store = {}
        self.next_page_token_store = {}
        # setting inital values
        self.data_store[self.current_page_index] = parsed_inital_data
        self.next_page_token_store[self.current_page_index+1] = self.page_token
        self.current_next_page_token = self.page_token

    # transition_to -> playlist_menu:  playlist_title,playlist_id, youtube_api_handle
    # transition_to -> video_menu :  video_id, youtube_api
    # transition_to -> channel_menu: channel_id, youtube_api
    # standard format for data
    # id, title, api
    # tranistions
    # -> playlists -> videos --> videos menu to play

    def start_loop(self,youtube_api,parser_functions_type,transition_to,search_loop=False):

        while True:
            terminal_size = shutil.get_terminal_size().columns

            for message in self.print_messages:
                print(message)
            
            # Adding message to print_messages array
            static_messages = []
            static_messages.append("------------------------------")
            static_messages.append("enter [b] to go back")
            static_messages.append('enter [n] to go to the next page of items')
            static_messages.append('enter [p] to go to the previous page of items')
            static_messages.append("--------------------------------------")
            static_messages.append(" Enter an item's index to select it")
            static_messages.append("------------------------------------")

            # printing out messages
            for message in static_messages:
                print(message)

            item_index = (self.current_page_index*25)+1

            for item in self.data_store[self.current_page_index].keys():

                if search_loop == False:
                    combined_string = str(item_index)+": "+item
                    print(combined_string)

                if search_loop == True:
                    content_type = self.data_store[self.current_page_index][item]['type']
                    combined_string = '('+content_type+')'+str(item_index)+": "+item
                    print(combined_string)
                    
                item_index+=1

            print("-------------------------------------------")
            user_choice = input()

            if user_choice !='b':
                if user_choice == 'n':
                    if self.current_next_page_token!=None:

                        # adding next page token
                        self.youtube_query_args['pageToken'] = self.current_next_page_token
                        api_query_data = self.youtube_api[0].list(**self.youtube_query_args).execute()
                        parsed_next_page_data = extract_content_data(api_query_data,parser_functions_type)

                        # important for adding new data
                        self.data_store[self.current_page_index+1] = parsed_next_page_data
                        self.current_page_index+=1

                        try:
                            self.current_next_page_token = api_query_data['nextPageToken']
                            self.next_page_token_store[self.current_page_index+1] = self.current_next_page_token

                        except KeyError:
                            self.current_next_page_token = None
                    
                    else:
                        print("There are no more pages")
                    
                if user_choice == 'p':
                    if self.current_page_index!=0:
                        if self.current_page_index - 1 !=0:
                            self.current_next_page_token = self.next_page_token_store[self.current_page_index-1]

                        self.current_page_index-=1

                    else:
                        print("You are alread on the first page")

                if user_choice!='b':

                    if user_choice!='p':

                        if user_choice!='n':

                            try:
                                chosen_index = int(user_choice) - 1
                                chosen_index = chosen_index - (self.current_page_index*25)
                                keys = list(self.data_store[self.current_page_index].keys())
                                data = self.data_store[self.current_page_index][keys[chosen_index]]
                            
                                # Formating data to move to new menu
                                packaged_data = {}
                                packaged_data['title'] = keys[chosen_index]
                                packaged_data['id'] = data['id']

                                if search_loop == True:
                                    data_type = data['type']
                                    transition_to = data_type

                                if transition_to == 'video':
                                    video_menu_loop(youtube_api,packaged_data['id'])

                                if transition_to == 'playlist':
                                    playlist_menu_loop(packaged_data['title'],packaged_data['id'],youtube_api)

                                if transition_to == 'channel':
                                    channel_menu_loop(youtube_api,packaged_data['id'])
                                   
                            except ValueError:
                               print("Please enter a number".center(terminal_size))

                            except IndexError:
                                print("Please enter a index in the correct range")

            else:
                print("Either going to previous menu or ending script")
                break


                

               




    

    
