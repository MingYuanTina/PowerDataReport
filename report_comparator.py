#!/usr/local/bin/python3
from collections import defaultdict
import re

class ReportComparator: 	
	IMPORT_KEYWORD = "import"
	EXPORT_KEYWORD = "export"
	
	def __init__(self):
		self.diff = ""
		self.new_dic = defaultdict(ReportItem)
		self.old_dic = defaultdict(ReportItem)
	
	def _stripe_tag(self, index): 
		content = self.content[index].decode("utf-8")
		return re.sub('<[^>]+>', "", content).rstrip()

	def parse_content(self, content):
		i = 0
		self.content = content
		dic = defaultdict(ReportItem)
		while i < len(content):
			if (content[i].decode("utf-8") == ReportItem.INTERFACE_DATA):
				item = ReportItem(
					title=self._stripe_tag(i+1), 
					issue_date=self._stripe_tag(i+2), 
					start_date=self._stripe_tag(i+3), 
					end_date=self._stripe_tag(i+4), 
					operating_limit=self._stripe_tag(i+5), 
					comments=self._stripe_tag(i+6))
				dic[item.title] = item
				i += 7
			else:
				i += 1
		return dic
		
	def _difference(self, set1, set2, identifier):
		new_additioinals = set1.difference(set2)
		if (len(new_additioinals) != 0):
			self.diff += "Additional line(s) in " + identifier +" report:\n"
			for key in new_additioinals:
				if (identifier == "new"):
					self.diff += self.new_dic[key].__str__()
				else:
					self.diff += self.old_dic[key].__str__()
					
	def _intersection(self, set1, set2):
		intersection = set1.intersection(set2)
		for key in intersection:
			new_item = self.new_dic[key]
			old_item = self.old_dic[key]
			if_import_export = key.lower().find("import") != -1 or key.lower().find("export") != -1
			if if_import_export and new_item.__eq__(old_item) == False: 
				self.diff += "Differences at " + new_item.title + " :\n"
				self.diff += "New Report: " + new_item.__str__()
				self.diff += "Old Report: " + old_item.__str__() + "\n"
	
	def compare_content(self, new_content, old_content):
		self.new_dic = self.parse_content(new_content)
		self.old_dic = self.parse_content(old_content)
		
		set1 = set(self.new_dic.keys())
		set2 = set(self.old_dic.keys())
		self._difference(set1, set2, "new") # compute any additional lines in new report.
		self._difference(set2, set1, "old") # compute any additional lines in old report.
		self._intersection(set1, set2)		# compute any differences between existing lines in common.
		return self.diff
	

class ReportItem:
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
