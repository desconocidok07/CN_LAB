import socket
c=socket.socket()
c.connect(("127.0.0.1",9999))
c_name="Rahul"
c_number=int(input("Enter Your Number:"))
c.send(f"{c_name},{c_number}".encode())
d=c.recv(1024).decode()
s_number,s_name=d.split(",")
s_number=int(s_number)
print(f"Client Name: {c_name}")
print(f"Server Name: {s_name}")
print(f"Client's Integer: {c_number}")
print(f"Server's Integer: {s_number}")
print(f"Sum: {c_number+s_number}")
c.close()

