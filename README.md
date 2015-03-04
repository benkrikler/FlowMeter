FlowMeter
----
A tool to sumarize set of [FlowDock](https://www.flowdock.com) flows.

Configuration
-------------
User details:
 - Username, private token
Flowdock source
 - List of flows
 - Number of hours to retrieve messages from
Outputs:
 - A list of Outputs to run. Currently only (Plain)TextEmail is (partially) implemented.

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
