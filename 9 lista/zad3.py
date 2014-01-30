#encoding: utf-8


class Zdania:
    """
    Klasa pozwalająca na rozbijanie tekstu na poszczególne zdanie,
    dostęp do nich jako do iteratora i ich poprawę.
    """

    def __init__(self, tekst):
        """
        Pobiera tekst i od razu zmienia na zdania.
        """
        self.tekst = self.intoSentences(tekst)
        self.iterator = 1
        self.tekstLength = len(self.tekst)
        self.tekst = [x.strip() for x in self.tekst]

    def next(self):
        """
        Zwraca następne zdanie
        """
        if self.iterator > self.tekstLength:
            self.iterator = 1
            raise StopIteration
        iterator = self.iterator
        self.iterator += 1
        return self.tekst[iterator-1]

    def __iter__(self):
        return self

    def intoSentences(self, paragraph):
        """
        Zmienia podany tekst na zdania, zakładając,
        że każde kolejne zdanie kończy się
        kropką, wykrzyknikiem lub znakiem zapytania
        """
        import re
        sentenceEnders = re.compile('[.!?]')
        sentenceList = sentenceEnders.split(paragraph)
        sentenceList = filter(lambda x: not re.match(r'^\s*$', x), sentenceList)
        return sentenceList

    def korekta(self, zdanie):
        """
        Poprawia podane zdanie.
        """
        zdanie = zdanie.capitalize()
        zdanie += ". "
        return zdanie

    def correctMe(self):
        """
        Poprawia wszystkie zdania w klasie
        """
        self.tekst = [self.korekta(x) for x in self.tekst]
        return self

if __name__ == "__main__":
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
