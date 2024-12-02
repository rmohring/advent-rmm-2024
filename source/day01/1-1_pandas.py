import pandas as pd

#fh = open('1_test.dat', 'r')
fh = open('1_1.dat', 'r')

df = pd.read_csv('1_1.dat', sep="\s+", header=None)
df.columns = ['x','y']

x = df.sort_values('x')['x']
y = df.sort_values('y')['y']

print(x.head())
print(y.head())

diff = 0
for a,b in zip(x,y):
    diff += abs(a-b)

print(diff)