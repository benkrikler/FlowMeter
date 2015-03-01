import requests
import json

REST_API_URL="https://api.flowdock.com/"

#: r=requests.get("https://api.flowdock.com/flows/comet/icedust-in-general/messages",auth=("<private-token>","")); r.json()

class Connection():
    """ A class to manage connecting to flowdock"""

    def __init__(self, token):
        self.token=token
        self.decoder=json.JSONDecoder()

    def MakeURL(self,organisation,flow,service):
        return "{base}/flows/{organisation}/{flow}/{service}".format(
                base=REST_API_URL,
                organisation=organisation,
                flow=flow,
                service=service)

    def GetFlow(self,date,organisation,flow):
        """ Get all the flows since date """
        # prepare the target URL
        url=self.MakeURL(organisation,flow,"messages")
        r=requests.get(url, auth=(self.token,"")); 
        objects=r.json()
        for obj in objects:
            #print(obj.keys())
            print(obj["created_at"], obj["content"])
