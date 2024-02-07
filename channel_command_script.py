import menu_loops
from menu_loops import *

# grabbing credentials
cred = gen_creds()
youtube_api = build('youtube','v3',credentials=cred)

# Print messages for the loop
print_messages = [ 'Location://Subscription//Channels','----------------------------------' ]

# running loop
subscriptions_menu_loop(youtube_api,print_messages)
