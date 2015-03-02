import BaseClasses
from collections import defaultdict
import operator
import re
import string

class TallyTags(BaseClasses.BaseProduct):
    def __init__(self):
        BaseClasses.BaseProduct.__init__(self)
        self.tags     = defaultdict(list)
        self.threads  = defaultdict(list)
        self.mentions = defaultdict(list)

    def ProcessData(self, flowData):
        mention_re=re.compile(r":user:(\d+)")
        thread_re=re.compile(r"influx:(\d+)")
        unread_re=re.compile(r":unread:(\d+)")

        # tally up all tags
        tags={}
        for flow, data in flowData.iteritems():
            tag_count=defaultdict(int)
            for iid, msg in data.messages.iteritems():
                for tag in msg['tags']:
                    tag_count[tag] += 1
            tags[flow]=sorted(tag_count.items(),
                              reverse=True,
                              key=operator.itemgetter(1))

            # Now separate tags, mentions and threads.
            # Ought to do this in the last loop for speed
            print(type(tags),tags)
            for tag, count in tags[flow]:
                if mention_re.match(tag):
                    user_id=int(mention_re.match(tag).group(1))
                    print(user_id)
                    user= flowData[flow].users[user_id]
                    print(user['id'],user['nick'])
                    self.mentions[flow].append(("@"+user['nick'],count) )
                elif thread_re.match(tag):
                    print(flowData[flow].messages.keys())
                    thread=flowData[flow].messages[thread_re.match(tag).group(1)]
                    self.threads[flow].append( 
                            (thread,count) )
                elif tag == ":thread": continue
                elif unread_re.match(tag): continue
                else :
                    self.tags[flow].append( (tag,count) )

class SimpleSummaryData(BaseClasses.BaseProduct):
    def ProcessData(self, flowData):
        self.n_messages={}
        self.n_users={}
        for flow, data in flowData.iteritems():
            self.n_messages[flow]=len(data.messages)
            self.n_users[flow]=len(data.users)


class LargestThread(BaseClasses.BaseProduct):
    def ProcessData(self, flowData):
        pass
