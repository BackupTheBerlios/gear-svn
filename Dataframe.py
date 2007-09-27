def LoadCsv(filename, separator=','):
""" Read a file with an arbitrary number of columns.
The type of data in each column is arbitrary
It will be cast to the given dtype at runtime
"""
myfile = open(filename, "r")
contents = myfile.readlines()
myfile.close()
l = contents[0].strip().split('"')[1:]
colnames = l[0:len(l):2]
colnames.insert(0, 'Time')
vars = contents[1].strip().split(separator)
ltypes = [] # the first colums is a string representing a date
for v in vars:
try:
float(v)
ltypes.append('float')
except ValueError:
ltypes.append('S20')
dtype = N.dtype(zip(colnames, ltypes))
contents = contents[1:]
data = [[] for dummy in xrange(len(dtype))]
for line in contents:
fields = line.strip().split(separator)
for i, number in enumerate(fields):
data[i].append(number)
print data[0]
for i in xrange(len(dtype)):
data[i] = N.cast[dtype[i]](data[i])
return N.rec.array(data, dtype=dtype), dtype
19:36 
S20
