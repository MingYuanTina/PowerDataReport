#!/usr/local/bin/python3

from datetime import datetime
from report_parser import Parser
from utilities import WebCrawler, EmailSender

#---------------------------------- Logic  ----------------------------------
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
		self.directory_url = directory_url
		self.dir_content = ""
		self.diff = ""


	def generate_report_content(self, index=0, reverse=False):
		a_links = self.dir_content.find_all("a")
		a_index = len(a_links)-index if reverse else index
		report_tag = a_links[a_index]

		meta_data = report_tag.next_sibling.lstrip().split(' ')
		dir_path = self.directory_url
		filename = report_tag.attrs['href']
		date = meta_data[0]
		time = meta_data[1]
		return Report(dir_path, filename, date, time)


	def compute_diff(self, xml1, xml2):
		diff = ""
		i = 14
		while i < len(xml1):
			if (xml1[i].decode("utf-8") == "<InterfaceData>\n"):
				rowTitle = xml1[i+1].decode("utf-8").replace("<InterfaceName>", "").replace("</InterfaceName>", "")
				for j in range(i + 2, i + 7):
					if (xml1[j] != xml2[j]):
						old_line = "Older: " + xml2[j].decode("utf-8")
						new_line = "Latest: " + xml1[j].decode("utf-8")
						diff = diff + rowTitle + old_line + new_line
				i = i + 7
			i += 1

		if len(xml1) != len(xml2):
			diff = diff + "Extra Lines: "
		for i in range(len(xml1), len(xml2)):
			diff = diff + xml2[i].decode("utf-8")
		return diff

	def generate_report_diff(self, dic1, dic2):
		set1 = set(dic1.keys())
		set2 = set(dic2.keys())
		new_lines_dic1 = set1.difference(set2)
		if (len(new_lines_dic1) != 0):
			self.diff = self.diff + "Additional Line(s) in NEW report\n"
			self.__compute_diff__(new_lines_dic1, dic1)
	
		
		new_lines_dic2 = set2.difference(set1)
		if (len(new_lines_dic2) != 0):
			self.diff = self.diff + "Additional Line(s) in OLD report\n"
			self.__compute_diff__(new_lines_dic2, dic2)
			
		# print(new_lines_dic1)
		# print(new_lines_dic2)
		
		intersection = set1.intersection(set2)
		for key in intersection:
			item1 = dic1[key]
			item2 = dic2[key]
			if item1.__eq__(item2) == False: 
				self.dic += "Difference at {item1.title} :\n"
				self.dic += "New Report: " + item1.__str__() + "\n"
				self.dic += "Old Report: " + item1.__str__() + "\n"
	
	def __compute_diff__(self, l, dic1):
		for i in range(0, len(l)):
			key = l[i]
			item = dic1[key]
			self.dic += item.__str__()

	
	def compare_reports_at(self, first_index, second_index):
		self.dir_content = self.web_crawler.get_html_content(self.directory_url) 
		most_recent_report = self.generate_report_content(index=first_index, reverse=True)
		second_last_report = self.generate_report_content(index=second_index, reverse=True)

		# Compute the timestamp difference.
		last_modified = datetime.strptime(most_recent_report.time, '%H:%M')
		second_last_modified = datetime.strptime(second_last_report.time, '%H:%M')
		print("Timestamp Compared: " + str(last_modified) + " vs " + str(second_last_modified))

		# Retrieve the xml content of two reports.
		xml1 = self.web_crawler.get_xml_content(most_recent_report.url)
		xml2 = self.web_crawler.get_xml_content(second_last_report.url)
		diff = ""

		# Parse two reports and store them as dictionary [key=Row], [value=list of columns].
		parser = Parser()
		dic1 = parser.parse_content(xml1)
		dic2 = parser.parse_content(xml2)
		
		self.generate_report_diff(dic1, dic2)

		#  Compare two report sets and compute their differences.
		if (len(xml1) < len(xml2)):
			diff = self.compute_diff(xml1, xml2)
		else:
			diff = self.compute_diff(xml2, xml1)

		if (diff == ""): 
			return None
		else:
			header = most_recent_report.url + "\n" + second_last_report.url + "\n"
			return header + diff
		
	def proces_reports(self):
		content_diff = self.compare_reports_at(1, 5)
		if (content_diff == None): 
			self.email_sender.send_email("no difference")
		else:
			self.email_sender.send_email(content_diff)


url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"

reportProcessor = ReportProcessor(url)
reportProcessor.proces_reports()


