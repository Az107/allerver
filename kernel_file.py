def tobytes(cadena):
    return str.encode(cadena)

def kernel(sock):
	sock.send(tobytes("Bienvenido al servidor echo\n"))
	data = sock.recv(1024)
	while (data.decode("utf-8") != ""):
		sock.send(data)
		sock.send(tobytes(("-"*len(data.decode("utf-8"))+"\n")))
		data = sock.recv(1024)