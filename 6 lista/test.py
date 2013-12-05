#encoding: utf-8
import WWWViewer
import WWWChecker

test = WWWViewer.WWWViewer("/Users/kayne/portfoilo")
print "To są wszystkie znalezione linki:"
print test.showAllLinks()


test.checkAllLinksWithMultithreading()

print "To są wszystkie działające linki:"
print test.showAllWorkingLinks()
print "To są zepsute linki:"
print test.showAllBrokenLinks()

print "###"
print "Teraz sprawdźmy, które pliki są odnośnikami do innych plików:"
cos = WWWChecker.WWWChecker("/Users/kayne/portfoilo")
print cos.showDatabase()