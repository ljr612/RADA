# python plddt_calculate.py <file_neme>

import sys

f = open(sys.argv[1], "r")
name = sys.argv[1].split('/')[-1].split('.')[0]
lh = int(name[1:3])-2
sum = 0.0
num = 0

sumh1 = 0.0
sumh2 = 0.0
sumh3 = 0.0
suml1 = 0.0
suml2 = 0.0
suml3 = 0.0

numh1 = 0
numh2 = 0
numh3 = 0
numl1 = 0
numl2 = 0
numl3 = 0



for line in f:
    l = line.split()
    if len(l)== 12 :
        a = float(l[10])
        b = int(l[5])
        sum += a
        num += 1
        if l[4] == 'H' and b >= 31 and b <= 36:
            sumh1 += a
            numh1 += 1
        if l[4] == 'H' and b >= 50 and b <= 65:
            sumh2 += a
            numh2 += 1
        if l[4] == 'H' and b >= 98 and b <= 98 + lh:
            sumh3 += a
            numh3 += 1        
        if l[4] == 'L' and b >= 24 and b <= 35:
            suml1 += a
            numl1 += 1
        if l[4] == 'L' and b >= 51 and b <= 57:
            suml2 += a
            numl2 += 1            
        if l[4] == 'L' and b >= 90 and b <= 98:
            suml3 += a
            numl3 += 1            
            
    
    
rmsd=sum/num

rmsdh1=sumh1/numh1
rmsdh2=sumh2/numh2
rmsdh3=sumh3/numh3
rmsdl1=suml1/numl1
rmsdl2=suml2/numl2
rmsdl3=suml3/numh3

print(name,rmsd,rmsdh1,rmsdh2,rmsdh3,rmsdl1,rmsdl2,rmsdl3)