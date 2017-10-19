#!/usr/bin/python
import requests
import json
import yaml
import time
from slackclient import SlackClient

# read and set config values
with open('config.yaml', 'r') as stream:
    config = yaml.load(stream)

# Create SlackClient Object with API token   
sc = SlackClient(config['slack_bot_token'])
USER = config['slack_username']

# Set the alert temperature for each GPU
MAX_GPU_TEMP = config['gpu_alert_temp']

# Continue to loop script
while True:
    
    try:
        for miner in config['miner']:
            
            # construct url to reach claymore miner port
            miner_url = "http://{}:{}".format(miner['host_ip'],miner['port'])
            
            # parse and extract the GPU info from the response
            mine_info = requests.get(miner_url).text
            json_string = mine_info.split('\n')[1].split('<br><br>')[0]
            json_object = json.loads(json_string)
            result = json_object['result']
            gpus = result[6].split(";") # gpus info is at index 6 in the response
            
            # determine the number of GPUs in response
            # Each GPU will have a temperature and fan speed value
            num_of_cards = int((len(gpus) / 2))
                
            # blank dictionary to construct Mining and GPU info
            mining_rig = {}
            
            result_index = 0
            
            for i in range(0, num_of_cards):
                gpu_num = 'GPU(%s)' % i
                mining_rig[gpu_num] = {}
                mining_rig[gpu_num]['temp'] = gpus[result_index]
                mining_rig[gpu_num]['fanSpeed'] = gpus[result_index + 1]
                mining_rig.update(mining_rig)
                result_index = result_index + 2
            
            # parse through gpus to determine if any are above the MAX_GPU_TEMP
            for key, value in mining_rig.items():
                if int(value['temp']) >= MAX_GPU_TEMP:
                    # send message to Slack Bot
                    sc.api_call(
                    "chat.postMessage",
                    channel="@{}".format(USER),
                    text="{} {} is overheating! {}\u00b0 C".format(miner['name'],key,value['temp'])
                    )  
                    
    except Exception:
        print("Error Reaching Mining Rigs")
     
       
    time.sleep(60) # check gpu temps once a minute  