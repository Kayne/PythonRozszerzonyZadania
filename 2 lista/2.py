#coding: utf-8
class ObiektyDodawalne:
	def __add__(a, b):
		nowy = ObiektyDodawalne()
		for variable, value in a.__dict__.iteritems():
			nowy.__dict__[variable] = value
		for variable, value in b.__dict__.iteritems():
			if variable in nowy.__dict__:
				print "** UWAGA! Istnieje już pole '" + variable + "'. Nadpisuję je! **"
			nowy.__dict__[variable] = value
		return nowy

class JakisObiekt(ObiektyDodawalne):
	def __init__(self):
		self.haslo = "Tajne"
		self.user = "User1"

	def zmienHaslo(self, zmienione):
		self.haslo = zmienione

class InnyObiekt(ObiektyDodawalne):
	def __init__(self):
		self.haslo = "Super!Tajne"

nic = JakisObiekt()
cos = InnyObiekt()
qos = JakisObiekt()
qos.zmienHaslo("noweHaslo!")
w = cos + qos

print nic.__dict__
print cos.__dict__
print qos.__dict__
print w.__dict__