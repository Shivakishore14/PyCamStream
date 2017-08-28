#!/usr/bin/env python

import socket
import os

i = 0
def HandleConn(conn):
	global i
	while 1:
		img = conn.recv(40000)
		f = open("img"+str(i)+".jpg", 'w')
		i = i + 1
		f.write(img)
		f.close
		if len(img) == 0:
			print("break")
			conn.close()
			break

def Main():
	TCP_IP = '0.0.0.0'
	TCP_PORT = 8888

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	while True:
		conn, addr = s.accept()
		print 'Connection address:', addr
		HandleConn(conn)


if __name__ == '__main__':
	Main()
#data = conn.recv(29789)
