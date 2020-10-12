#!/usr/local/bin/python3

from report_processor import ReportProcessor

def __main__():
    url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
    reportProcessor = ReportProcessor(url)
    reportProcessor.main(10)
        
    
__main__()