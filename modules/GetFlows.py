import requests
import json
import datetime

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

    def GetFlow(self,date_offset,organisation,flow):
        """ Get all the flows since date """
        # prepare the target URL
        url=self.MakeURL(organisation,flow,"messages")

        # What's the date we want to stop at?
        stop_time=datetime.datetime.now() - datetime.timedelta(hours=date_offset)
        print(stop_time)

        # Pull messages until we've reached the requested time offset
        reachedDesiredDate=False
        last_id=-1
        while(not reachedDesiredDate):
            params={'limit':100}
            if last_id != -1: params['until_id']=last_id
            r=requests.get(url, auth=(self.token,""),params=params); 
            objects=r.json()
            for obj in reversed(objects):
                #print(obj.keys())
                created_at=datetime.datetime.strptime(obj["created_at"],"%Y-%m-%dT%H:%M:%S.%fZ")
                last_id=int(obj["id"])
                print(str(created_at),obj["created_at"], str(stop_time), created_at < stop_time)
                if created_at < stop_time:
                    reachedDesiredDate=True
                    break
                print(obj["user"], obj["content"])
            #reachedDesiredDate=True
