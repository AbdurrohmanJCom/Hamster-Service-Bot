# import json
# import requests
# from datetime import datetime

# def extract_event_info(event):
#     event_id = event['event_id']
#     action_type = event['actions'][0]['type']
#     comment = event['actions'][0]['simple_preview']['description'] if 'simple_preview' in event['actions'][0] else ''
#     jetton_units = event['actions'][0]['TonTransfer']['amount'] if 'TonTransfer' in event['actions'][0] else None
#     jetton_type = event['actions'][0]['simple_preview']['value'] if 'simple_preview' in event['actions'][0] else ''
#     date_time = datetime.fromtimestamp(event['timestamp'])
    
#     return {
#         'event_id': event_id,
#         'action_type': action_type,
#         'comment': comment,
#         'jetton_units': jetton_units,
#         'jetton_type': jetton_type,
#         'date_time': date_time
#     }

# def new_trans(wallet_address):
#     data = requests.get(f'https://tonapi.io/v2/accounts/{wallet_address}/events?limit=19').json()
#     events = data.get('events', [])
    
#     extracted_events = [extract_event_info(event) for event in events]
    
#     return extracted_events

# wallet_address = "UQDf8qesxr2WNO29i-k4Iu6HdbB3230ussI1HIUNu06viDzl"
# events = new_trans(wallet_address)
# for event in events:
#     print(event)

import json
import requests
from datetime import datetime

def new_trans(wallet_address):
    data = requests.get(f'https://tonapi.io/v2/accounts/{wallet_address}/events?limit=100').json()
    
    events_data = []

    for event in data['events']:
        for action in event['actions']:
            event_id = event['event_id']
            action_type = action['type']
            comment = action.get('TonTransfer', {}).get('comment', 'N/A')
            jetton_units = action.get('TonTransfer', {}).get('amount', 'N/A')
            jetton_type = 'TON' if action_type == 'TonTransfer' else 'Unknown'
            date_time = datetime.utcfromtimestamp(event['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            
            event_info = {
                'event_id': event_id,
                'action_type': action_type,
                'comment': comment,
                'jetton_units': jetton_units,
                'jetton_type': jetton_type,
                'date_time': date_time
            }
            
            events_data.append(event_info)
    
    return events_data

wallet_address = "UQDf8qesxr2WNO29i-k4Iu6HdbB3230ussI1HIUNu06viDzl"
transactions = new_trans(wallet_address)

for tx in transactions:
    print(tx)
