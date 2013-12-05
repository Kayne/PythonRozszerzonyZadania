from bs4 import BeautifulSoup
import os

class WWWChecker:
	def __init__(self, catalog):
		self.files = {}
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
		temp = ""
		for root, dirs, files in os.walk(catalog):
			for file in files:
				if file.endswith(".html"):
					fd = open(os.path.join(root, file), 'r')
					data = fd.read()
					fd.close()
					soup = BeautifulSoup(data)

					for link in soup.find_all('a'):
						temp = link.get('href')
						if temp is not None:
							try:
								self.files[temp].add(file)
							except KeyError:
								self.files[temp] = set([file])
					for link in soup.find_all('img'):
						temp = link.get('src')
						if temp is not None:
							try:
								self.files[temp].add(file)
							except KeyError:
								self.files[temp] = set([file])