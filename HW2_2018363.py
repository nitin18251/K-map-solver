# CSE 101 - IP HW2
# K-Map Minimization 
# Name:Sandeep kumar singh
# Roll Number:2018363
# Section:B
# Group:4
import copy

def num2bin(dec,numVar=4):#for conversion of a decimal no. to its binary equivalent
	bin=''
	while dec>1:
		i=int(dec%2)
		dec=int(dec/2)
		bin=str(i)+bin
	if dec==0:
		bin='0'
	else:
		bin='1'+bin
	bin=(numVar-len(bin))*'0'+ bin
	return bin

def diff1(b1,b2):# takes input in form of string i.e in binary and returns True if difference of bit is exactly 1
	diff=0
	for i in range(len(b1)):
		if b1[i]!=b2[i] :
			diff+=1
	if diff==1:
		return True
	return False

def split_n_d(s):#function to return normal and dont cares as two different lists
	nor=[] #normal minterms
	dor=[] #dont care
	if s.count('d')==0:
		s=s+'d'
	s=s.replace(" ","")
	d=s.split('d')
	
	d[0]=d[0].split(',')
	
	for i in d[0]:
		if i.isdigit():
			nor.append(int(i))
	
	d[1]=d[1].split(',')
	for i in d[1]:
		if i.isdigit():
			dor.append(int(i))
	nor.sort()
	dor.sort()
	return nor,dor

def remempty(g):#for removing empty lists from lists
	h=[i for i in g if len(i)!=0]
	return h

def remredun1(g):#remove redundancy from  1-D list
	new=[]
	for i in g:
		if i not in new:
			new.append(i)
	return new

def remredun2(g):#remove redundancy from 2-D list
	New=[]
	g.sort()
	for i in g:
		i.sort()
		if i not in New:
			New.append(i)
	
	return New

def min2var(min_b,numVar=4):#it takes min term in binary reduced(eg 1_01) form an return its corresponding alphabetic equivalent(eg wy`z)
	c=-1
	min_v=''
	variables='WXYZ'
	if numVar==3:
		variables=variables[:3]
	elif numVar==2:
		variables=variables[:2]
	
	if min_b=="_"*numVar:#if all positions consists of "_" then its reduced form is 1
		return '1'
	
	for i in min_b:
		c+=1
		if i=='0':
			min_v+=variables[c]+'`'
		elif i=='1':
			min_v+=variables[c]
	return min_v

def red(b1,b2):#takes input in form of string i.e in binary and returns reduced binary value in string with '_'
	c=-1
	if diff1(b1,b2):
		for i in range(len(b1)):
			c+=1
			if b1[i].isdigit() and b1[i]!=b2[i]:
				break
		
		red=b1[:c]+'_'+b1[c+1:]	
	else:
		print('non reducible',b1,b2)
		return None
	return red

def red4(a,b,c,d,numVar=4):#takes input in form of integers and returns reduced binary value in string with "-"
	a=num2bin(a,numVar)
	b=num2bin(b,numVar)
	c=num2bin(c,numVar)
	d=num2bin(d,numVar)
	if diff1(a,b) and diff1(c,d):
		e=red(a,b)
		f=red(c,d)
	elif diff1(a,c) and diff1(b,d):
		e=red(a,c)
		f=red(b,d)
	elif diff1(a,d) and diff1(b,c):
		e=red(a,d)
		f=red(c,b)
	g=red(e,f)
	return(g)

def step1(group,All_min,numVar):#reduction of groups on the basis of difference of no. bits in them

	w=0
	Remaining=All_min.copy()
	red_bin=[]
	red_min=[]
	while w<len(group)-1:
		for i in group[w+1]:
			for j in group[w]:
				if diff1(num2bin(i,numVar),num2bin(j,numVar)):
					red_bin.append(red(num2bin(i,numVar),num2bin(j,numVar)))
					red_min.append([j,i])
					if j in Remaining:
						Remaining.remove(j)
					if i in Remaining:
						Remaining.remove(i)
		w+=1
	return red_bin,red_min,Remaining #a is reduced binary value, x is represents the minterms which were reduced, and h represents which minterms left without reduction

