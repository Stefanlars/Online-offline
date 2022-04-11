import requests
import json
from datetime import datetime
#function for deleting tags in an opportunity

def del_tag(tag_name, oppor_id,):

  url = f"https://api.na1.insightly.com/v3.1/Opportunities/{oppor_id}/Tags"

  payload = json.dumps({
    "TAG_NAME": f"{tag_name}"
  })
  headers = {
    'Authorization': '*****************************',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
  }

  response = requests.request(f"DELETE", url, headers=headers, data=payload)

  return response
#function for posting tags in an opportunity

def post_tag(tag_name, oppor_id):
  url = f"https://api.na1.insightly.com/v3.1/Opportunities/{oppor_id}/Tags"

  payload = json.dumps({
    "TAG_NAME": f"{tag_name}"
  })
  headers = {
    'Authorization': '*****************************',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
  }

  response = requests.request(f"POST", url, headers=headers, data=payload)


  return response


def add_note(opp_id, node_status, node_type):
  url = f"https://api.na1.insightly.com/v3.1/Opportunities/{opp_id}/Notes"
  if node_type == 'nebra':
    payload = json.dumps({
    "TITLE":f"Node Status:{node_status}",
    "BODY":f"Node {node_status} in Nebra Portal: {datetime.now()}"
    })
  else:
    payload = json.dumps({
      "TITLE": f"Node Status:{node_status}",
      "BODY": f"Node {node_status} in explorer: {datetime.now()}"
    })
  headers={
    'Authorization': '**************************************',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
def put_opp_fields(opp_id,node_status):
  url = "https://api.na1.insightly.com/v3.1/Opportunities"
  id_int = int(opp_id)
  payload = json.dumps({
    "OPPORTUNITY_ID": id_int,
    "CUSTOMFIELDS": [
      {
        "FIELD_NAME": "Node_Status__c",
        "FIELD_VALUE": node_status,
        "CUSTOM_FIELD_ID": "Node_Status__c"
      }
    ]
  })
  headers = {
    'Authorization': '************************************',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
  }

  response = requests.request("PUT", url, headers=headers, data=payload)





