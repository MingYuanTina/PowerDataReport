#!/usr/local/bin/python3

from datetime import datetime
from report_comparator import ReportComparator
from utilities import WebCrawler, EmailSender

# ReportProcess define comparison rules and run checking against http://reports.ieso.ca/public/TxLimitsOutage0to2Days/
# Compare the most recent report with the second last report output
# If there is a different, email the user the differences of the two reports. 
class Report:
	def __init__(self, dir_path="", filename="", date="", time=""):
		self.url = dir_path + "/" + filename
		self.date = date   # last modified date
		self.time = time   # last modified time

class ReportProcessor(object):
	def __init__(self, directory_url=""):
		self.web_crawler = WebCrawler()
		self.email_sender = EmailSender()
		self.directory_url = directory_url

	def _generate_report_object(self, dir_content="", index=0, reverse=False):
		a_links = dir_content.find_all("a")
		a_index = len(a_links)-index if reverse else index
		report_tag = a_links[a_index]

		meta_data = report_tag.next_sibling.lstrip().split(' ')
		dir_path = self.directory_url
		filename = report_tag.attrs['href']
		return Report(dir_path=dir_path, filename=filename, date=meta_data[0], time=meta_data[1])
			
	# Retrieve the xml content of two reports, parse and store content as dictionary. 
	def _process_reports_at(self, url1, url2):
		xml1 = self.web_crawler.get_xml_content(url1)
		xml2 = self.web_crawler.get_xml_content(url2)
		comparator = ReportComparator()
		diff = comparator.compare_content(xml1, xml2)
		if (diff != ""): 
			header = "New report: {0} \nOld report: {1} \n".format(url1, url2)
			diff = header + diff
		return diff
			
	def main(self, comparison_num): # return differences of two reports.
		interval = 4
		msg_list = []
		
		rp = ReportProcessor(self.directory_url)
		dir_content = self.web_crawler.get_html_content(self.directory_url) 
		for i in range(1, comparison_num * interval + 1, interval):
			new_report = self._generate_report_object(dir_content, index=i, reverse=True)
			old_report = self._generate_report_object(dir_content, index=i+interval, reverse=True)
			diff = rp._process_reports_at(new_report.url, old_report.url)
			
			last_modified = datetime.strptime(new_report.time, '%H:%M')
			second_last_modified = datetime.strptime(old_report.time, '%H:%M')
			print("Timestamp Compared: " + str(last_modified) + " vs " + str(second_last_modified))
			if (diff != ""):
				msg_list.append(diff)
				print("There is a difference. Email is sent to the mailbox")
		print("Total email sent: ", len(msg_list))
		self.email_sender.send_emails(msg_list)
        
        
        	
        
        
        
        
		
			
			
			