def step2(red_bin1,red_min1):#almost works same as above
	w=0
	
	red_min_c=copy.deepcopy(red_min1)
	red_bin2=[]
	red_min2=[]
	
	for i in red_bin1:
		for j in red_bin1[w:]:
			if diff1(i,j):			
				red_bin2.append(red(i,j))
				red_min2.append(red_min1[red_bin1.index(j)]+red_min1[red_bin1.index(i)])
				if red_min1[red_bin1.index(j)] in red_min_c :						
					red_min_c.remove(red_min1[red_bin1.index(j)])
				if red_min1[red_bin1.index(i)] in red_min_c:
					red_min_c.remove(red_min1[red_bin1.index(i)])	
	w+=1
	
	red_bin2=remredun1(red_bin2)
	red_min2=remredun2(red_min2)
	return red_bin2,red_min2,red_min_c

def step3(red_bin2,red_min2):#almost works same as above. it is not needed in many cases but since this program is general in nature thats why needed
	w=0	
	red_min_c=copy.deepcopy(red_min2)
	red_min3=[]
	red_bin3=[]
	for i in red_bin2:
		for j in red_bin2[w:]:
			if diff1(i,j):
				k=red_min2[red_bin2.index(j)]
				l=red_min2[red_bin2.index(i)]
				red_bin3.append(red(i,j))
				red_min3.append(k+l)
				if k in red_min_c:
					red_min_c.remove(k)
				if l in red_min_c:
					red_min_c.remove(l)
				
	w+=1
	red_bin3=remredun1(red_bin3)
	red_min3=remredun2(red_min3)
	return red_bin3,red_min3,red_min_c

def Reducedbin(Reduced_min,numVar):#it changes the reduced minterms to its alphabetic equivalent
	Reduced_bin=[]
	for i in Reduced_min:
			if str(i).isnumeric()==False:
				if len(i)==2:
					j=num2bin(i[0],numVar)
					k=num2bin(i[1],numVar)
					Reduced_bin.append(red(j,k))
				elif len(i)==4:
					Reduced_bin.append(red4(i[0],i[1],i[2],i[3],numVar))
			else:
				Reduced_bin.append(num2bin(i,numVar))
	return Reduced_bin

def chart_create(Reduced_bin,Reduced_min,normal,numVar):#this function creates the last prime implicant chart in mccluskey method
	chart=[]
	for j in range(len(Reduced_bin)):
		chart.append([min2var(Reduced_bin[j],numVar)])
		for i in normal:
			if type(Reduced_min[j]) is list:
				if i in Reduced_min[j] :
					chart[j].append("*")
				else:
					chart[j].append(" ")
			else:
				if i==Reduced_min[j]:
					chart[j].append("*")
				else:
					chart[j].append(" ")
	
	for i in chart:#for removal of quads made up by only don't cares
		if "*" not in i:
			chart.remove(i)
	return chart

def isin(l1,l2):#for checking whether list1 can be covered by list2 or not
	c=0
	for k in range(len(l1)):
		if l1[k]=='*' and l2[k]==l1[k]:
			c+=1	
	
	if c==l1.count('*'):
		return True
	return False

def rem_min(chart,chart_original):#for searching of minterms which are not covered by the EPI chart
	r=[]

	if len(chart)>0:
		for i in range(len(chart[0])):
			c=0
			for j in range(len(chart)):
				if chart[j][i]==" ":
					c+=1
			if c==len(chart):
				r.append(i)
	else:
		for i in range(1,len(chart_original)+1):# assigning of all available minterms in case no EPI is found
			r.append(i)
			
	return r

def func(chart,r):#for searching of minterms which can be used for covering remaining minterms in EPI chart
	g=[]

	if len(chart)==1:
		count=0
		for i in r:
			if chart[0][i]=='*':
				count+=1
		if count==len(r):
			g.append(chart[0])
				
	else:
		c=copy.deepcopy(r)
		
		for i in chart:#search for case when there is a single minterm to cover remaining positions
			count=0
			if i.count('*')==len(r):
				for j in r:
					if i[j]=='*':
						count+=1
				
				if count==len(r):
					c=[]
					g.append(i)
					
					return g

		for i in chart:
			for j in r:
				if j in c and i[j]=='*':
					g.append(i)
					
					for k in range(len(i)):
						if k in c and i[k]=='*':
							c.remove(k)
	
	return g

