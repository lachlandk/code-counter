import os


class CounterNode:

	def __init__(self, path, parent=None):
		self.path = path
		self.parent_node = parent
		self.child_nodes = []
		self.files = []
		self.line_counts = []

		self.index()
		self.count()
		print(self)

	def __repr__(self):
		return self.path + str(self.files)

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

	def count(self):
		for file in self.files:
			line_count = 0
			with open(file) as f:
				try:
					for _ in f:
						line_count += 1
				except UnicodeDecodeError:
					pass  # TODO: Fix this
			if self.parent_node is not None:  # TODO: get rid of this, identifier for master node
				notfound = True
				master_node = self.parent_node
				while notfound:
					if master_node.parent_node is None:
						notfound = False
					else:
						master_node = master_node.parent_node
				master_node.line_counts.append((file, line_count))
			else:
				self.line_counts.append((file, line_count))


if __name__ == "__main__":
	ignored_directories = [".git", ".idea", "__pycache__", "dist", "build"]
	master = CounterNode(input("Root directory: "))
	print(master.line_counts)
