import BaseClasses
from collections import defaultdict
import operator
import re
import string

class TagsFilter():
    def __init__(self):
        self.user_re=re.compile(r":user:(\d+)")
        self.skip_re=re.compile(r"influx:\d+|:unread:\d+|:thread")

    def Apply(self, taglist, user_map):
        cleaned_tags=set("")
        for tag in taglist:
            user=self.user_re.match(tag)
            if user:
                cleaned_tags.add("@"+user_map[int(user.group(1))]['nick'])
            elif not self.skip_re.match(tag):
                cleaned_tags.add(tag)
        return cleaned_tags

class TallyTags(BaseClasses.BaseProduct):
    def __init__(self):
        BaseClasses.BaseProduct.__init__(self)
        self.tags     = defaultdict(list)
        self.links     = defaultdict(list)
        self.files     = defaultdict(list)
        self.threads  = defaultdict(list,"")
        self.mentions = defaultdict(list)

    def ProcessData(self, flowData,config):
        mention_re=re.compile(r":user:(\d+)")
        everyone_re=re.compile(r":user:(team|everyone|everybody|all|anyone|anybody)")
        thread_re=re.compile(r"influx:(\d+)")
        unread_re=re.compile(r":unread:(\d+)")
        #file_re=re.compile(r":file")
        skip_tags=[]
        if config.has_option("source","skip_tags"):
                skip_tags=config.get("source","skip_tags").split()

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
            #print(type(tags),tags)
            for tag, count in tags[flow]:
                if tag in skip_tags: continue
                elif mention_re.match(tag):
                    user_id=int(mention_re.match(tag).group(1))
                   # print(user_id)
                    user= flowData[flow].users[user_id]
                   # print(user['id'],user['nick'])
                    self.mentions[flow].append(("@"+user['nick'],count) )
                elif everyone_re.match(tag): 
                    self.mentions[flow].append(("@Team",count) )
                elif thread_re.match(tag): continue
                elif tag == ":thread": continue
                elif tag == ":file": continue
                elif tag == ":url": 
                    continue
                elif unread_re.match(tag): continue
                else :
                    self.tags[flow].append( (tag,count) )


class SimpleSummaryData(BaseClasses.BaseProduct):
    def ProcessData(self, flowData,config):
        self.n_messages={}
        self.n_users={}
        for flow, data in flowData.iteritems():
            self.n_messages[flow]=len(data.messages)
            self.n_users[flow]=len(data.users)


class LargestThread(BaseClasses.BaseProduct):
    def __init__(self):
        BaseClasses.BaseProduct.__init__(self)
        # key = flow_name
        # value = (thread id, counts, title )
        self.threads  = defaultdict(list)

    def ProcessData(self, flowData,config):
        # Get the list of threads
        for flow, data in flowData.iteritems():
            threads=[]
            # For each thread, check how many messages are attached and who commented
            for thread_id, thread_data in data.threads.iteritems():
                print (flow, thread_id, thread_data['internal_comments'], thread_data['title'] )
                threads.append( (thread_id, thread_data['internal_comments'], thread_data['title'] ))
            self.threads[flow]=sorted(threads,
                              reverse=True,
                              key=operator.itemgetter(1))
