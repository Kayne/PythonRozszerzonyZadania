import timeit
def pierwsze_generator(n):
  def generuj(n):
    yield 2
    i = 2
    while i <= n:
      i += 1
      for p in generuj(n):
        if p*p > i:
            yield i
            break
        if (i%p)==0:
            break
  return [x for x in generuj(n)]


def pierwsze_skladane(n):
  return [x for x in xrange(2,n) if not [y for y in xrange(2, int(x**0.5)+1) if x%y ==0]]

def pierwsze_funkcyjne(n):
  def isPrime(n):
    i = 2
    if n < 2:
        return False
    while i < n:        
        if n % i == 0:
            return False
        else:
            i += 1
    return True
  return filter(isPrime, [x for x in xrange(n)])


def porownajFunkcje(start, stop, step):
  time1 = 0
  time2 = 0
  time3 = 0
  digits = len(str(stop))
  print "%*s | %*s | %*s | %*s" % (digits, "", 9, "Funkcyjna", 9, "Skladana", 9, "Generator")
  while start <= stop:
    # Funkcyjna
    startTime = timeit.default_timer()
    pierwsze_funkcyjne(start)
    stopTime = timeit.default_timer()
    time1 = stopTime - startTime
    # Skladana
    startTime = timeit.default_timer()
    pierwsze_skladane(start)
    stopTime = timeit.default_timer()
    time2 = stopTime - startTime
    # Generator
    startTime = timeit.default_timer()
    pierwsze_generator(start)
    stopTime = timeit.default_timer()
    time3 = stopTime - startTime
    print "%*d | %*f | %*f | %*f" % (digits, start, 9, time1, 9, time2, 9, time3)
    start *= step

porownajFunkcje(10, 100000, 10)

#print pierwsze_skladane(13000)
#print pierwsze_funkcyjne(13000)
#print pierwsze_generator(13000)