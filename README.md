FlowMeter
----
A tool to summarize set of [FlowDock](https://www.flowdock.com) flows.

Configuration
-------------
Configuration is done using python's ConfigParser and the file name for the
config should be passed on the command line as the only option.

The following is an example config file:
```cfg
# myConfig.cfg
[source]
token= <your flowdock private token>
date_offset= < the number of hours to look for messages from >

# You can either a give a list of flows to summarize:
flows= < space separated list of flows (including the organisation) >
# or you can summarize all flows, but skip a few
all_flows=True
skip_flows=< space separated list of flows (including the organisation) >

# Ignore several specific tags:
skip_tags=< space separated list of tags (normally lower case) >

[output]
outputs=<A space separated list of output modules to run.  Currentl only TextEmail is available>
from=< The email address of the sender >
subject_tag=< The subject tag to be prefixed to the email, useful for inbox
filtering. >
to=< A space separted list of email addresses to send the outputs to >

```

Outputs
-------
Would like to see:
- Number of comments in each flow
- Tally of tags mentioned
- Tally of comments from people
Want to link everything back to flowdock APP
Distribute data:
 - Email (plan text)
 - Email (html)
 - Web-page

Some future ideas:
- Comparison to last fortnight's activity
- Special section for new members 
- Special section for @everyone comments
- List of files attached w/ links to get them
- Frequency of all words, including non-tagged items (excluding common words
  like 'the', 'and' etc).

Code structure
--------------
1. Select outputs
   - Outputs state the products they need
2. Get latest activity
   - Latest is since last update (probably nightly)
   - Stored locally (how do you best store json objects ?)
3. Make products
   - Init each producer
   - For each JSON object, run each producer
   - Finish each producer
4. Prepare outputs
   - Prepares html, text etc 
   - Uploads to web-page or sends out an email
