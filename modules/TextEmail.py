import BaseClasses
from string import Template
from datetime import datetime,timedelta
import smtplib
from email.mime.text import MIMEText

def Underline(str,char="-"):
    return ''.join([char]*len(str))

class TextEmail(BaseClasses.BaseOutput):
    def __init__(self):
        BaseClasses.BaseOutput.__init__(self,['TallyTags','LargestThread','SimpleSummaryData','FlowEmails'])

    def MakeURL(self,flow,**kwargs):
        url="www.flowdock.com/app/{0}?filter=all".format(flow)
        url+="".join([ "&{0}={1}".format(key,value) for key, value in kwargs.iteritems()])
        return url

    def MakeTagsTable(self,tags_tally,flow):
        if len(tags_tally[flow]) == 0:
            return None
        output=""
        for tag,count in tags_tally[flow]:
            output+="* {:<20} {: <3} ({})\n".format( tag,
                                                   count,
                                                   self.MakeURL(flow,tags=tag))
        return output

    def MakeThreadsTable(self,threads_tally,flow):
        if len(threads_tally[flow]) == 0:
            return None
        output=""
        for thread,count,title in threads_tally[flow]:
            if count<3: continue
            tmp=""
            url=self.MakeURL(flow+"/messages/"+str(thread))
            tmp+=u"* \"{}\"\n"
            tmp+=u"     Replies: {: <3}\n"
            tmp+=u"{}\n\n"
            output+=tmp.format( title, count,  url)
        return output

    def MakeFlowSection(self,flow,config, products):
        n_msg=products['SimpleSummaryData'].n_messages[flow]
        if n_msg<1: return None
        hours=config.get('source','date_offset')

        output=flow+"\n"
        output+=Underline(flow)
        output+="\n"
        output+="There ha" + ("s" if n_msg==1 else "ve") + " been "
        output+=str(n_msg)+" new message" + ("s" if n_msg > 1 else "")
        output+=" in the "+str(hours)+ " hours since "
        output+=(datetime.now() - timedelta(hours=int(hours))).strftime("%c")
        output+="\n"
        output+="\n"

        # Get the tags for this flow
        sect=self.MakeTagsTable(products['TallyTags'].tags,flow)
        if sect: 
            output+="= Tags =\n"
            output+=sect
            output+="\n"

        # Get the mentions for this flow
        sect=self.MakeTagsTable(products['TallyTags'].mentions,flow)
        if sect: 
            output+="= Mentions =\n"
            output+=sect
            output+="\n"

        # Get the longes threads for this flow
        sect=self.MakeThreadsTable(products['LargestThread'].threads,flow)
        if sect: 
            output+="= Threads =\n"
            output+=sect
            output+="\n"

        return output

    def MakeFlowEmails(self,flows,email_product):
        output="Access details for all Flows:\n"
        output+=Underline(output)+"\n"
        for flow in flows:
            output+=flow+":\n"
            output+="  Join: "+email_product.join_urls[flow]+"\n"
            output+="  Email: "+email_product.emails[flow]+"\n"
            output+="\n"
        output+="""
You can email directly to any flow using the emails above.  To tag the email,
add "+tagname" before the '@' symbol.  To mention someone, add '.person' before
the '@' symbol.  So for example, to email a flow called death-star, mention luke
and tag it with the force write to: death-star.luke+use_force@jedis.flowdock.com
"""
        return output

    def CompileOutput(self,flows,config, products):
        # Prepare the message
        complete="Summary of FlowDock activity"
        complete+=" for "+datetime.today().strftime("%A %d-%b-%Y %Z")+"\n\n"
        had_activity=False
        for flow in flows:
            section=self.MakeFlowSection(flow,config,products)
            if section:
                had_activity=True
                complete+=section
        complete+="\n"
        complete+=self.MakeFlowEmails(flows,products['FlowEmails'])
        complete+="""
---- Made using FlowMeter ( github.com/BenKrikler/FlowMeter )
        """

        # Do we want to continue (was there activity)?
        if not had_activity:
            print "There was no activity today, so nothing to report"
            return

        #############
        # Email the message
        #############
        #print(type(complete))

        # Create a text/plain message
        msg = MIMEText(complete.encode('ascii','ignore'))

        # me == the sender's email address
        # you == the recipient's email address
        From=config.get("output","from")
        To=config.get("output","to")
        Subject=config.get("output","subject_tag")+" "
        Subject+=datetime.today().strftime("%d-%b-%Y %Z")+"\n"
        msg['Subject'] = Subject
        #msg['From'] = From
        #msg['To'] = To

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('localhost')
        print(msg)
        s.set_debuglevel(True)
        print(To.split())

        s.sendmail(From, To.split(), msg.as_string())
        s.quit()
