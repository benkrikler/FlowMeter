#! /usr/bin/env python2

import configparser
import sys
from modules import BaseClasses,GetFlows
import exceptions
from collections import defaultdict

default_config={
	'date_offset':24 # hours to look for messages
        }
config = configparser.ConfigParser(default_config)

class FlowData():
    messages={}
    users={}
    threads=[]
    info=()

def GetAllFlows(date_offset, flowdock, flows):
    flowData=defaultdict(FlowData)
    flow_orgs=[ flow['organization']['parameterized_name'] for flow in flows]
    flow_names=[ flow['parameterized_name'] for flow in flows]
    for [org,flow,info] in zip(flow_orgs,flow_names,flows):
        org_flow=org+"/"+flow
        flowData[org_flow].messages = flowdock.GetMessages(date_offset,org,flow)
        flowData[org_flow].users = flowdock.GetUsers(org,flow)
        flowData[org_flow].threads = flowdock.GetThreads(org,flow)
        flowData[org_flow].info = info
    return flowData

def GetInstances(class_list, base_class):
    # I'm  not sure what the  most pythonic way  to test this situation  is, but
    # this works at least:
    instances={}
    for request in class_list:
        found_class=False
        for clas in base_class.__subclasses__():
            if clas.__name__ == request: 
                instances[request]=clas()
                found_class=True
                break
        if not found_class:
            raise LookupError("Unknown class ('"+request+"') requested")
    return instances

def DeduceOutputs(requested_outputs):
    return GetInstances(requested_outputs,BaseClasses.BaseOutput)

def DeduceProducts(outputs):
    # Gather all the needed products from the output dependencies
    requested_products=set()
    for name, output in outputs.iteritems():
        requested_products |= set(output.product_dependencies)

    # Now get the products ready
    return GetInstances(requested_products,BaseClasses.BaseProduct)

def Main(config):
    # Check config file

    # Deduce the products we need to make given the requested outputs
    outputs=DeduceOutputs(config.get("output","outputs").split())
    print("Outputs that will be run: "+ str(outputs.keys()))
    products=DeduceProducts(outputs)
    print("Products that will be created: "+ str(products.keys()))

    # Get all available flows for this token that are organisation wide:
    flowdock=GetFlows.Connection(config.get("source","token"))
    allFlows=flowdock.GetFlows()

    # Get all new messages for each requested flow
    date_offset=config.getfloat("source","date_offset")
    if config.has_option("source","all_flows") and config.getboolean("source","all_flows"):
            flows=allFlows
    else: 
            flows=[ flow for flow in allFlows if flow['organization']['parameterized_name'] +"/"+ flow['parameterized_name'] in config.get("source","flows").split() ]
    flowData = GetAllFlows(date_offset,flowdock,flows )

    # Make each requested product 
    for name, product in products.iteritems():
        product.ProcessData(flowData,config)

    # Lastly, compile and send / upload each output
    for name, output in outputs.iteritems():
        output.CompileOutput( flowData.keys(),config,products)


if __name__ == "__main__":
    # Get the configuration
    config_file="flowmeter.cfg"
    if len(sys.argv) > 1:
        config_file=sys.argv[1]
    config.read(config_file)

    # Now run the program
    Main(config)
