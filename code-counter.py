import os


class CounterNode:

	def __init__(self, path, parent=None):
		self.path = path
		self.parent_node = parent
		self.child_nodes = []
		self.files = []
		self.line_counts = {}

		self.index()
		self.count()
		self.merge()

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

		for directory in ignored_directories:
			if directory in dirnames:
				dirnames.remove(directory)

		for dirname in dirnames:
			new_child = CounterNode(os.path.join(self.path, dirname), self)
			self.child_nodes.append(new_child)

	def count(self):  # TODO: count method not counting newlines at end of file
		for file in self.files:
			path_split = os.path.splitext(file)
			file_type = (path_split[1] if not path_split[1] == "" else path_split[0])
			line_count = 0
			with open(file) as f:
				try:
					for _ in f:
						line_count += 1
				except UnicodeDecodeError:
					pass  # TODO: Fix this
			try:
				self.line_counts[file_type] += line_count
			except KeyError:
				self.line_counts[file_type] = line_count

	def merge(self):
		if self.parent_node is not None:
			for file_type in self.line_counts:
				try:
					self.parent_node.line_counts[file_type] += self.line_counts[file_type]
				except KeyError:
					self.parent_node.line_counts[file_type] = self.line_counts[file_type]


if __name__ == "__main__":
	ignored_directories = [".git", ".idea", "__pycache__", "dist", "build"]
	master = CounterNode(input("Root directory: "))
	print(master)
