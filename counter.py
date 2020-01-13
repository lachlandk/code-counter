import os


class Counter:

	def __init__(self, file):
		self.path = file
		self.result = ()
		self.count()
		# TODO: turn count method into generator

	def count(self):  # TODO: count method not counting newlines at end of file
		path_split = os.path.splitext(self.path)
		file_type = (path_split[1] if not path_split[1] == "" else path_split[0])
		line_count = 0
		with open(self.path) as f:  # TODO: check if file is binary or not (ignored filetypes?)
			try:
				for _ in f:
					line_count += 1
			except UnicodeDecodeError:
				pass  # TODO: Fix this
		self.result = (file_type, line_count)


if __name__ == "__main__":
	count = Counter(input("Path to file: "))
