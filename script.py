#!/usr/local/bin/python3

from report_processor import ReportProcessor

def __main__():
    url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
    reportProcessor = ReportProcessor(url)
    reportProcessor.get_reports_at(1, 5)
    url1 = reportProcessor.most_recent_report.url
    url2 = reportProcessor.second_last_report.url
    reportProcessor.process_reports_at(url1, url2)
    
__main__()