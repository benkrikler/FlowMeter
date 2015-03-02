import BaseClasses
from string import Template
from datetime import datetime

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

    def CompileOutput(self,flows,config, products):
        output="""
${flow}
--------
There have been ${n_messages} new messages in the last ${hours} hours

= Tags =
${tags_table}

= Mentions =
${mentions_table}

= 10 longest threads =
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
                    'thread_table':" < not yet implemented >"
                    }
            complete+=template.substitute(params)

        complete+="""
---- Made using FlowMeter ( github.com/BenKrikler/FlowMeter )
        """
        
        print(complete)
