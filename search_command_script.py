import menu_loops
from menu_loops import *

# grabbing credentials
cred = gen_creds()
youtube_api = build('youtube','v3',credentials=cred)
search_menu_loop(youtube_api)