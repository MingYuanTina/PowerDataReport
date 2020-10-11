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

	def _print(self):
		print('Report: ' + self.url + ' modified on ' + self.date + " " + self.time)

class ReportProcessor(object):
	def __init__(self, directory_url=""):
		self.web_crawler = WebCrawler()
		self.email_sender = EmailSender()
		self.comparator = ReportComparator()
		self.directory_url = directory_url
		self.diff = ""

	def _generate_report_object(self, dir_content="", index=0, reverse=False):
		a_links = dir_content.find_all("a")
		a_index = len(a_links)-index if reverse else index
		report_tag = a_links[a_index]

		meta_data = report_tag.next_sibling.lstrip().split(' ')
		dir_path = self.directory_url
		filename = report_tag.attrs['href']
		date = meta_data[0]
		time = meta_data[1]
		return Report(dir_path, filename, date, time)
		
	def get_reports_at(self, first_index, second_index):
		dir_content = self.web_crawler.get_html_content(self.directory_url) 
		self.most_recent_report = self._generate_report_object(dir_content, index=first_index, reverse=True)
		self.second_last_report = self._generate_report_object(dir_content, index=second_index, reverse=True)
		
		# Compute the timestamp difference.
		last_modified = datetime.strptime(self.most_recent_report.time, '%H:%M')
		second_last_modified = datetime.strptime(self.second_last_report.time, '%H:%M')
		print("Timestamp Compared: " + str(last_modified) + " vs " + str(second_last_modified))
			
	def process_reports_at(self, url1, url2):
		# Retrieve the xml content of two reports, parse and store content as dictionary. 
		xml1 = self.web_crawler.get_xml_content(url1)
		xml2 = self.web_crawler.get_xml_content(url2)
		self.diff = self.comparator.compare_content(xml1, xml2)
		
		if (self.diff == ""): 
			self.email_sender.send_email("no difference")
		else:
			header = "{0} \n {1} \n".format(url1, url2)
			self.diff = header + self.diff
			self.email_sender.send_email(self.diff)
			
			
			