def EPI_find(chart_original,normal):#for finding the EPI for our function
	dic={}
	chart=copy.deepcopy(chart_original)
	for i in normal:
		dic[i]=[]#initialisation of with empty list
	c=1
	for j in normal:		
		for i in range(len(chart)):
			dic[j].append(chart[i][c])# assiging every minterms columns to corresponding minterms
		c+=1
	
	new_chart=[]
	indexes=[]

	for i in dic:						#searching for those minterms which has single '*' in the whole column
		ind=dic[i].index("*")			#search for the positon of required minterm
		if dic[i].count("*")==1 and ind not in indexes:
			new_chart.append(chart_original[ind]) #creation of new chart consisting only of essential prime implicant
			indexes.append(ind)
			chart.remove(chart_original[ind])
	
	chart1=copy.deepcopy(chart)
	for i in chart:					#creation of chart by removing minterms which can be covered by EPI chart
		for j in new_chart:
			if isin(i,j):
				chart1.remove(i)
	
	chart=copy.deepcopy(chart1)
	for i in chart1:				#for removal of those minterms which can  be covered by other minterm
		for j in chart1:
			if i!=j and isin(i,j):
				chart.remove(i)

	chart=sorted(chart,key=lambda l:l.count('*'),reverse=True)#sorting chart in decreasing order of number of '*' present in them

	new_chart.extend(func(chart,rem_min(new_chart,chart_original)))#finding and extending final chart if some normal minterms gets left by previous EPI chart 
	
	temp=copy.deepcopy(new_chart)
	for i in range(len(new_chart)):
		cf=0
		for k in range(len(new_chart[0])):
			if  new_chart[i][k]=='*':
				for j in range(len(new_chart)):				
					if  new_chart[j] in temp and i!=j and new_chart[j][k]=='*':
						cf+=1
						break
		if cf==new_chart[i].count('*'):
			temp.remove(new_chart[i])
	new_chart=temp
	return new_chart


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN FUNCTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def minFunc(sIn, numVar=4):
	"""
    This python function takes function of maximum of 4 variables as input and gives the corresponding minimized function(s)
    as the output (minimized using the QUINE-MCCLUSKEY methodology), considering the case of Don’t Care conditions.

	Input is a string of the format (a0,a1,a2, ...,an d d0,d1, ...,dm) Output is a string representing the simplified Boolean Expression
	in SOP form. No need for checking of invalid inputs. Do not include any print statements in the function."""
	
	normal,dont_care=split_n_d(sIn)                            #splitting into normal minterms and don't cares
	
	All_min=normal+dont_care								   #combination of all normal and don't cares
	All_min.sort()

	for i in All_min:# for checking of wrong minterms
		if i>(2**numVar)-1:
			return None

	if len(All_min)==2**numVar:
		return 1
	elif len(normal)==0:
		return 0
	group=[[] for i in range(numVar+1)]                        #divison into different groups of minterms on basis of no.of 1 in binary value
	for  i in range(len(All_min)):
		j=num2bin(All_min[i],numVar).count('1')
		group[j].append(All_min[i])

	group=remempty(group)                                      #removed empty lists

	red_bin1,red_min1,Remaining1=step1(group,All_min[:],numVar)#step 1 of quine mccluskey method 
	
	red_bin2,red_min2,Remaining2=step2(red_bin1[:],red_min1[:])#step 2 of quine mccluskey method

	red_bin3,red_min3,Remaining3=step3(red_bin2[:],red_min2[:])#step 3 of quine mccluskey method, neccessary only when octets are being formed
	
	Remaining=Remaining1+Remaining2+Remaining3                 #remaining terms which didn't participated in reduction in step1,step2 and step3
	
	Reduced_min=Remaining+red_min3                             #prime implicants in form of lists of mintems
	
	Reduced_bin=Reducedbin(Reduced_min,numVar)+red_bin3        #prime implicant in form of lists of reduced binary string

	chart=chart_create(Reduced_bin,Reduced_min,normal,numVar)  #final chart creation
	
	#search for essential prime implicants
	EPI=EPI_find(chart,normal)
	s=''
	for i in EPI:
		s+=i[0]+' + '
	return s[:-3]

print(minFunc('2,5d0,4,6',3))
print(minFunc('1,2d3',2))
print(minFunc('d0',2))
print(minFunc('1,2,4,5,6,10,11,12,13',4))
print(minFunc('3,6,10,13d0,2,5,7,8,9,12',4))
print(minFunc('1d0',1))
print(minFunc('2,5d0,4,6',3))
print(minFunc('d1,4,9,15',4))
print(minFunc('0,1,4,5,7,9,10,11,13,15',4))