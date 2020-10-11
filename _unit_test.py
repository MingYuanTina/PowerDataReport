#!/usr/local/bin/python3
import unittest
from report_processor import ReportProcessor

######
# The following are unit tests that verify the following scenarios:
# 1. UnitTest: two reports are identical
# 2. UnitTest: the old report has additional lines that is not contained within new report. 
# 3. UnitTest: the lastest report has additional lines that is not contained within old report.
# 4. UnitTest: two reports have differences but not belong to import/export category.
# 5. UnitTest: two reports have differences and it belongs to import/export category.
# 6. IntegrtionTest: process the latest two reports.
######
class UnitTest(unittest.TestCase):
    def _get_xml(self, url):
        f = open(url, "rb")
        content = f.readlines()
        f.close()
        return content

    # Scenario 1.
    def test1(self):
        xml1 = self._get_xml("./test/test1_xml1.xml")
        xml2 = self._get_xml("./test/test1_xml2.xml")
        reportProcessor = ReportProcessor("")
        dic1 = reportProcessor.parser.parse_content(xml1)
        dic2 = reportProcessor.parser.parse_content(xml2)
        diff = reportProcessor._generate_report_diff(dic1, dic2)
        print("----------------------Test1 no difference----------------------\n")
        self.assertEqual(diff, "")
        
    # Scenario 2.
    def test2(self):
        xml1 = self._get_xml("./test/test2_xml1.xml")
        xml2 = self._get_xml("./test/test2_xml2.xml")
        reportProcessor = ReportProcessor("")
        dic1 = reportProcessor.parser.parse_content(xml1)
        dic2 = reportProcessor.parser.parse_content(xml2)
        diff = reportProcessor._generate_report_diff(dic1, dic2)
        expected_content = "additional line(s) in old report:\n" \
            + "Manitoba + Minnesota Export | 2020-09-09T19:41:18 | 2020-08-21T21:00:00 | 2020-12-31T23:59:00 | 100 | Internal system conditions \n"
        print("----------------------Test2 Result----------------------")
        print("Actual Results\n", reportProcessor.diff)
        print("Expected Results\n", expected_content)
        self.assertEqual(diff, expected_content)
        
    # Scenario 3.
    def test3(self):
        xml1 = self._get_xml("./test/test3_xml1.xml")
        xml2 = self._get_xml("./test/test3_xml2.xml")
        reportProcessor = ReportProcessor("")
        dic1 = reportProcessor.parser.parse_content(xml1)
        dic2 = reportProcessor.parser.parse_content(xml2)
        diff = reportProcessor._generate_report_diff(dic1, dic2)
        expected_content = "additional line(s) in new report:\n" \
            + "Manitoba + Minnesota Import | 2020-09-20T21:12:38 | 2020-08-21T21:00:00 | 2020-12-31T23:59:00 | 190 | Internal system conditions \n"
        print("----------------------Test3 Result----------------------")
        print("Actual Results\n", reportProcessor.diff)
        print("Expected Results\n", expected_content)
        self.assertEqual(diff, expected_content)
        
    # Scenario 4.
    def test4(self):
        xml1 = self._get_xml("./test/test4_xml1.xml")
        xml2 = self._get_xml("./test/test4_xml2.xml")
        reportProcessor = ReportProcessor("")
        dic1 = reportProcessor.parser.parse_content(xml1)
        dic2 = reportProcessor.parser.parse_content(xml2)
        diff = reportProcessor._generate_report_diff(dic1, dic2)
        print("----------------------Test4 no difference----------------------\n")
        self.assertEqual(diff, "")
        
    # Scenario 5.
    def test5(self):
        xml1 = self._get_xml("./test/test5_xml1.xml")
        xml2 = self._get_xml("./test/test5_xml2.xml")
        reportProcessor = ReportProcessor("")
        dic1 = reportProcessor.parser.parse_content(xml1)
        dic2 = reportProcessor.parser.parse_content(xml2)
        diff = reportProcessor._generate_report_diff(dic1, dic2)
        expected_content = "Difference at Manitoba + Minnesota Import :\n" \
            + "New Report: Manitoba + Minnesota Import | 2020-09-20T21:12:38 | 2020-08-21T21:00:00 | 2020-12-31T23:59:00 | 200 | Internal system conditions \n" \
            + "Old Report: Manitoba + Minnesota Import | 2020-09-20T21:12:38 | 2020-08-21T21:00:00 | 2020-12-31T23:59:00 | 190 | Internal system conditions \n" \
            + "\n"
        print("----------------------Test5 Result----------------------")
        print("Actual Results\n", reportProcessor.diff)
        print("Expected Results\n", expected_content)
        self.assertEqual(diff, expected_content)
        
    # Full integration test that runs the latest two reports. 
    def test6(self):
        url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
        reportProcessor = ReportProcessor(url)
        reportProcessor.get_reports_at(1, 5)
        url1 = reportProcessor.most_recent_report.url
        url2 = reportProcessor.second_last_report.url
        reportProcessor.process_reports_at(url1, url2)
    
    def test7(self):
        dir_url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
        url1 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v75.xml"
        url2 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v71.xml"
        reportProcessor = ReportProcessor(dir_url)
        reportProcessor.process_reports_at(url1, url2)
        
    def test8(self):
        dir_url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"
        url1 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v67.xml"
        url2 = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days/PUB_TxLimitsOutage0to2Days_20201009_v63.xml"
        reportProcessor = ReportProcessor(dir_url)
        reportProcessor.process_reports_at(url1, url2)
    
if __name__ == '__main__':
    unittest.main()
    