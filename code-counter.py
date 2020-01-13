import os


class CounterNode:

	def __init__(self, path, parent=None):
		self.path = path
		self.parent_node = parent
		self.child_nodes = []
		self.files = []

		self.index()
		print(self)

	def __repr__(self):
		return self.path + str(self.files)

	def index(self):
		_, dirnames, filenames = next(os.walk(self.path))
		self.files = filenames

		for directory in ignored_directories:
			if directory in dirnames:
				dirnames.remove(directory)

		for dirname in dirnames:
			new_child = CounterNode(os.path.join(self.path, dirname), self)
			self.child_nodes.append(new_child)

	def count(self):
		pass


if __name__ == "__main__":
	ignored_directories = [".git", ".idea", "__pycache__", "dist", "build"]
	master = CounterNode(input("Root directory: "))
