#!/usr/local/bin/python3
import smtplib, ssl
import urllib.request, urllib.error				# html inspector 
from bs4 import BeautifulSoup 	    			# html parser
from email.mime.text import MIMEText

class WebCrawler(object):
	def __init__(self, url=""):
		self.html_features = "html.parser"
		self.xml_features = "xml"

	def get_html_content(self, url):
		page = urllib.request.urlopen(url)
		html = BeautifulSoup(page, features=self.html_features)
		return html

	def get_xml_content(self, url): 
		try:
			xml = urllib.request.urlopen(url)
			content = xml.readlines()
			return content
		except urllib.error.URLError as e:
			print("URL Open Error", e)
			xml = urllib.request.urlopen(url)
			content = xml.readlines()
			return content


class EmailSender(object): 
	SENDER = "powerreport202009@gmail.com"
	RECEIVER = "powerreport202009@gmail.com"
	SUBJECT = 'Power Data Report'
	
	def send_emails(self, msg_list): 
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login("powerreport202009@gmail.com", "smartkids")
			for message in msg_list:
				msg = MIMEText(message)
				msg['From'] = EmailSender.SENDER
				msg['To'] = EmailSender.RECEIVER
				msg['Subject'] = EmailSender.SUBJECT
				server.sendmail(EmailSender.SENDER, EmailSender.RECEIVER, msg.as_string())
		
	
	def send_email(self, message): 
		msg = MIMEText(message)
		msg['From'] = EmailSender.SENDER
		msg['To'] = EmailSender.RECEIVER
		msg['Subject'] = EmailSender.SUBJECT

		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login("powerreport202009@gmail.com", "smartkids")
			server.sendmail(EmailSender.SENDER, EmailSender.RECEIVER, msg.as_string())