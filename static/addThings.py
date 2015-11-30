f=open('stop-word-list.csv','r')
fr=f.read()
a=fr.split(',')
for i in range(len(a)):
    a[i]=a[i].strip(' ')
#print a
f.close()

n=open('nounlist.txt')
b=[]
for l in n:
    b.append(l)
for i in range(len(b)):
    b[i]=b[i].strip('\n')

n.close()
#print b

#c is all nouns
c=a+b
#print c

#print s
fem=open('first-names.txt','r')
femlist=[]
for l in fem:
    femlist.append(l)
for i in range(len(femlist)):
    femlist[i]=femlist[i].strip('\r\n').lower()
#print femlist

mas=open('middle-names.txt','r')
maslist=[]
for l in mas:
    maslist.append(l)
for i in range(len(maslist)):
    maslist[i]=maslist[i].strip('\r\n').lower()
print maslist

allnames=femlist+maslist
#print allnames

last=[]
for el in c:
    if el=='margaret':
        print 'MARGARET!===================================================='
    if el not in allnames:
        last.append(el)
    #else:
        #print "name: "+el

print last
s=''
for el in last:
    s=s+el+', '
s=s[:-2]
#print s
final=open('stop3.csv','w')
final.write(s)
