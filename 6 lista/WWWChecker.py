from bs4 import BeautifulSoup
import os
import threading

class checkTags(threading.Thread):
	def __init__(self, WWWChecker, file, root):
		threading.Thread.__init__(self)
		self.WWWChecker = WWWChecker
		self.file = file
		self.root = root

	def run(self):
		temp = ""
		if self.file.endswith(".html"):
			fd = open(os.path.join(self.root, self.file), 'r')
			data = fd.read()
			fd.close()
			soup = BeautifulSoup(data)
			for link in soup.find_all('a'):
				temp = link.get('href')
				if temp is not None:
					try:
						WWWChecker.files[temp].add(self.file)
					except KeyError:
						WWWChecker.files[temp] = set([self.file])
			for link in soup.find_all('img'):
				temp = link.get('src')
				if temp is not None:
					try:
						WWWChecker.files[temp].add(self.file)
					except KeyError:
						WWWChecker.files[temp] = set([self.file])

class WWWChecker:
	files = {}
	def __init__(self, catalog):
		self.getDatabase(catalog)

	def showDatabase(self):
		return self.files

	def showFormattedDatabase(self):
		for key, value in self.files.iteritems():
			print key + " - ",
			for every in value:
				print value,
			print ""

	def getDatabase(self, catalog):
		threads = []
		for root, dirs, files in os.walk(catalog):
			for file in files:
				threads.append(checkTags(self, file, root))
				threads[-1].start()

		for t in threads:
		    t.join()