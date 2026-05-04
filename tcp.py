import socket
import threading
import time 


HOST="0.0.0.0"
PORT=5001

response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 17\r\n"
        "\r\n"
        "Hello from server"
    )

def Do(conn,addr):
    conn.recv(1024)
    time.sleep(10)
    
    conn.sendall(response.encode())

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:         # socket.AF_INET Specifies the address family AF_INET for IPv4 addresses   and socket.SOCK_STREAM specifies for the socket type SOCK_STREAM = TCP

    s.bind((HOST,PORT))
    s.listen()                                                  # To make the server listen at port 5001
    print(f"Server is listening on port {PORT}")
    
    while True:
        conn,addr=s.accept()                                        # Now the server waits for the client to connect
        print(conn)                                        
        threading.Thread(target=Do,args=(conn,addr),daemon=True).start()    #for parallel processing of requests



    
