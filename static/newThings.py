A='A'
B=(chr(90))
print B

f=open('stop-word-list.csv','r')
fr=f.read()
a=fr.split(',')
for i in range(len(a)):
    a[i]=a[i].strip(' ')
a=a[:-1]
f.close()

cnum=65
alpha=[]
while cnum<91:
    fname='../CSV Format/'+chr(cnum)+' Words.csv'
    print fname
    f=open(fname, 'r')
    for line in f:
        alpha.append(line.strip('\n'))
    f.close()
    cnum+=1

master=alpha+a
print master

new=open('stop4.csv', 'w')
s=''
for el in master:
    s=s+el
    s=s+', '
    #print 'hi'
s=s[:-2]

new.write(s)
new.close()

