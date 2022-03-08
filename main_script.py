import re
import time
import requests
import json
import insightly_api
import nebra_portal
import peerbook

#TODO: IMPORTANT: before running main script make sure to re-input the cookies as they change and the script will break
#if not changed in hotspotty_api.py
my_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization' : 'Basic {{{{{{{insert api key}}}}}}}}}}', 'Accept-Encoding': 'gzip','Cookie':
    'AWSALB=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjU1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; AWSALBCORS=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjU1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; snaptid=sac1prdc01wut07',
    'Accept':'*/*','Connection':'keep-alive'}

def check_hotspot(helium_url, hotspot_name):
    id_re = re.compile('(https://explorer.helium.com/hotspots/)(.+)')
    helium_id = f"{id_re.search(helium_url).group(2)}"
    helium_r= requests.get(f"https://api.helium.io/v1/hotspots/{helium_id}")
    time.sleep(1)
    hotspot_data = helium_r.json()
    if hotspot_data['data']['status']['online'] == 'offline':
        return 'offline'
    if hotspot_data['data']['status']['online'] == 'online':
        return 'online'



r = requests.get("https://api.insightly.com/v3.1/Opportunities/SearchByTag?tagName=Offline&brief=false&top=300&count_total=false", headers=my_headers)

r2 = requests.get("https://api.insightly.com/v3.1/Opportunities/SearchByTag?tagName=Online&brief=false&top=300&count_total=false", headers=my_headers)

Offline_nodes = r.json()

Online_nodes = r2.json()

online_list = []
offline_list = []
changed_list_online = []
changed_list_offline= []
offline_node_list = []
offline_nebra = []
num_offline = 0
num_online = 0
for item in Offline_nodes: num_offline = num_offline+1
for item in Online_nodes: num_online = num_online+1



print(f'{num_online} Online\n\n{num_offline} Offline')

print("\nNow verifying Offline nodes.....")
#TODO: offline node update in insightly
for item in Offline_nodes:
    hotspot = item["OPPORTUNITY_NAME"]
    OPP_ID = item["OPPORTUNITY_ID"]
    print(f"{hotspot} is now being verified")
    hardware = ''
    for field in item['CUSTOMFIELDS']:
        if field['FIELD_NAME']== 'Nebra Outdoor Unit':
            hardware = 'Nebra'
            node_dict1 = {}
            node_dict1['info'] = {'name': hotspot, 'opp_id': OPP_ID, 'helium_id': ''}
            offline_nebra.append(node_dict1)
        else:
            pass
    for field in item['CUSTOMFIELDS']:
        if field['FIELD_NAME']== 'Explorer_Link__c':
            hotspot_url=field['FIELD_VALUE']
            time.sleep(3)


            try:
                NODE_STATUS=check_hotspot(hotspot_url,hotspot)
            except:
                NODE_STATUS = 'offline'
#TODO: 2/22/2022: IN PROGRESS: adding nebra function so that nebras are online and up to date
            if NODE_STATUS == 'online':
                changed_list_online.append(f'{hotspot} is now online and updated in hotspotty')
                insightly_api.put_opp_fields(opp_id=OPP_ID, node_status=NODE_STATUS)
                insightly_api.del_tag(oppor_id=OPP_ID, tag_name='Offline')
                insightly_api.post_tag(oppor_id=OPP_ID, tag_name='Online')
                insightly_api.add_note(opp_id=OPP_ID, node_status=NODE_STATUS, node_type='rak')

            if NODE_STATUS == 'offline':
                offline_list.append(f'{hotspot}')


        else:
            pass
#
# #TODO: online node update in insightly
print("\nNow verifying online nodes.....")
for item in Online_nodes:
    hotspot = item["OPPORTUNITY_NAME"]
    opp_id = item["OPPORTUNITY_ID"]
    print(f"{hotspot} is now being verified")
    for field in item['CUSTOMFIELDS']:
        if field['FIELD_NAME']== 'Explorer_Link__c':
            hotspot_url=field['FIELD_VALUE']
            time.sleep(3)
            try:
                node_status=check_hotspot(hotspot_url,hotspot)
            except:
                node_status = 'online'

            if node_status == 'online':
                online_list.append(f'{hotspot}')
            if node_status == 'offline':
                changed_list_offline.append(f'{hotspot}')
                id_re = re.compile('(https://explorer.helium.com/hotspots/)(.+)')
                helium_id = f"{id_re.search(hotspot_url).group(2)}"
                node_dict = {}
                node_dict['info'] = {'name':hotspot,'opp_id':opp_id,'helium_id':helium_id}
                offline_node_list.append(node_dict)

        else:
            pass


print(changed_list_online)


# print(f'\n\n{changed_list_offline}')

f = open('node_info.json', 'w')
f.seek(0)
f.write(json.dumps(offline_node_list))
f.close()

hotspotty_nodes = nebra_portal.check_nebra_dashboard()

# print(hotspotty_nodes)

peerbook.check_node_peerbook(node_list=hotspotty_nodes)

# print(offline_nebra)

# nebra_portal.offline_nebra_check(offline_nebra)

print('all nodes have been succesfully verified')
