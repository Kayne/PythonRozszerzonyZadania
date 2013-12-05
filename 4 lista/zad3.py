class Zdania:
   def __init__(self, tekst):
      self.tekst = self.intoSentences(tekst)
      self.iterator = 1
      self.tekstLength = len(self.tekst)
      self.tekst = [x.strip() for x in self.tekst]
      #print self.tekst, self.tekstLength

   def next(self):
      if self.iterator > self.tekstLength:
         self.iterator = 1
         raise StopIteration
      iterator = self.iterator
      self.iterator += 1
      return self.tekst[iterator-1]

   def __iter__(self):
      return self

   def intoSentences(self, paragraph):
      import re
      sentenceEnders = re.compile('[.!?]')
      sentenceList = sentenceEnders.split(paragraph)
      sentenceList = filter(lambda x: not re.match(r'^\s*$', x), sentenceList)
      return sentenceList

   def korekta(self, zdanie):
      zdanie = zdanie.capitalize()
      zdanie += ". "
      return zdanie

   def correctMe(self):
      self.tekst = [self.korekta(x) for x in self.tekst]
      return self


test = Zdania("To jest bardzo fajne zdanie. ktore, nie jest zbyt dlugie. Za to bardzo je lubie... Co o tym sadzisz?")

print "### Normalne: ###"
for i in test:
	print i

print "### Po korekcie: ###"
skorygowane = Zdania("".join([test.korekta(i) for i in test]))
for x in [test.korekta(i) for i in test]:
   print x

print "### Oryginal po skorygowaniu: ###"
test.correctMe()
for i in test:
   print i

print "### Od nowa, z jednym wyjatkiem: ###"
test = Zdania("To jest bardzo fajne zdanie. ktore, nie jest zbyt dlugie. Za to bardzo je lubie... Co o tym sadzisz?")
for i in test.correctMe():
   print i