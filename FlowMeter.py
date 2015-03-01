#! /usr/bin/env python2

import configparser
import sys
from modules import GetFlows

default_config={
        }
config = configparser.ConfigParser(default_config)

if __name__ == "__main__":
    # Get the configuration
    config_file="flowmeter.cfg"
    if len(sys.argv) > 1:
        config_file=sys.argv[1]
    config.read(config_file)

    # Obtain the flow
    flows=GetFlows.Connection(config.get("flowdock","token"))
    flows.GetFlow("","comet","icedust-in-general")
