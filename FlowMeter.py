#! /usr/bin/env python2

import configparser
import sys
from modules import GetFlows

default_config={
	'date_offset':24 # hours to look for messages
        }
config = configparser.ConfigParser(default_config)

if __name__ == "__main__":
    # Get the configuration
    config_file="flowmeter.cfg"
    if len(sys.argv) > 1:
        config_file=sys.argv[1]
    config.read(config_file)

    # Obtain the flow
    flows=GetFlows.Connection(config.get("source","token"))
    date_offset=config.getfloat("source","date_offset")
    for org_flow in config.get("source","flows").split():
	    [org,flow]=org_flow.split("/",1)
	    flows.GetFlow(date_offset,org,flow)
