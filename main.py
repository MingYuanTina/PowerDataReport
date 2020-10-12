#!/usr/local/bin/python3

from report_processor import ReportProcessor
import sys

def __main__():
    url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
    reportProcessor = ReportProcessor(url)
    num_compared = int(sys.argv[1])
    reportProcessor.main(num_compared) 
    
__main__()