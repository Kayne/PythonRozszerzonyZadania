#coding: utf-8
def zaszyfruj(tekst, klucz):
	if (not klucz in range(0,256)):
		raise ValueError("Key must be in range [0;255]")
	return ''.join([chr(int(bin(ord(slowo)), 2) ^ int(bin(klucz), 2)) for slowo in tekst])

def odszyfruj(tekst, klucz):
	if (not klucz in range(0,256)):
		raise ValueError("Key must be in range [0;255]")
	return ''.join([chr(int(bin(ord(slowo)), 2) ^ int(bin(klucz), 2)) for slowo in tekst])

print zaszyfruj("Python", 7)
print odszyfruj(zaszyfruj("Python", 7), 7)