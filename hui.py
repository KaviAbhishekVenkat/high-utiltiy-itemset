from __future__ import print_function
import time
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.image import AxesImage
from matplotlib import style
import numpy as np
import csv
list=[]
style.use('fivethirtyeight')  
with open('price.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        list.append(int(row[0]))
def draw(array,price,title):
        plt.rcParams['font.size']=8.0
        labels=[j[1] for j in array]
        sizes=[j[0] for j in array]
        time=[j[2] for j in array]
        #print (time)
        explode=[j[0]/1000 for j in array]
        fig1, (ax1,ax2) = plt.subplots(1,2)
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90) 
        ax1.set_title('Frquency')
        ax2.bar(labels,time) 
        ax2.set_title('Time')
        plt.show()  
def highUtiltiy(Table,dsit,tHold,lines):
    ordered = []
    time=[]
    factor=[]
    price=[]
    mean=0
    for i in Table:
        if Table[i] > (len(lines) * tHold):
            ordered.append([Table[i], i,dsit[i]])
            time.append([dsit[i],i])
            factor.append([Table[i]*dsit[i],i])
    ordered.sort(reverse=True)
    factor.sort(reverse=True)
    time.sort(reverse=True)
    max_utlity=0
    min_utlity=10000000000000
    for i in ordered:
            a=i[1].split(',')
            b=[int(j) for j in a]
            pc=0
            for h in b:
                pc=pc+list[h]
            if pc>max_utlity:
                max_utlity=pc
            if pc<min_utlity:
                min_utlity=pc            
            price.append(pc)

    for x in factor:
        mean+=x[0]
    mean=mean/len(factor)
    draw(ordered,price,'after apriori')
    tot = 0
    print('itemset before high uility pruning and after applying apriori-')
    print('(X,Y..:frequency)')
    for i in ordered:
        tot += 1
        print(tot, ')', i[1], ':', i[0])
    tot=0
    print('1.enter range {0} to {1}  2.enter item numbers. 3.AutoPrune'.format(min_utlity,max_utlity))
    opt=int(input())
    if(opt==1):
        loc=[]
        print('enter threshold for high utilty =')
        thr=int(input())
        print('itemset after pruning-')
        print('(X,Y..:frequency)')
        for i,j in zip(ordered,range(0,len(price))):
            if((price[j])>thr):
                loc.append(j)
                tot += 1
                print(tot, ')', i[1], ':', i[0], 'time-',i[2], 'factor-',i[0]*i[2])       
                print ('item set price->{0}rs and the total sale ->{1}'.format(price[j],price[j]*i[0]))
            #print(b)
        temp1=[ordered[a] for a in loc]
        temp2=[price[a] for a in loc]
        #label=[j[1] for j in temp1]
        fer_var1=[j[0] for j in temp1]
        tim_var2=[j[2] for j in temp1]
        temp3=[i[0]*j/10000 for i,j in  zip(temp1,temp2)]
        #factor_new=[i*j for i,j in zip(fer_var1,tim_var2)]        
        x, y, c, s = rand(4, len(fer_var1))       
        draw(temp1,temp2,'new')
        index=[]
        def onpick3(event):
            ind = event.ind
            index.append(ind[0])
            print('onpick3 scatter:', ind, np.take(fer_var1, ind), np.take(tim_var2, ind))
        fig, ax = plt.subplots()
        col = ax.scatter(fer_var1, tim_var2,temp3,c, picker=True)
        ax.set_title('Time vs Frequency vs Profit')
        #fig.savefig('pscoll.eps')
        fig.canvas.mpl_connect('pick_event', onpick3)
        #plt.set_title('Time vs Frequency vs Profit')
        plt.show()
        print('The selected itemsets are-')
        print([temp1[j][1] for j in index ])
    elif(opt==2):
        print('enter item numbers (Eg-x,y,z,..)')
        opt=input()
        temp=opt.split(',')
        list_hui=[int(j) for j in temp]
        print(list_hui)
        for i in ordered:
            a=i[1].split(',')
            b=[int(j) for j in a]
            for x in list_hui:
                if(x in b):
                    tot += 1
                    print(tot, ')', i[1], ':', i[0])
                    break
    else:
        tot=0
        x=[(a[0]) for a in time]
        y=[a[0] for a in ordered]
        plt.scatter(x,y,marker='^')
        plt.show()
        for i in factor:
            if(i[0]>mean ):
                tot += 1
                print(tot, ')',i[1], ':factor-', i[0])
