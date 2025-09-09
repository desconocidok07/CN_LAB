import socket

s=socket.socket()#socket creation with default values
print("Socket Created")
s.bind(("127.0.0.1",9999)) #we have to sent only single item
s_number=45
server_name="JOhn Smith"
s.listen(1) #how many clients to attend
#as we have to make server which responds again and again we are using while loop
try: 
   while True:
       #now server should accept the request
       c,addr=s.accept()
       d=c.recv(1024).decode() # 1024 is the size of buffer and have to apply decode rather it will give with b which resembles bytes
       c_name,c_number=d.split(",") # as d will come in as string and have different info have to split at "," which will distinguish data
       c_number=int(c_number)
       if c_number<1 or c_number>100:
             print("Invalid Number")
             c.close()
             s.close()
             break
       print(f"Client Name: {c_name}")
       print(f"Server Name: {server_name}")
       print(f"Client's Integer: {c_number}")
       print(f"Server's Integer: {s_number}")
       print(f"Sum: {c_number+s_number}")
       c.send(f"{s_number},{server_name}".encode())
       c.close()       
except KeyboardInterrupt:
    print("\n[!] Server stopped by user (Ctrl+C)")
    s.close()   
s.close()


       