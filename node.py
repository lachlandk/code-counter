import os
import json
import counter


class CounterNode:

	def __init__(self, path, parent=None, auto_report=False,):
		self.path = path
		self.parent_node = parent
		self.child_nodes = []
		self.files = []
		self.line_counts = {}

		self.index()
		self.count()
		self.merge()
		if auto_report:
			print(self)

	def __str__(self):
		results = "Results for /" + self.path + ":\n"
		results += "File Type | Number of Lines\n"
		results += "---------------------------\n"
		for line_count in self.line_counts:
			results += line_count + " | " + str(self.line_counts[line_count]) + "\n"
		return results

	def index(self):
		_, dirnames, filenames = next(os.walk(self.path))
		for filename in filenames:
			self.files.append(os.path.join(self.path, filename))

		with open("ignored.json", "r") as f:
			ignored_directories = json.load(f)["ignored"]
			for directory in ignored_directories:
				if directory in dirnames:
					dirnames.remove(directory)

		for dirname in dirnames:
			new_child = CounterNode(os.path.join(self.path, dirname), parent=self)
			self.child_nodes.append(new_child)

	def count(self):
		for file in self.files:
			try:
				file_type, line_count = counter.Counter(file).result
				try:
					self.line_counts[file_type] += line_count
				except KeyError:
					self.line_counts[file_type] = line_count
			except ValueError:
				# Not a text file
				continue

	def merge(self):
		if self.parent_node is not None:
			for file_type in self.line_counts:
				try:
					self.parent_node.line_counts[file_type] += self.line_counts[file_type]
				except KeyError:
					self.parent_node.line_counts[file_type] = self.line_counts[file_type]


if __name__ == "__main__":
	master = CounterNode(input("Root directory: "))
	print(master)
