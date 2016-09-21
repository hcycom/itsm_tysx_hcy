from django.test import TestCase

# Create your tests here.



import string



for i in string.lowercase:
    print i

a = range(10)

b =[2,3,4,9,45.56]

b = set(b)
a = set(a)

print a.difference(b)

print b.difference(a)

print a & b


print list(b)