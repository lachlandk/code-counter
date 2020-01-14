from os import path
import sys
import json


class Counter:

	def __init__(self, file):
		self.path = file
		self.type = None
		self.result = ()

		self.identify_filetype()
		self.count()
		# TODO: turn count method into generator

	def identify_filetype(self):
		file_type = path.splitext(self.path)[1] if not path.splitext(self.path)[1] == "" else path.split(self.path)[1]

		if hasattr(sys, '_MEIPASS'):
			langs_json = path.join(sys._MEIPASS, "langs.json")
		else:
			langs_json = path.join(path.abspath("."), "langs.json")
		with open(langs_json, "r") as f:
			langs = json.load(f)
			try:
				self.type = langs[file_type]["type"]
			except KeyError:
				self.type = file_type

	def count(self):
		line_count = 0
		try:
			with open(self.path, "r", encoding="utf-8") as f:
				for _ in f:
					line_count += 1
				self.result = (self.type, line_count)
		except UnicodeDecodeError:
			# Not a text file
			pass
