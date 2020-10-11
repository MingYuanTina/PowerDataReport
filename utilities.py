#!/usr/local/bin/python3
import smtplib, ssl
import urllib.request				# html inspector 
from bs4 import BeautifulSoup 	    # html parser
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
		xml = urllib.request.urlopen(url)
		content = xml.readlines()
		return content


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