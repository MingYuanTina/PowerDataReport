#!/usr/local/bin/python3

import smtplib, ssl
import urllib.request				# html inspector 
from bs4 import BeautifulSoup 	    # html parser
from datetime import datetime
from email.mime.text import MIMEText
from xml_parser import Parser

#---------------------------------- Utilities ----------------------------------
class WebCrawler(object):
	def __init__(self, url=""):
		self.html_features = "html.parser"
		self.xml_features = "xml"

	def get_html_content(self, url):
		page = urllib.request.urlopen(url)
		html = BeautifulSoup(page, features=self.html_features)
		return html

	def get_xml_content(self, url): 
		return urllib.request.urlopen(url).readlines()

class EmailSender(object): 
	def send_email(self, message): 
		sender_email = "powerreport202009@gmail.com"
		receiver_email = "powerreport202009@gmail.com"

		msg = MIMEText(message)
		msg['From'] = sender_email
		msg['To'] = receiver_email
		msg['Subject'] = 'Power Data Report'

		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login("powerreport202009@gmail.com", "smartkids")
			server.sendmail(sender_email, receiver_email, msg.as_string())

#---------------------------------- Logic  ----------------------------------
# ReportProcess define comparison rules and run report checking. 
#   on http://reports.ieso.ca/public/TxLimitsOutage0to2Days/
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
		self.reports = {}


	def generate_report(self, index=0, reverse=False):
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

	
	def compare_diff(self, first, second):
		self.dir_content = self.web_crawler.get_html_content(self.directory_url) 
		most_recent_report = self.generate_report(index=first, reverse=True)
		second_last_report = self.generate_report(index=second, reverse=True)

		last_modified = datetime.strptime(most_recent_report.time, '%H:%M')
		second_last_modified = datetime.strptime(second_last_report.time, '%H:%M')
		print("Timestamp Compared: " + str(last_modified) + " vs " + str(second_last_modified))

		xml1 = self.web_crawler.get_xml_content(most_recent_report.url)
		xml2 = self.web_crawler.get_xml_content(second_last_report.url)
		diff = ""

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
		content_diff = self.compare_diff(1, 5)
		if (content_diff == None): 
			self.email_sender.send_email("no difference")
		else:
			self.email_sender.send_email(content_diff)


url = "http://reports.ieso.ca/public/TxLimitsOutage0to2Days"

reportProcessor = ReportProcessor(url)
reportProcessor.proces_reports()


