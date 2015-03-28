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
        self.threads  = defaultdict(list,"")
        self.mentions = defaultdict(list)

    def ProcessData(self, flowData):
        mention_re=re.compile(r":user:(\d+)")
        everyone_re=re.compile(r":user:(everyone|everybody|all|anyone|anybody)")
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
            #print(type(tags),tags)
            for tag, count in tags[flow]:
                if mention_re.match(tag):
                    user_id=int(mention_re.match(tag).group(1))
                   # print(user_id)
                    user= flowData[flow].users[user_id]
                   # print(user['id'],user['nick'])
                    self.mentions[flow].append(("@"+user['nick'],count) )
                elif everyone_re.match(tag): 
                    self.mentions[flow].append(("@everyone",count) )
                elif thread_re.match(tag): continue
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
    def __init__(self):
        BaseClasses.BaseProduct.__init__(self)
        self.threads  = defaultdict(dict)
        self.tag_filter=TagsFilter()


    def ProcessData(self, flowData):
        # Get the list of threads
        thread_re=re.compile(r"influx:(\d+)")
        for flow, data in flowData.iteritems():
            threads=[]
            # For each thread, check how many messages are attached and who commented
            thread_count=defaultdict(int)
            thread_tags=defaultdict(set)
            for iid, msg in data.messages.iteritems():
                thread_id=[ thread_re.match(tag).group(1) for tag in msg['tags'] if thread_re.match(tag) ]
                if len(thread_id) >0:
                    thread_id=thread_id[0]
                    thread_count[thread_id]+=1
                    thread_tags[thread_id].update(msg['tags'])
                    thread_tags[thread_id].add("@"+data.users[int(msg['user'])]['nick'])

            # sort by count
            ids=sorted(thread_count.items(),
                              reverse=True,
                              key=operator.itemgetter(1))
            for thread_id,count in ids:
                content=data.threads[thread_id]["content"]
                if not isinstance(content,basestring): continue
                content=content.split()
                content=" ".join(content[0:10]) + ( r"..." if len(content) > 10 else "" )
                threads.append( (thread_id, count,
                                 self.tag_filter.Apply(thread_tags[thread_id],
                                                       data.users),
                                 content ) )
            self.threads[flow]=threads
