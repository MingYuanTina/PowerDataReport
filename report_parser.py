#!/usr/local/bin/python3
from collections import defaultdict
import re

class Item:
	INTERFACE_DATA = "<InterfaceData>\n"
	def __init__(self, title, issue_date, start_date, end_date, operating_limit, comments):
		self.title = title
		self.issue_date = issue_date
		self.start_date = start_date
		self.end_date = end_date
		self.operating_limit = operating_limit
		self.comments = comments

	def __eq__(self, item):
		return (self.title == item.title 
			and self.issue_date == item.issue_date 
			and self.start_date == item.start_date 
			and self.end_date == item.end_date
			and self.operating_limit == item.operating_limit)
		
	def __str__(self):
		return "{0} | {1} | {2} | {3} | {4} | {5} \n".format(self.title, self.issue_date, 
			self.start_date, self.end_date, self.operating_limit, self.comments)

class Parser: 
	def __init__(self):
		self.content = ""
		
	def stripe_tag(self, index): 
		content = self.content[index].decode("utf-8")
		return re.sub('<[^>]+>', "", content).rstrip()

	def parse_content(self, content):
		i = 0
		self.content = content
		dic = defaultdict(Item)
		while i < len(content):
			if (content[i].decode("utf-8") == Item.INTERFACE_DATA):
				item = Item(
					title=self.stripe_tag(i+1), 
					issue_date=self.stripe_tag(i+2), 
					start_date=self.stripe_tag(i+3), 
					end_date=self.stripe_tag(i+4), 
					operating_limit=self.stripe_tag(i+5), 
					comments=self.stripe_tag(i+6))
				dic[item.title] = item
				i += 7
			else:
				i += 1
		return dic
