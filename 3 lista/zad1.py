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


#print pierwsze_skladane(13000)
print pierwsze_funkcyjne(13000)