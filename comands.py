def load(comandos):
    comandos[":D"] = "face(self)"
    comandos["eco"] = "eco(self,'$arg')"
    comandos["var"] = "self.puts(str($arg))"
    comandos["chgprompt"] = "self.prompt = '$arg'"
    comandos["emitir"] = "emitir(self,clients,hilos,'$arg')"
    #comandos["open"] = "opensock(self,clients,'$arg')"
    return comandos

def face(self):
    self.puts(":D")
def eco(self,text):
    self.puts(text)
def emitir(self,clientes,hilos,text):
    self.puts("Enviando " + text + " a todos")
    for cliente in clientes:
        cliente[0].send(str.encode(text))
