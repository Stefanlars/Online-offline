import paramiko
import re
import insightly_api
from paramiko import SSHClient
import requests


#TODO: IMPORTANT: If node deosn't show up on peerbook, it is offline on blockchain. Create simple ssh script to check
# blockchain if no IP address is found in helium api.


def peer_book_ping(helium_id):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='REDACTED', port=22, username='REDACTED', password='REDACTED')

    client.exec_command(
        f"docker exec miner miner peer ping /p2p/{helium_id}"
    )
    stdin, stdout, stderr = client.exec_command(
        f"docker exec miner miner peer book /p2p/{helium_id}"
    )

    peer_book_look = (f"{stdout.readlines()}")

    # print(peer_book_look)

    list_addrss_re = re.search(
        '/p2p/(.{40,60})/p2p-circuit/p2p/.{10,70}\||(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
        peer_book_look
    )
    # group1_type = type(list_addrss_re.group(1))
    # group2_type = type(list_addrss_re.group(2))

    try:
        list_address = list_addrss_re.group(1)
        stdin, stdout, stderr = client.exec_command(f"docker exec miner miner peer ping /p2p/{list_address}")
        ping_attempt = f"{stdout.readlines()}"
        ping_re = re.search('( successfully)', ping_attempt)
        ping_re_type = type(ping_re)
        if ping_re_type != None:
            node_status = "Successfully pinged through blockchain"
        else:
            node_status = "Offline"

    except AttributeError:
        try:
            list_address = list_addrss_re.group(2)
            stdin, stdout, stderr = client.exec_command(f"telnet {list_address} 44158")
            connect_attempt = f"{stdout.readlines()}"
            client.exec_command("^C")
            connect_re = re.search('(Connected)', connect_attempt)
            connect_re_type = type(connect_re)
            if connect_re_type != None:
                node_status = "successfully telnetted into device"
            else:
                node_status = "Offline"
        except AttributeError:
            print("ERROR: Unable to fetch listening address")
            node_status = "N/A"

    client.close()

    return node_status


def check_node_peerbook(node_list):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='137.184.151.218', port=22, username='root', password='WidePutin2015s')

    for item in node_list:
        helium_id = item['info']['helium_id']
        opp_id = item['info']['opp_id']
        name = item['info']['name']
        r = requests.request(
            'GET', url=f'https://api.helium.io/v1/hotspots/{helium_id}'
        )
        helium_data = f"{r.json()}"
        helium_re = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/tcp/(\d{5})', helium_data)
        try:
            ip_address = helium_re.group(1)
            port = helium_re.group(2)
            stdin, stdout, stderr = client.exec_command(f"telnet {ip_address} {port}")
            telnet_response = f'{stdout.readlines()}'
            # print(telnet_response)
            client.exec_command("^C")
            telnet_re = re.search('(Connected)', telnet_response)

            if telnet_re.group(1) == "Connected":
                    print(f"{name} is online and unchanged")
        except AttributeError:
            print(f"Unable to connect to {name} via ip address, trying p2p network...")
            client.exec_command(
                f"docker exec miner miner peer ping /p2p/{helium_id}"
            )
            stdin, stdout, stderr = client.exec_command(
                f"docker exec miner miner peer book /p2p/{helium_id}"
            )

            peer_book_look = (f"{stdout.readlines()}")
            peer_book_fail_re = re.search("( failed)", peer_book_look)
            try:
                if peer_book_fail_re.group(1) == ' failed':
                    insightly_api.put_opp_fields(opp_id=opp_id, node_status='offline')
                    insightly_api.del_tag(oppor_id=opp_id, tag_name='Online')
                    insightly_api.post_tag(oppor_id=opp_id, tag_name='Offline')
                    insightly_api.add_note(opp_id=opp_id, node_status='offline', node_type='rak')
                    print(f"\n!!!!{name} is offline and changed in insightly!!!!\n")
            except AttributeError:
                print(f"{name} is online and unchanged in insightly")
