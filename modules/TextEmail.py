import BaseClasses
from string import Template
from datetime import datetime
import smtplib
from email.mime.text import MIMEText


class TextEmail(BaseClasses.BaseOutput):
    def __init__(self):
        BaseClasses.BaseOutput.__init__(self,['TallyTags','LargestThread','SimpleSummaryData'])

    def MakeURL(self,flow,**kwargs):
        url="https://www.flowdock.com/app/{0}?filter=all".format(flow)
        url+="".join([ "&{0}={1}".format(key,value) for key, value in kwargs.iteritems()])
        return url

    def MakeTagsTable(self,tags_tally,flow):
        output=""
        for tag,count in tags_tally[flow]:
            output+="* {:<20} {: <3} ({})\n".format( tag,
                                                   count,
                                                   self.MakeURL(flow,tags=tag))
        return output

    def MakeThreadsTable(self,threads_tally,flow):
        output=""
        for thread,count,tags,title in threads_tally[flow]:
            if count<3: break
            tmp=""
            url=self.MakeURL(flow+"/messages/"+str(thread))
            tmp+=u"* \"{:<50}...\"\n"
            tmp+=u"     Replies: {: <3}, Tags:{}\n"
            tmp+=u"{}\n\n"
            output+=tmp.format( title, count, ", ".join(tags), url)
        return output


    def CompileOutput(self,flows,config, products):
        # Prepare the message
        output="""
${flow}
--------
There have been ${n_messages} new messages in the last ${hours} hours

= Tags =
${tags_table}

= Mentions =
${mentions_table}

== Longest Threads ==
${thread_table}

"""
        template=Template(output)
        complete="Summary of FlowDock activity"
        complete+=" for "+datetime.today().strftime("%A %d-%b-%Y %Z")+"\n"
        for flow in flows:
            params={
                    'flow':flow,
                    'n_messages':products['SimpleSummaryData'].n_messages[flow],
                    'hours':config.get('source','date_offset'),
                    'tags_table':self.MakeTagsTable(products['TallyTags'].tags,flow),
                    'mentions_table':self.MakeTagsTable(products['TallyTags'].mentions,flow),
                    'thread_table':self.MakeThreadsTable(products['LargestThread'].threads,flow)
                    }
            complete+=template.substitute(params)

        complete+="""
---- Made using FlowMeter ( github.com/BenKrikler/FlowMeter )
        """
        
        # Email the message
        print(complete)

        # Create a text/plain message
        msg = MIMEText(complete,'plain','utf-8')

        # me == the sender's email address
        # you == the recipient's email address
        From=config.get("output","from")
        To=config.get("output","to")
        Subject="[FlowMeter] "+datetime.today().strftime("%d-%b-%Y %Z")+"\n"
        msg['Subject'] = Subject
        msg['From'] = From
        msg['To'] = To

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('localhost')
        s.sendmail(From, To.split(","), msg.as_string())
        s.quit()
