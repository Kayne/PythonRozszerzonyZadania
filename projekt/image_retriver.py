#encoding: utf-8
from bs4 import BeautifulSoup
import urllib


class ImageRetriver:
    """
    Pobieranie tapet z serwisu 4Chan
    """

    def __init__(self, url='http://boards.4chan.org/wg/', sites=0, counter=0, path=''):
        """
        Ustawiamy zmienne
        """
        self.counter = counter
        self.url = url
        self.sites = sites + 1
        self.path = path

    def retriveAll(self):
        """
        Pobieramy wszystkie tapety ze wszystkich stron
        """
        for page in xrange(self.sites):
            self.retrive(page, self.path)

    def retrive(self, page):
        """
        Pobieramy tapety z wskazanej strony
        """
        self.soup = BeautifulSoup(urllib.urlopen(self.url+str(page)).read())
        results = self.soup.findAll("a", {"class": "fileThumb"})
        return self.downloadImages(results)

    def downloadImages(self, results):
        """
        Ściąga grafiki z wskazanych adresów i zwraca listę nazw plików z ściężką dostępu
        """
        result = []
        for link in results:
            urllib.urlretrieve("http:" + link.get('href'), self.path + "/" + str(self.counter) + ".jpg")
            result.append(str(self.counter) + ".jpg")
            self.counter += 1
        return result
