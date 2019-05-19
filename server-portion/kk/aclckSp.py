# clock string specifier to integer specifier

#should provide the input

#follow instructions

#as how you call the time
 
#answering when someone asks you time

#like 
#__________________________________
#|inputs          | expected output|
#|________________|________________|
#|nine thirty     |   9 : 30       |
#|quarter to eight|   7 : 45       |
#|five to nine    |   9 : 55       |
#|nine past ten   |   10 : 9       |
#|nine'Oclock     |   9 : 0        |
#|six             |   6 : 0        |
#|________________|________________|

#etc..

#instructions
#nine'Oclock no spaces here and 'O' is capital
#spelling should be perfect
#all small letters




one_two={1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',0:"'Oclock",11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen',16:'sixteen',17:'seventeen',18:'eighteen',19:'ninteen',20:'twenty',10:'ten',20:'twenty',30:'thirty',40:'fourty',50:'fifty',60:'sixty',70:'seventy',80:'eighty',90:'ninty'}#for other purpose
#a ref to the integer number to a string
item=one_two.items()#listify only string to identify
to={}# for ref purpose
for i,j in item:
	to[j]=i
inpt=raw_input('enter time format in words\n')
inpt=inpt.split()# get input
if len(inpt)==1:#here process starts
	if inpt[0] in to.keys():#nine  |  9 : 00
		print to[inpt[0]],': 00'
	else:# 
		tk=''
		for i in inpt[0]:
			if i=="'":
				break
			tk+=i
		print to[tk],': 00'
elif len(inpt)==2:
	if inpt[0] in to.keys():
		hour=to[inpt[0]]
	if inpt[1] in to.keys():
		mnts=to[inpt[1]]
	if mnts>=60:
	    hour+=1
	    mnts=0
	print hour,':',mnts
elif len(inpt)==3:
	hour=0
	mnts=0
	if inpt[0]=='quarter':
		if inpt[1]=='to':
			print to[inpt[2]]-1,': 45'
		elif inpt[1]=='past':
			hour=to[inpt[2]]
			mnts=15
	elif inpt[1]=='to':
		hour=to[inpt[2]]-1
		mnts=60-to[inpt[0]]
	elif inpt[1]=='past':
		hour=to[inpt[2]]
		mnts=to[inpt[0]]
	elif inpt[0] in to.keys():#and inpt[1]!='to':
		hour=to[inpt[0]]
	else:
		print"hours should less than 12"
	if inpt[1] in to.keys():
		mnts=int(to[inpt[1]])+to[inpt[2]]
		if mnts>=60:
			 if hour+1>12:
			 	print "mistake is done by you"
			 else:
			 	hour=hour+1;mnts='00'
	print hour,':',mnts
