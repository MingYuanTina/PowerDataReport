#!/usr/local/bin/python3
from collections import defaultdict

# TODO: 
# 1. [DONE] import parser to script.py
# 2. parse xml file into map [key=title, values=(groups of items)]
# 3. comparator functionality
# 4. parse output etc. 

class Item:
	INTERFACE_DATA = "<InterfaceData>\n"
	INTERFACE_NAME = "InterfaceName"
	ISSUE_DATE = "IssueDate"
	START_DATE = "StartDate"
	END_DATE = "EndDate"
	OPERATIN_LIMIT = "OperatingLimit"
	COMMENTS = "Comments"

	def __init__(self):
		self.issue_date = "" 
		self.start_date = ""
		self.end_date = ""
		self.operating_limit = ""
		self.comments = ""


class Parser: 
	def __init__(self, content):
		self.dic = defaultdict(Item)
		self.xml_content = content
		self.column_size = 5;

		pass

	def parse_content(self):
		i = 14
		while i < len(self.xml_content)
			row_title = xml1[i+1].decode("utf-8").replace("<InterfaceName>", "").replace("</InterfaceName>", "")
			for j in range(i + 2, i + 7):
		

		while i < len(xml1):
			if (xml1[i].decode("utf-8") == "<InterfaceData>\n"):
				item = Item()
				rowTitle = xml1[i+1].decode("utf-8").replace(open_tag(Item.INTERFACE_NAME), "").replace(end_tag((Item.INTERFACE_NAME)), "")
				print(rowTitle)
				# for j in range(i + 2, i + 7):
				# 	if (xml1[j] != xml2[j]):
				# 		old_line = "Older: " + xml2[j].decode("utf-8")
				# 		new_line = "Latest: " + xml1[j].decode("utf-8")
				# 		diff = diff + rowTitle + old_line + new_line
				# i = i + 7
			i += 1

	def open_tag(self, content):
		"<" + content  + ">"

	def end_tag(self, content):		
		"</" + content  + ">"

	def add_item(self, item):
		self.dic[1] = item



	def test(self): 
		print("This is a test")
		print(self.dic[1].issue_date)
		print(self.dic[1].start_date)
		print(self.dic[1].end_date)
		print(self.dic[1].operating_limit)
		print(self.dic[1].comments)


parser = Parser()
item = Item("2020-09-09T19:41:18", "2020-08-21T21:00:00", "2020-12-31T23:59:00", "100", "Internal system conditions")
parser.add_item(item)
parser.test()
