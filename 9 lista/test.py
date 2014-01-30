#encoding: utf-8
import unittest
import zad1
import zad3


class TestZad1PrimesGenerator(unittest.TestCase):
    """
    Test generowania liczb pierwszych przy pomocy generatorów
    """

    def runTest(self):
        oczekiwane = [2, 3, 5, 7]
        wynik = zad1.pierwsze_generator(10)
        assert oczekiwane == wynik, 'primes are not generated correctly'

class TestZad1PrimesComprehension(unittest.TestCase):
    """
    Test generowania liczb pierwszych przy pomocy list składanych
    """

    def runTest(self):
        oczekiwane = [2, 3, 5, 7]
        wynik = zad1.pierwsze_skladane(10)
        assert oczekiwane == wynik, 'primes are not calculated correctly'


class TestZad1PrimesFunction(unittest.TestCase):
    """
    Test generowania liczb pierwszych przy pomocy zwykłych funkcji
    """

    def runTest(self):
        oczekiwane = [2, 3, 5, 7]
        wynik = zad1.pierwsze_skladane(10)
        assert oczekiwane == wynik, 'primes are not calculated correctly'


class TestZad3Iterator(unittest.TestCase):
    """
    Test iteratora Zdania
    """

    def setUp(self):
        """
        Ustawia tekst
        """
        self.zdania = zad3.Zdania("To jest bardzo fajne zdanie. ktore, nie jest zbyt dlugie. Za to bardzo je lubie... Co o tym sadzisz?")

    def runTest(self):
        """
        Uruchamia testy
        """
        self.splitting()
        self.nextIterator()
        self.korekta()
        self.correctMe()

    def splitting(self):
        """
        Testuje podział tekstu na zdania
        """
        oczekiwane = ['To jest bardzo fajne zdanie', 'ktore, nie jest zbyt dlugie', 'Za to bardzo je lubie', 'Co o tym sadzisz']
        assert oczekiwane == self.zdania.tekst, 'sentences aren\'t splitted correctly'

    def nextIterator(self):
        """
        Testuje działanie iteratora
        """
        self.zdania.next()
        assert "ktore, nie jest zbyt dlugie" == self.zdania.next(), 'next iterator is broken'

    def korekta(self):
        """
        Testuje korektę pojedynczego zdania
        """
        assert "Za to bardzo je lubie. " == self.zdania.korekta(self.zdania.next()), 'correcting doesn\'t work'

    def correctMe(self):
        """
        Testuje korektę wszystkich zdań
        """
        oczekiwane = ['To jest bardzo fajne zdanie. ', 'Ktore, nie jest zbyt dlugie. ', 'Za to bardzo je lubie. ', 'Co o tym sadzisz. ']
        assert oczekiwane == self.zdania.correctMe().tekst, 'correcting all words aren\'t working'


if __name__ == "__main__":
    s1 = TestZad1PrimesGenerator()
    s2 = TestZad1PrimesComprehension()
    s3 = TestZad1PrimesFunction()

    s4 = TestZad3Iterator()

    alltests = unittest.TestSuite([s1, s2, s3, s4])
    unittest.TextTestRunner(verbosity=3).run(alltests)
