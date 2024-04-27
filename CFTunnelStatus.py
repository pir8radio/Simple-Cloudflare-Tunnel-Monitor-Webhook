from time import sleep
from sys import stdout
import json
import requests
import datetime


############# Settings #############
token = " " #CF Token
email = " " #CF Email
account_id = " " #CF Account ID
cf_tunnel_id = " " #CF Tunnel ID To Monitor
statpage_url = "https://api.instatus.com/v3/integrations/webhook/<YOUR WEBHOOK CODE>"
sleep_time = 60 # In seconds between checks
recheck_time = 30 # In seconds recheck after error
statdowndata = { "trigger": "down", }
statupdata = { "trigger": "up", }
####################################


url = "https://api.cloudflare.com/client/v4/accounts/" + account_id + "/cfd_tunnel?is_deleted=false"
headers = {"X-Auth-Email":email, "Authorization": "Bearer " + token}   
alert_sent = False
ok_sent = False

def check_tunnels_status():
    try:
        global alert_sent
        global ok_sent
        while True:
            now = datetime.datetime.now()
            response = requests.get(url,headers = headers)
            if response.status_code == 200:
                for t in response.json()["result"]:
                    TunnelId = str(t["id"])
                    CurrentTunnelState = t["status"]
                    print(" ", end='\r')
                    print(TunnelId + " " + CurrentTunnelState + " " + now.strftime("%m-%d-%Y %H:%M:%S"))
                    if TunnelId == cf_tunnel_id and CurrentTunnelState != "healthy":
                        if not alert_sent:
                            requests.post(statpage_url, data=json.dumps(statdowndata), headers={'Content-Type': 'application/json'})
                            alert_sent = True
                            print("Tunnel DOWN and is in the " + CurrentTunnelState + " state - status page updated " + now.strftime("%m-%d-%Y %H:%M:%S"))
                            sleep(2)
                    elif TunnelId == cf_tunnel_id:
                        alert_sent = False
                        if not ok_sent:
                            requests.post(statpage_url, data=json.dumps(statupdata), headers={'Content-Type': 'application/json'})
                            ok_sent = True
                            print("Tunnel UP and is in the " + CurrentTunnelState + " state - status page updated " + now.strftime("%m-%d-%Y %H:%M:%S"))
            else:
                print(f"Cloudflare API returned error {str(response.status_code)} " + now.strftime("%m-%d-%Y %H:%M:%S"))
                
            print(" ", end='\r')
            for remaining in range(sleep_time, 0, -1):
                stdout.write("\r")
                stdout.write("Sleeping for {:2d} seconds.".format(remaining))
                stdout.flush()
                sleep(1)
    except:
        print(" ", end='\r')
        for remaining in range(recheck_time, 0, -1):
            stdout.write("\r")
            stdout.write("Restarting in {:2d} seconds due to an error.".format(remaining))
            stdout.flush()
            sleep(1)
        check_tunnels_status()

if __name__ == "__main__":
    print("Tunnel monitor starting...")
    check_tunnels_status()
