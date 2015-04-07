from retry import *
import requests
import json
from datetime import datetime, timedelta
import re
from collections import defaultdict

REST_API_URL="https://api.flowdock.com/"
TIME_FORMAT="%Y-%m-%dT%H:%M:%S.%fZ"

class Connection():
    """ A class to manage connecting to flowdock"""

    def __init__(self, token):
        self.token=token
        self.decoder=json.JSONDecoder()
        self.threads=defaultdict(dict)

    def MakeURL(self,organisation,flow,service):
        return "{base}/flows/{organisation}/{flow}/{service}".format(
                base=REST_API_URL,
                organisation=organisation,
                flow=flow,
                service=service)

    @retry(requests.exceptions.ConnectionError, tries=4, delay=3, backoff=2)
    def Request(self,url,token=None,**kwargs):
        r=requests.get(url, auth=(self.token if not token else token ,""),params=kwargs); 
        return r.json()

    def GetMessages(self,date_offset,organisation,flow):
        """ Get all the flows since date """
        # prepare the target URL
        url=self.MakeURL(organisation,flow,"messages")

        # What's the date we want to stop at?
        stop_time=datetime.now() - timedelta(hours=date_offset)
        #print(stop_time)

        # Pull messages until we've reached the requested time offset
        reachedDesiredDate=False
        last_id=-1
        new_messages={}
        thread_re=re.compile(r"influx:(\d+)")
        while(not reachedDesiredDate):
            # Request a set of messages
            params={'limit':100}
            if last_id != -1: params['until_id']=last_id
            objects=self.Request(url,**params)

            # Reverse iterate  to check if we've  got all that we  need to reach
            # our requested time limit
            for obj in reversed(objects):
                created_at=datetime.strptime(obj["created_at"],TIME_FORMAT)
                last_id=int(obj["id"])
                if created_at < stop_time:
                    reachedDesiredDate=True
                    break
                # Valid new message so keep it
                new_messages[obj["id"]]=(obj)
                self.GetThreadHeads([ thread_re.match(tag).group(1) for tag in obj["tags"] if thread_re.match(tag) ],
                organisation,flow)
        #print(obj["tags"])
        return new_messages

    def GetUsers(self,organisation,flow):
        """ Get all users for a flow """
        # prepare the target URL
        url=self.MakeURL(organisation,flow,"users")

        # get the users list
        objs= self.Request(url)
        return dict(zip( [ obj['id'] for obj in objs], objs ))

    def GetThreadHeads(self,threads,organisation,flow):
        url=self.MakeURL(organisation,flow,"messages/")
        for thread in threads:
            if thread in self.threads[organisation+"/"+flow].keys(): continue
            obj=self.Request(url+str(thread))
            self.threads[organisation+"/"+flow][thread]=obj

    def GetThreads(self,organisation,flow):
        return self.threads[organisation+"/"+flow]

    def GetFlows(self):
        url=REST_API_URL+"/flows/all"
        objs= self.Request(url,users=1)
        for obj in objs: 
                if obj['access_mode']!="organization":
                        objs.remove(obj)
        return objs
