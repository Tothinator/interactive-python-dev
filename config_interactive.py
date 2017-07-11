''' Config File '''

# DO NOT CHANGE THESE VALUES OR THE BOT WILL BREAK
BEAM_URI = 'https://beam.pro/api/v1/'
AUTHTOKEN_URI = 'oauth/token'
USERSCURRENT_URI = 'users/current'
CHATSCID_URI = 'chats/{cid}'
INTERACIVE_URI = "interactive/{channel}/robot"
INTERACTIVEHOSTS_URI = 'interactive/hosts'

# THE SETTINGS BELOW CAN BE CHANGED
# This need to be the ID for the channel you wish to join
# https://beam.pro/api/v1/channels/channelname?fields=id
# CHANNELID = '694518'
CHANNELID = '149583'

# Project Version ID
VERSION_ID = '61923'

# Project Share ID
SHARE_ID = 'mqvw0jrp'

# Access Token
# I use a DB however you will need to change the get_access_token() function in helpers.py to return this token
ACCESS_TOKEN = 'Your Access Token'

# This is up to you to obtain. This can be done though
# Rest API. for more info https://dev.beam.pro/reference/oauth/index.html
# This will be pulled from the database

# Client ID, obtained from https://beam.pro/lab
# select OAUTH CLIENTS and copy ID
CLIENTID = 'Enter Client ID'


# enables/disables raw chat details as recieved from the server
# without the chat formatting
CHATDEBUG = False