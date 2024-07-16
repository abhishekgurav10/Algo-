
# seon details 
consumer_key=
consumer_secret=
mobilenumber=
password=
import neo_api_client 
from neo_api_client import NeoAPI

from neo_api_client import NeoAPI

def on_message(message):
    print('[Res]: ', message)


def on_error(message):
    result = message
    print('[OnError]: ', result)
    

#the session initializes when the following constructor is called
client = NeoAPI(consumer_key=consumer_key,consumer_secret=consumer_secret,environment="PROD")
client.on_message = on_message  # called when message is received from websocket
client.on_error = on_error  # called when any error or exception occurs in code or websocket
client.on_close = None  # called when websocket connection is closed
client.on_open = None 
# client.on_close = None  # called when websocket connection is closed
# client.on_open = None

client.login(mobilenumber=mobilenumber, password=password) 
MPIN =  # 6 digit my MPIN
client.session_2fa(OTP=MPIN)
