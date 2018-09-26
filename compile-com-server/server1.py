######################################################
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
#@                                                  @#
#@	#   # #####  ##   # #   #     #   ########  @#
#@	#   # #      # #  # ###     #  #     #      @#
#@ 	#  #  ####   #  # # #  #   #####     #      @#
#@	 #    ###### #   ## #   # #     #    #      @#
#@                                                  @#
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
######################################################



try:
	import socket,os,traceback
	import threading,sys,time
	import urllib,json,unicodedata
	import tasking,magic,platform
except:
	print "failed import "

"""
	Author		: 	M.Venkat   sai
	Last-Modified	:	28 sept 2018
	release		:	alpha 0.0.1(still in development)
	platform	:	linux
	email		:	venkatsaimaragani@gmail.com
	
	note:all modules are standard for python27 except magic that is same directory and tasking made by myself
"""
class Serve:
	host = ""
	port = 8000
	request = ''
	response = 	"""HTTP/1.1 {}
Content-Type: {}
Last-Modified: {}

{}"""
	curdir = '.'
	def __init__(self,host = "",port = 8000,directory = ''):
		if host == "":
			self.host = 'localhost'
		self.host = host
		if port != 8000:
			self.port = port 
		if directory != '':
			self.curdir = directory
		else:
			self.curdir = "."
		self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.server.bind((self.host,self.port))


	def start(self):
		self.server.listen(1)
		print "Server started at http://"+str(self.host if self.host != "" else "localhost")+":"+str(self.port)
		while True:
			c,a = self.server.accept()
			#print "ip",a,"connected"
			t = threading.Thread(target = self.handler,args = (c,a))
			t.start()

	def handler(self,c,a):
		#temp_req = str(c.recv(10000).decode('utf-8'))
		temp_req = ''
		while True:
			k = c.recv(2048)
			temp_req+=k
			if k: break
		request = self.format(temp_req)
		request["req"] = urllib.unquote(request["req"])
		
		method = request["method"]
		if method == "POST":
			request_data = temp_req.split('\r\n\r\n')
			# not working the json one
			data = {"status":"500 Internal Server Error","Content-type":"test/txt","Last-Modified":"","response":"Internal Server Error"}
			try:
				data = self.post_response(request_data[-1])
				#data["response"]= data
				last_modified = ""
			except Exception as e:
				last_modified = ''
				print "while getting POST response..."
				print e
				#ex_type, ex, tb = sys.exc_info() #debugging purpose
                        	#traceback.print_tb(tb)

		if method == "GET":
			data = {"status":"500 Internal Server Error","Content-type":"test/txt","Last-Modified":"","response":"Internal Server Error"}
			try:
				data = self.get_response(request["req"])
				if platform.system() == 'Windows':
					last_modified = os.path.getctime(self.curdir + request["req"])
				else:
					last_modified = time.ctime(os.stat(self.curdir + request["req"]).st_mtime)
			except Exception as e:
				print e
				#ex_type, ex, tb = sys.exc_info() # debugging purpose
                        	#traceback.print_tb(tb)
				last_modified = ""
		localtime = time.asctime(time.localtime(time.time()))

		
		print localtime+" < "+method+' '+request["req"]+' '+str(data["status"])+'>'
		final_response = self.response.format(  data["status"].encode('utf-8'),      \
							data["Content-type"].encode('utf-8'),\
							last_modified,								\
							data["response"]                    \
						     )
		c.send(final_response)
		c.close()
	def get_response(self,link):

		temp = link.split('?');

		param = temp[1:]
		f = temp[0]
		status = None
		response = ''
		# all files and directories should be on childs not parents
		try:
			if f == '/' or os.path.isdir(self.curdir+f):
				ls = os.listdir(self.curdir)
				hasthem = False
				if 'index.html'  in ls: 
					now = f+'/index.html'
					hasthem = True
				elif 'home.html' in ls:
					now = f+'/home.html'
					hasthem = True
				else:
					response = self.getlistdir(self.curdir+f,f)
					#mimetype = 'text/html'
				if hasthem:
					print now
					f_ = open(self.curdir+"/"+now.lstrip('/'),'rb')
					response += f_.read()
					f_.close()
					#mimetype = "text/html"
			else:
				f_ = open(self.curdir+f,'rb')
				response += f_.read()
				f_.close()
			mimetype = magic.from_buffer(response,mime=True)
			status = '200 OK'
		except Exception as e:
			print '\n--------debuging info----------'
			print e,"\n"
			#ex_type, ex, tb = sys.exc_info()
			#traceback.print_tb(tb)

			#response += "<h1><center>404 ERROR FILE NOT FOUND</center></h1>".encode('utf-8') 
			
			f_ = open("error.html",'rb')
			response = f_.read().encode('utf-8')
			f_.close()
			
			status = "404 NOT FOUND"			
			mimetype = "text/html"

		final_response = {"status":status ,"Content-type":mimetype ,"response":response}
		return final_response
	def post_response(self,data):
		print data
		s = urllib.unquote(bytes(data)).decode('utf8')
		s = unicodedata.normalize('NFKD', s).encode('ascii','ignore')
		s = json.loads(s)

		data = tasking.get_out(s['code'],s['input'])
		res = {"status":"200 OK","Content-type":"text/json","response":json.dumps({'out':data})}
		return res
	
	def format(self,string):
		try:
			result = {}
			ls = string.split(' ')
			result["method"] = ls[0]
			if ls>2:
				result["req"] = ls[1]
		except Exception as e:
			print e
			result = {"method":"GET","req":"/index.html"}
		return result
	
	def shutdown(self):
		self.server.shutdown(socket.SHUT_RDWR)
		self.server.close()
	def getlistdir(self,r,frm = ''):
		result = '''<!DOCTYPE html>
<html>
<head>
	<title>listing directories</title>
</head>
<body>
	<h1>Index for %s</h1><hr/>
	<ol style='list-style-type:circle'>'''%(r)
		ls = os.listdir(r)
		for i in ls:
			result += '<li><a href = "'+('' if frm=='/' else frm)+'/'+i+'">'+i+'</a></li>'
		result += ' </ol> </body> </html>'	
		return result








def main():
	try:
		server = Serve("",80,'./server-portion')
		server.start()
	except KeyboardInterrupt:
		print " recieved Server was Shut-Downed"
		#server.shutdown()

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print "----------main exception-----------"
		print e,'\n'





#*****************************************************************************#  
#    #   #  #####   #####   ### #     # #####  ##   # #   #    #   ########   #
#    #  #   #   #   #   #  #     #   #  #      # #  # #  #    # #     #       #
#    # #    ####    #   #  #      # #   ####   #  # # # #    #####    #       #
#    #   #  #    #  #####   ###    #    ###### #   ## #   # #     #   #       # 
#*****************************************************************************#
