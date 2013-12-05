#coding: utf-8
import WWWViewer
import WWWChecker

print "Sprawdźmy najpierw wszystkie linki dla pewnej strony."
cos = WWWViewer.WWWViewer("/Users/kayne/portfoilo")
print "To są wszystkie znalezione linki:"
print cos.showAllLinks()
cos.checkAllLinks()
print "To są wszystkie działające linki:"
print cos.showAllWorkingLinks()
print "To są zepsute linki:"
print cos.showAllBrokenLinks()

print "###"
print "Teraz sprawdźmy, które pliki są odnośnikami do innych plików:"
cos = WWWChecker.WWWChecker("/Users/kayne/portfoilo")
print cos.showDatabase()