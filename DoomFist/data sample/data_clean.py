def get(st):
    k = st.strip().split(':')
    k[0] = k[0][1:len(k[0]) - 1]
    if(k[0] in ['gx','gy','gz','ax','ay','az']):
        k[1] = float(k[1])
    else:
        k[1] = -99999999999
    return (k[0],k[1])
f = open('charge_dataset2_real.txt','r')
w = open('charge_out.txt','w+')
data = []
a = []
cnt = 0
for line in f:
    if(line.find('end') != -1):
        if(len(a) > 30) : a = a[:30]
        if(len(a) == 30): data.append(a)
        a = []
    else:
        a += [float(e) for e in line.split()]
print(data)
            
