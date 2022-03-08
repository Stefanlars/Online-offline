import requests
import json
import insightly_api
headers = {
    'Content-type': 'application/json',
    'cookie': "_y=d6a0f273-0e6c-48cb-bc3b-230b2bed340d; _shopify_y=d6a0f273-0e6c-48cb-bc3b-230b2bed340d; _ga=GA1.2.1527245938.1642694847; _fbp=fb.1.1642694847817.1147303733; csrftoken=TjCNUKA0pDI4EE7aj494CXGXuCUoF29vhimepkm0KAeqRKm8d5DsFzA8wdMAa1i3; sessionid=42uwhy4395zahquqviivmb0c8s708c4n",
    'origin': 'https://dashboard.nebra.com',
    'referer': 'https://dashboard.nebra.com/devices',
    'x-csrftoken': 'inp3ArxT2aoeb636oqvZ2Ix0RmDtrjitGm9u51jTn7UAoci4irZn5krbTXvFWir1'
  }

def check_nebra_dashboard():
  url = "https://dashboard.nebra.com/api/v0.1/device/device_list/"

  payload={}

  response = requests.request("POST", url, headers=headers, data=payload)

  nebra_data = response.json()


  #TODO: create check to make sure nebra devices are online

  f = open('node_info.json')


  sussy_nodes = json.load(f)

  nebra_list = nebra_data
  nebra_offline_list = []

  print(sussy_nodes)

  for item in sussy_nodes:
    name = f"{item['info']['name']}"
    for nebra in nebra_list:
      if nebra["name"].lower() == name.replace('-',' ').lower():
        nebra_parsed = {}
        nebra_parsed['info'] = {
          'opp_id':item['info']['opp_id'], 'nebra_status':nebra['balena_status'], 'name': nebra['name']
        }
        nebra_offline_list.append(nebra_parsed)

      else:
        pass

  for item in nebra_offline_list:
    if item['info']['nebra_status'] == True:
      print(f"{item['info']['name']} is online")
    if item['info']['nebra_status'] == False:
      insightly_api.put_opp_fields(opp_id=item['info']['opp_id'], node_status='Offline')
      insightly_api.del_tag(tag_name='Online',oppor_id=item['info']['opp_id'])
      insightly_api.post_tag(tag_name='Offline', oppor_id = item['info']['opp_id'])
      insightly_api.add_note(opp_id=item['info']['opp_id'], node_status='Offline', node_type='nebra')
      print(f"!!!{item['info']['name']} is offline and is updated in insightly!!!")
    if item['info']['nebra_status'] == None:
      print(f"{item['info']['name']}'s status is undetermined")


  for item in nebra_offline_list:
    for node in sussy_nodes:
      if item['info']['opp_id'] == node['info']['opp_id']:
        sussy_nodes.remove(node)
      else: pass

  return sussy_nodes

def offline_nebra_check(node_list):
  url = "https://dashboard.nebra.com/api/v0.1/device/device_list/"

  payload = {}

  response = requests.request("POST", url, headers=headers, data=payload)

  nebra_data = response.json()

  nebra_list = nebra_data
  nebra_offline_list = []

  for item in node_list:
    name = f"{item['info']['name']}"
    for nebra in nebra_list:
      if nebra["name"].lower() == name.replace('-',' ').lower():
        nebra_parsed = {}
        nebra_parsed['info'] = {
          'opp_id':item['info']['opp_id'], 'nebra_status':nebra['balena_status'], 'name': nebra['name']
        }
        nebra_offline_list.append(nebra_parsed)

      else:
        pass

  for item in nebra_offline_list:
    if item['info']['nebra_status'] == True:
      print(f"{item['info']['name']} is online and updated in insightly")
      insightly_api.put_opp_fields(opp_id=item['info']['opp_id'], node_status='Online')
      insightly_api.del_tag(tag_name='Offline', oppor_id=item['info']['opp_id'])
      insightly_api.post_tag(tag_name='Online', oppor_id=item['info']['opp_id'])
      insightly_api.add_note(opp_id=item['info']['opp_id'], node_status='Online', node_type='nebra')
    if item['info']['nebra_status'] == False:
      print(f"{item['info']['name']} is offline and unchanged in explorer")
    if item['info']['nebra_status'] == None:
      print(f"{item['info']['name']}'s status is undetermined")
