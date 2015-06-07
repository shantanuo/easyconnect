gateway_host='1.2.3.4' 
gateway_port=3232
gateway_user='some_user'
gateway_pass='user@pass'

dest_ip='10.0.0.240'
dest_port=22022
dest_user='root'
dest_pass='pass'

# command to execute on destination server
mycommand='ls'

import paramiko
middle_client = paramiko.SSHClient()
middle_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
middle_client.connect(hostname=gateway_host, port=gateway_port, username=gateway_user,  password=gateway_pass)
transport = middle_client.get_transport()
dest_addr = (dest_ip, dest_port)
local_addr = ('127.0.0.1', 1234)
channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)
last_server = paramiko.SSHClient()
last_server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
last_server.connect(hostname='localhost',  username=dest_user, password=dest_pass, sock=channel)
# use sftp.put or sftp.get to transfer files
#sftp = last_server.open_sftp()
#sftp.put('/tmp/test1.txt', '/tmp/test2.txt')

# execute command
(sshin1, sshout1, ssherr1) = last_server.exec_command(mycommand)
print sshout1.read()
        
