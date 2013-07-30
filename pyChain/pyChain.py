import errno
import socket
import thread
import time
 
BUFF = 1024
HOST = '127.0.0.1'
PORT = 9999
active = False

clients = []
 
def dataSender():
    while active:
        for client in clients:
            try:
                client.send("Test")
            except socket.error, v:
                errorcode = v[0]
                if( errorcode == errno.WSAECONNRESET ):
                    print "Connection closed by Peer"
                else:
                    print "Another error occured: " + errno.errorcode[errorcode]
                break
            
            time.sleep(1)

def processData(clientsock, data):
    print "Received data: " + repr(data)
            
def connectionHandler(clientsock, addr):
    #add to our clients
    clients.append(clientsock)
    print "We have now %d clients" % len(clients)
        
    while active:
        try:
            data = clientsock.recv(BUFF)
        except socket.error, v:
            errorcode = v[0]
            if( errorcode == errno.WSAECONNRESET ):
                print "Connection closed by Peer"
            else:
                print "Another error occured: " + errno.errorcode[errorcode]
            break
            
        processData(clientsock, data)
        clientsock.send("Data accepted")

    #close everything if we're finished here
    print "Closing socket"
    clientsock.close()
    
    #remove the client from our client-list
    clients.remove(clientsock)
    print "We have now %d clients" % len(clients)
 
if __name__=='__main__':
    ADDR = (HOST, PORT)
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    
    #start the thread which prints data to all our clients
    thread.start_new_thread(dataSender, ())
    
    active = True
    while active:
        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        print '...connected from: ', addr
        thread.start_new_thread(connectionHandler, (clientsock, addr))
