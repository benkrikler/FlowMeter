URLS
----
Get all messages from an organisation and from a flow:
 "https://<private-token>@api.flowdock.com/flows/comet/icedust-in-general/messages"

Outputs
-------
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

Configuration
-------------
User details:
 - Username, tokens
Which desired outputs
