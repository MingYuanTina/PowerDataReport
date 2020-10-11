#!/usr/local/bin/python3
import unittest
from ../report_processor import ReportProcessor

# Full integration test that runs the latest two reports. 
def test1(self):
    url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
    reportProcessor = ReportProcessor(url)
    reportProcessor.get_reports_at(1, 5)
    url1 = reportProcessor.most_recent_report.url
    url2 = reportProcessor.second_last_report.url
    reportProcessor.process_reports_at(url1, url2)

# Full integration test that run the scenario when there are additional lines in the old report.
def test2(self):
    dir_url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
    url1 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v75.xml"
    url2 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v71.xml"
    reportProcessor = ReportProcessor(dir_url)
    reportProcessor.process_reports_at(url1, url2)
    
# Full integration test that run the scenario when there are additional lines in the new report.
def test3(self):
    dir_url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
    url1 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v67.xml"
    url2 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v63.xml"
    reportProcessor = ReportProcessor(dir_url)
    reportProcessor.process_reports_at(url1, url2)
    

test1()
test2()
test3()