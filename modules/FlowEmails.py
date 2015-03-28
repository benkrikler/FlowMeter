import BaseClasses
import string

class FlowEmails(BaseClasses.BaseProduct):
    def __init__(self):
        BaseClasses.BaseProduct.__init__(self)
        self.emails = {}
        self.join_urls = {}

    def ProcessData(self, flowData,config):
        """ Pick out the emails and urls to communicate to flowdock with """
        for flow, data in flowData.iteritems():
            self.emails[flow]=data.info['email']
            if 'join_url' in data.info:
                self.join_urls[flow]=data.info['join_url']
            else:
                self.join_urls[flow]="( no join URL available )"
