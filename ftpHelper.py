import socket
import getpass
import random
import time
import os

class FTPClient:

    def __init__(self):
        self.server_name = None
        self.clientSocket = None
        self.connection = False
    
    def clear_variable(self):
        self.server_name = None
        self.clientSocket = None
        self.connection = False

    def ascii(self):
        if self.clientSocket == None:
            print('Not connected.')
            return
        self.clientSocket.send(f'TYPE A\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")
        
    def binary(self):
        if self.clientSocket == None:
            print('Not connected.')
            return
        self.clientSocket.send(f'TYPE I\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")


    def cd(self,path=None):
        if self.clientSocket == None:
            print('Not connected.')
            return
        if path is None:
            path = input('Remote directory ')
        if path == '':
            print("cd remote directory.")
            return

        self.clientSocket.send(f'CWD {path}\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")

    def close(self):
        self.disconnect()


    def delete(self,file=None):
        if self.clientSocket == None:
            print('Not connected.')
            return
        if file is None:
            file = input('Remote file ')
        if file == '':
            print("delete remote file.")
            return

        self.clientSocket.send(f'DELE {file}\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")

        
    def disconnect(self):
        if self.clientSocket == None:
            print('Not connected.')
            return
        self.clientSocket.send(f'QUIT\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")
        self.clientSocket.close()
        self.clear_variable()

    

    def quit(self):
        if self.clientSocket == None:
            print()
            return
        self.clientSocket.send(f'QUIT\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")
        self.clientSocket.close()
        self.clear_variable()
        print()

    def bye(self):
        self.quit()


    def check_connect(self, sock, host, port):
        try:
            sock.connect((host, port))
            return True
        except socket.gaierror:
            print(f"Unknown host {host}.")
            return False
        except ConnectionRefusedError:
            print(f"> ftp: connect :Connection refused")
            return False
        except socket.error as msg:
            print(f"Failed to connect: {msg}")
            return False
        

    def show_transfer_rate(self, start_time, end_time, size):
        elapsed = end_time - start_time
        if elapsed == 0:
            elapsed = 0.000000001
        tf_rate = (size/1000)/elapsed
        if tf_rate > size: 
            tf_rate = size
        print(f"ftp: {size} bytes received in {elapsed:.2f}Seconds {tf_rate:.2f}Kbytes/sec.")


    def get(self, filename, local_file=None):
        if self.clientSocket is None:
            print('Not connected.')
            return
        number = random.randint(0,65535)
        ipaddr = socket.gethostbyname(socket.gethostname())+f".{number//256}.{number%256}"
        ipaddr = ipaddr.replace('.',',')
        
        self.clientSocket.send(f'PORT {ipaddr}\r\n'.encode())
        resp = self.clientSocket.recv(1024).decode()
        print(resp,end='')

        self.clientSocket.sendall(b'PASV\r\n')
        pasv_response = self.clientSocket.recv(1024).decode()
        data_host, data_port = self.parse_pasv_response(pasv_response)
        
        self.clientSocket.sendall(f'RETR {filename}\r\n'.encode())
        resp = self.clientSocket.recv(1024).decode()
        print(resp,end='')
        if resp.startswith('5'):
            return
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.settimeout(10)
        data_socket.connect((data_host, data_port))
        with open(local_file, 'wb') as lf:
            while True:
                # try:
                data = data_socket.recv(1024)
                size = 0  # Specify the total size of the data received
                start_time = time.time()
                if not data:
                    break
                lf.write(data)
                # except socket.timeout:
                #     print("Data connection timed out.")
                #     break
                # except Exception as e:
                #     print("An error occurred:", e)
                #     break
        data_socket.close()
        resp = self.clientSocket.recv(1024).decode()
        print(resp,end='')

        # Calculate and display transfer rate
        end_time = time.time()
        self.show_transfer_rate(start_time, end_time, size+10)


    def parse_pasv_response(self,response):
        parts = response.split('(')[1].split(')')[0].split(',')
        host = '.'.join(parts[:4])
        port = int(parts[4])*256 + int(parts[5])
        return host, port

    def ls(self,file=''):
        if self.clientSocket is None:
            print('Not connected.')
            return
        number = random.randint(0,65535)
        ipaddr = socket.gethostbyname(socket.gethostname())+f".{number//256}.{number%256}"
        ipaddr = ipaddr.replace('.',',')
        
        self.clientSocket.send(f'PORT {ipaddr}\r\n'.encode())
        resp = self.clientSocket.recv(1024).decode()
        print(resp,end='')
        if resp.startswith('5'):
            return

        self.clientSocket.sendall(b'PASV\r\n')
        pasv_response = self.clientSocket.recv(1024).decode()
        # print(f'self.connection {self.connection}')
        data_host, data_port = self.parse_pasv_response(pasv_response)
        with socket.create_connection((data_host, data_port)) as data_socket:
            self.clientSocket.sendall((f'NLST {file}\r\n').encode())
            dir_response = self.clientSocket.recv(1024).decode()
            print(dir_response, end='')
            if dir_response.startswith('5'):
                return
            size = 0  # Specify the total size of the data received
            start_time = time.time()
            while True:
                data = data_socket.recv(4096)
                if not data:
                    break
                print(data.decode(), end='')
    
        control_response = self.clientSocket.recv(1024).decode()
        print(control_response, end='')

         # Calculate and display transfer rate
        end_time = time.time()
        
        self.show_transfer_rate(start_time, end_time, size+10)



    def open(self, host, port=21):
        if self.server_name:
            print(f'Already connected to {self.server_name}, use disconnect first.')
            return
        
        if host == '':
            host = input('To ')
        port = int(port)

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect = self.check_connect(self.clientSocket,host,port)
        if connect == True:
            self.server_name = host
        else:
            self.clear_variable()
            return

        print(f'Connected to {self.server_name}.')
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")
        self.clientSocket.send(f'OPTS UTF8 ON\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")

        #user login
        username = input(f'User ({self.server_name}:(none)): ').strip()
        self.clientSocket.send(f'USER {username}\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        result_response = resp.decode()
        print(result_response,end="")
        if result_response.startswith('5'):
            print('Login failed.')
            return
        #password
        password = getpass.getpass(prompt='Password: ')
        self.clientSocket.send(f"PASS {password}\r\n".encode())
        resp = self.clientSocket.recv(1024)
        print()
        result_response = resp.decode()
        print(result_response,end="")
        if result_response.startswith('5'):
            print('Login failed.')
        else:
            self.connection = True


    def sent_transfer_rate(self, start_time, end_time, size):
        elapsed = end_time - start_time
        if elapsed == 0:
            elapsed = 0.000000001
        tf_rate = (size/1000)/elapsed
        if tf_rate > size: 
            tf_rate = size
        print(f"ftp: {size} bytes sent in {elapsed:.2f}Seconds {tf_rate:.2f}Kbytes/sec.")

    

    def put(self, file=None,new=None):
        if self.clientSocket is None:
            print('Not connected.')
            return
        if file is None and new is None:
            file = input('Local file ')
            if file == '':
                print('Local file put: remote file.')
                return
            new = input('Remote file ')
            if new == '':
                new = file

        if not os.path.exists(file):
            print(f'{file}: File not found')
            return

        number = random.randint(0,65535)
        ipaddr = socket.gethostbyname(socket.gethostname())+f".{number//256}.{number%256}"
        ipaddr = ipaddr.replace('.',',')
        self.clientSocket.send(f'PORT {ipaddr}\r\n'.encode())
        port_status = self.clientSocket.recv(1024)
        print(port_status.decode(),end="")
        with open(file,'rb') as f:
            try:

                self.clientSocket.sendall(b'PASV\r\n')
                response = self.clientSocket.recv(1024).decode()
                port_start = response.find('(') + 1
                port_end = response.find(')')
                port_str = response[port_start:port_end].split(',')
                data_port = int(port_str[-2]) * 256 + int(port_str[-1])
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect((socket.gethostbyname(self.server_name), data_port))
                self.clientSocket.sendall((f'STOR {new}\r\n').encode())
                response = self.clientSocket.recv(4096).decode()
                print(response,end='')
                if not response.startswith('150'):
                    return
                size = 0  # Specify the total size of the data received
                start_time = time.time()
                data = f.read(4096)
                while data:
                    data_socket.sendall(data)
                    data = f.read(4096)
            finally:
                data_socket.close()
            response = self.clientSocket.recv(1024)
            print(response.decode(),end='')
            
        end_time = time.time()
        self.sent_transfer_rate(start_time, end_time, size+10)


    def pwd(self):
        if self.clientSocket == None:
            print('Not connected.')
            return
        
        self.clientSocket.send(f'XPWD\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")

        
    def rename(self,filename=None,newname=None):
        if self.clientSocket == None:
            print('Not connected.')
            return
        if filename is None:
            filename = input('From name ')
        if filename == '':
            print('rename from-name to-name.')
            return
        if newname is None:
            newname = input('To name ')
        if newname == '':
            print('rename from-name to-name.')
            return
        self.clientSocket.send(f'RNFR {filename}\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="") 
        if not resp.decode().startswith('350') or resp.decode().startswith('5'):
            return
        self.clientSocket.send(f'RNTO {newname}\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="") 

    def user(self,username=None,password=None):
        if self.clientSocket == None:
            print('Not connected.')
            return
        if username is None:
            username = input('Username ')
            if username == '':
                print('Usage: user username [password] [account]')
                return
        self.clientSocket.send(f'User {username}\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        print(resp.decode(),end="")
        if not resp.decode().startswith('331'):
            print('Login failed.')
            return
        if password is None:
            password = getpass.getpass("Password: ")
            print()
        self.clientSocket.send(f'PASS {password}\r\n'.encode())
        resp = self.clientSocket.recv(1024)
        if resp.decode().startswith('5'):
            print(resp.decode(),end="")
            print('Login failed.')
            return
        else:
            self.connection = True
        self.username = username
        self.password = password
        print(resp.decode(),end="")