def apriori(baskets, tHold, start):
    C1 = {}
    for transaction in baskets:
        for item in transaction.split():
            if item not in C1:
                C1[item] = 1
            else:
                C1[item] += 1
    '''print('Initial frequency of items-')
    print(C1)'''	
    # Generate frequent itemset L1 from C1
    L1 = {}
    for key in C1:
        if C1[key] > (len(baskets) * tHold):
            L1[key] = C1[key]
    
    # Display L1
    print("items above threshold -L1")
    print(L1)
    print(" ")
def frequentTriples(dataset, tHold):
    myFile = open(dataset)
    triplesTable = {}
    triplesdsit = {}
    lines = myFile.readlines()
    print("L3")
    for line in lines:
        for item1 in line.split():
            for item2 in line.split():
                for item3 in line.split():
                    if (item1 < item2 and item2 < item3):
                        sub=line[line.find(item1)+1:line.find(item3)]
                        if (item1 +','+ item2 +','+ item3) not in triplesTable:
                            triplesTable[item1 +','+ item2 +','+ item3] = 1
                            triplesdsit[item1 +','+ item2 +','+ item3]=len(sub)
                        else:
                            triplesTable[item1 +','+ item2 +','+ item3] += 1
                            triplesdsit[item1 +','+ item2 +','+ item3]=(int(triplesdsit[item1 +','+ item2 +','+ item3]+ len(sub))/len(triplesdsit))*100
    highUtiltiy(triplesTable,triplesdsit,tHold,lines)   
def frequentDoubles(dataset, tHold):
    print("L2")
    myFile = open(dataset)
    pairsTable = {}
    lines = myFile.readlines()
    pairsTable = {}
    pairdist={}
    for line in lines:
        for item1 in line.split():
            for item2 in line.split():
                if (item1 < item2):
                    sub=line[line.find(item1)+1:line.find(item2)]
                    if (item1 +','+ item2) not in pairsTable:
                        pairsTable[item1 +','+ item2] = 1
                        pairdist[item1 +','+ item2] = len(sub)
                        
                    else:
                        pairsTable[item1 +','+ item2] += 1
                        pairdist[item1 +','+ item2] =(int(pairdist[item1 +','+ item2]+ len(sub))/len(pairdist))*100
    highUtiltiy(pairsTable,pairdist,tHold,lines)

print('------------------------------------------------------------------------')
print('Running...')
print('Done!')
def runData(tHold):
    dataset_file = 'data.dat'
    basket = []
        
    count = 0
    with open(dataset_file) as file:
        for line in file:
            basket.append(line)
            if count > 1382:
                break
            count += 1
    
    # Start the clock
    start = time.time() 
    apriori(basket, tHold, start)
    end = time.time()
    print('Time taken in seconds for basket:', end - start)
threshold = 0.03 # minimum support threshold
runData(0.03)
# Start the clock
start = time.time() 
frequentDoubles('data.dat',threshold)
end = time.time()

print('Time taken in seconds for frequent doubles:', end - start)
print('Done!')

print('------------------------------------------------------------------------')
print('Running...')
print('Done!')

# Start the clock

start = time.time() 
frequentTriples('data.dat',threshold)
end = time.time()

print('Time taken in seconds for frequent triples:', end - start)
print('Done!')