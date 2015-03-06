FlowMeter
----
A tool to sumarize set of [FlowDock](https://www.flowdock.com) flows.

Configuration
-------------
Configuration is done using python's ConfigParser and the file name for the
config should be passed on the command line as the only option.

The following is an example config file:
```cfg
# myConfig.cfg
[source]
token= <your flowdock private token>
flows= < space separated list of flows (including the organisation) >
date_offset= < the number of hours to look for messages from >

[output]
outputs=<A space separated list of output modules to run.  Currentl only TextEmail is available>
from=< The email address of the sender >
subject_tag=< The subject tag to be prefixed to the email, useful for inbox
filtering. >
to=< A space separted list of email addresses to send the outputs to >

```

Outputs
-------
(NOTE: This is only partially implemented at this point, 4 March 2015)
Would like to see:
- Number of comments in each flow
- Comparison to last fortnight's activity
- Tally of tags mentioned
- Tally of comments from people
- List of files attached w/ links to get them
- non-tagged keywords
Want to link everything back to flowdock APP
Distribute data:
 - Email (plan text)
 - Email (html)
 - Web-page

Code structure
--------------
1. Get latest activity
   - Latest is since last update (probably nightly)
   - Stored locally (how do you best store json objects ?)
2. Select outputs
   - Outputs state the products they need
3. Make products
   - Init each producer
   - For each JSON object, run each producer
   - Finish each producer
4. Prepare outputs
   - Prepares html, text etc 
   - Uploads to web-page or sends out an email
