#!/usr/local/bin/python3
import unittest
from report_processor import ReportProcessor

# Full integration test that runs the latest two reports. 

# class IntegrationTest(unittest.TestCase):
    

def test1():
    url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
    reportProcessor = ReportProcessor(url)
    reportProcessor.main(1)

# Full integration test that run the scenario when there are additional lines in the old report.
def test2():
    dir_url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
    url1 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v75.xml"
    url2 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v71.xml"
    reportProcessor = ReportProcessor(dir_url)
    reportProcessor._process_reports_at(url1, url2)
    
# Full integration test that run the scenario when there are additional lines in the new report.
def test3():
    dir_url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
    url1 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v67.xml"
    url2 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v63.xml"
    reportProcessor = ReportProcessor(dir_url)
    reportProcessor._process_reports_at(url1, url2)
    

test1()
test2()
test3()