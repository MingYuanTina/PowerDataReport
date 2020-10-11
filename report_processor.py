#!/usr/local/bin/python3

from datetime import datetime
from report_parser import Parser
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
		self.parser = Parser()
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

	def _generate_report_diff(self, dic1, dic2):
		set1 = set(dic1.keys())
		set2 = set(dic2.keys())
		new_lines_dic1 = set1.difference(set2)
		if (len(new_lines_dic1) != 0):
			self.diff += "additional line(s) in new report:\n"
			for key in new_lines_dic1:
				self.diff += dic1[key].__str__()
	
		new_lines_dic2 = set2.difference(set1)
		if (len(new_lines_dic2) != 0):
			self.diff = self.diff + "additional line(s) in old report:\n"
			for key in new_lines_dic2:
				self.diff += dic2[key].__str__()
		
		intersection = set1.intersection(set2)
		for key in intersection:
			item1 = dic1[key]
			item2 = dic2[key]
			if_import_export = key.lower().find("import") != -1 or key.lower().find("export") != -1
			if if_import_export and item1.__eq__(item2) == False: 
				self.diff += "Difference at " + item1.title + " :\n"
				self.diff += "New Report: " + item1.__str__()
				self.diff += "Old Report: " + item2.__str__() + "\n"
		return self.diff
		
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
		dic1 = self.parser.parse_content(xml1)
		dic2 = self.parser.parse_content(xml2)
		self._generate_report_diff(dic1, dic2)
		
		if (self.diff == ""): 
			self.email_sender.send_email("no difference")
		else:
			header = "{0} \n {1} \n".format(url1, url2)
			self.diff = header + self.diff
			self.email_sender.send_email(self.diff)
			
			
			
