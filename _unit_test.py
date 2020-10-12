#!/usr/local/bin/python3
import unittest
from report_processor import ReportProcessor
from report_comparator import ReportComparator

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
        comparator = ReportComparator()
        diff = comparator.compare_content(xml1, xml2)
        print("----------------------Test1 no difference----------------------\n")
        self.assertEqual(diff, "")
        
    # Scenario 2.
    def test2(self):
        xml1 = self._get_xml("./test/test2_xml1.xml")
        xml2 = self._get_xml("./test/test2_xml2.xml")
        comparator = ReportComparator()
        diff = comparator.compare_content(xml1, xml2)
        expected_content = "additional line(s) in old report:\n" \
            + "Manitoba + Minnesota Export | 2020-09-09T19:41:18 | 2020-08-21T21:00:00 | 2020-12-31T23:59:00 | 100 | Internal system conditions \n"
        print("----------------------Test2 Result----------------------")
        print("Actual Results\n", diff)
        print("Expected Results\n", expected_content)
        self.assertEqual(diff, expected_content)
        
    # Scenario 3.
    def test3(self):
        xml1 = self._get_xml("./test/test3_xml1.xml")
        xml2 = self._get_xml("./test/test3_xml2.xml")
        comparator = ReportComparator()
        diff = comparator.compare_content(xml1, xml2)
        expected_content = "additional line(s) in new report:\n" \
            + "Manitoba + Minnesota Import | 2020-09-20T21:12:38 | 2020-08-21T21:00:00 | 2020-12-31T23:59:00 | 190 | Internal system conditions \n"
        print("----------------------Test3 Result----------------------")
        print("Actual Results\n", diff)
        print("Expected Results\n", expected_content)
        self.assertEqual(diff, expected_content)
        
    # Scenario 4.
    def test4(self):
        xml1 = self._get_xml("./test/test4_xml1.xml")
        xml2 = self._get_xml("./test/test4_xml2.xml")
        comparator = ReportComparator()
        diff = comparator.compare_content(xml1, xml2)
        print("----------------------Test4 no difference----------------------\n")
        self.assertEqual(diff, "")
        
    # Scenario 5.
    def test5(self):
        xml1 = self._get_xml("./test/test5_xml1.xml")
        xml2 = self._get_xml("./test/test5_xml2.xml")
        comparator = ReportComparator()
        diff = comparator.compare_content(xml1, xml2)
        expected_content = "Difference at Manitoba + Minnesota Import :\n" \
            + "New Report: Manitoba + Minnesota Import | 2020-09-20T21:12:38 | 2020-08-21T21:00:00 | 2020-12-31T23:59:00 | 200 | Internal system conditions \n" \
            + "Old Report: Manitoba + Minnesota Import | 2020-09-20T21:12:38 | 2020-08-21T21:00:00 | 2020-12-31T23:59:00 | 190 | Internal system conditions \n" \
            + "\n"
        print("----------------------Test5 Result----------------------")
        print("Actual Results\n", diff)
        print("Expected Results\n", expected_content)
        self.assertEqual(diff, expected_content)
    
if __name__ == '__main__':
    unittest.main()
    