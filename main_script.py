from api_funcs import *
from googleapiclient.discovery import build
import os
import json


user_data_path = ".//user_data//"

user_file = 'user.json'

credentials = gen_creds()

youtube_api = build('youtube','v3',credentials=credentials) 


if os.path.exists(user_data_path+user_file) == False:

    user_file = open(user_data_path+user_file,'w')

    init_user_data = {'channels':{}}

    json_data = json.dumps(init_user_data)

    user_file.write(json_data)

    user_file.close()

    print("Created user json file")



user_data_file = open(user_data_path+user_file)

json_user_data = json.load(user_data_file)


if len(json_user_data['channels']) == 0:

    subscription_query = youtube_api.subscriptions().list(part='snippet',mine=True,maxResults=50)

    subscription_data = subscription_query.execute()

    parsed_subscription_data = extract_content_data(subscription_data,'channel',dict_key='id')

    new_user_data = {'channels':{}}

    for key in parsed_subscription_data.keys():

        new_user_data['channels'][key] = parsed_subscription_data[key]


    update_file_handle = open(user_data_path+user_file,'w')

    converted_json_data = json.dumps(new_user_data)

    update_file_handle.write(converted_json_data)

    update_file_handle.close()


    print("Added user subscriptions")


else:

    # Checking to see if the user added any new subscriptions
    
    new_ids = check_for_subscription_update(youtube_api,user_data_path+user_file)

    if len(new_ids) == 0:

        print("No new subscriptions")

    else:

        print(new_ids) 

    
                                            


# main area of script



            



    

        

                

            

            

        

            

        

        

        
    

    

