from bs4 import BeautifulSoup
from urllib2 import urlopen, URLError, HTTPError
import os

import threading

class checkLinkThread(threading.Thread):
	def __init__(self, WWWViewer, link):
		threading.Thread.__init__(self)
		self.WWWViewer = WWWViewer
		self.link = link

	def run(self):
		self.WWWViewer.checkLink(self.link)

class WWWViewer:
	def __init__(self, catalog):
		self.links = self.getLinksFromSite(catalog)
		self.workingLinks = set()
		self.brokenLinks = set()
		self.catalog = catalog

	def showAllLinks(self):
		return self.links

	def showAllWorkingLinks(self):
		return self.workingLinks

	def showAllBrokenLinks(self):
		return self.brokenLinks

	def getLinksFromSite(self, catalog):
		links = set()
		for root, dirs, files in os.walk(catalog):
			for file in files:
				if file.endswith(".html"):
					fd = open(os.path.join(root, file), 'r')
					data = fd.read()
					fd.close()
					soup = BeautifulSoup(data)
					for link in soup.find_all('a'):
						links.add(link.get('href'))
					for link in soup.find_all('img'):
						links.add(link.get('src'))
		return [x for x in links if x is not None]

	def checkLink(self, link):
		code = 404
		if self.isValidUrl(link):
			try:
				code = urlopen(link).code
			except (URLError, HTTPError):
				pass
			if (code / 100 < 4):
				self.workingLinks.add(link)
			else:
				self.brokenLinks.add(link)
		elif link.startswith("#") or link.startswith("mailto:"):
			self.workingLinks.add(link)
		else:
			if os.path.isfile(os.path.join(self.catalog, link)):
				self.workingLinks.add(link)
			else:
				self.brokenLinks.add(link)

	def checkAllLinks(self):
		for link in self.links:
			self.checkLink(link)

	def checkAllLinksWithMultithreading(self):
		threads = []
		for link in self.showAllLinks():
			threads.append(checkLinkThread(self, link))
			threads[-1].start()

		for t in threads:
		    t.join()

	def isValidUrl(self, url):
	    import re
	    regex = re.compile(
	        r'^https?://'  # http:// or https://
	        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
	        r'localhost|'  # localhost...
	        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
	        r'(?::\d+)?'  # optional port
	        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	    return url is not None and regex.search(url)