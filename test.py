from socket import *



sock = socket(AF_INET,SOCK_STREAM)

sock.bind(('0.0.0.0',8000))
sock.listen(1)

conn,addr = sock.accept()

conn.send('''GET / HTTP/1.1
Host:localhost:8000''')
print "sended "

recv  = conn.recv(1024)
print "recvied"
while recv:
	print recv
	recv = conn.recv(1024)

conn.close()
sock.close()
