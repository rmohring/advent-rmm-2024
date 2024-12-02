#fh = open('1_test.dat', 'r')
fh = open('1_1.dat', 'r')

left_data = []
right_data = []
for line in fh.readlines():
    print(line)
    (l,r) = line.split("   ")
    left_data.append(int(l))    
    right_data.append(int(r))


left_data = sorted(left_data)
right_data = sorted(right_data)

diff = 0
for (x,y) in zip(left_data, right_data):
    diff += abs(y-x)

#print(list(zip(left_data, right_data)))

#print(diff)

