import json
import os
import unicodedata
#from multiprocessing import Process

'''
	This module designed by myself for comp:le and runing purpose
	still supported for only c++
'''
# def __do_on_10(command):
# 	os.system(command)
def get_out(code,inpt):
	
	if os.system('cd compiler-online/1 && cd ../..') != 0:
		os.system('mkdir compiler-online/1')

	std = {"error1":None,"error2":None,"output":None}

	with open('compiler-online/inpt.txt','w') as f:
		f.write(inpt)
	with open('compiler-online/1/source.cpp','w') as f:
                f.write(code)
	
	# empty all files to reuse
	for i in ["compiler-online/error1.txt","compiler-online/error2.txt","compiler-online/output.txt"]:
		with open(i,'w') as f:
			f.write('')
	
	# compile
	os.system('g++ compiler-online/1/source.cpp -o compiler-online/1/application 2>compiler-online/error1.txt')
	
	with open('compiler-online/error1.txt','rb') as f:
		std["error1"] = f.read()
	# execute
	if 'application' in os.listdir('compiler-online/1'):
		print os.system('timeout 10 ./compiler-online/1/application >compiler-online/output.txt 2>compiler-online/error2.txt <compiler-online/inpt.txt')
		os.system('rm compiler-online/1/application')
	
	with open('compiler-online/output.txt','rb') as f:
		std["output"] = f.read()
	
	with open('compiler-online/error2.txt','rb') as f:
		std["error2"] = f.read()

	final_output = ''
	if std["output"] != '' :
		final_output += std["output"]+"\n"
	else:
		final_output += std["error1"] + "\n"

	final_output += std["error2"]

	return unicode(final_output,encoding = 'utf8',errors='ignore')

if __name__ == '__main__':
	print get_out('#include<iostream>\nusing namespace std;\nint main(){\ncout<<"hello world";\n}','')
