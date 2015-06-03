# easyconnect
connect to a server behind firewall and copy files, execute commands

Installation Instructions:

1) Install Latest Python 2.6+

2) Only for windows users:  Microsoft Visual C++ 9.0 is required. If not already installed then get it from http://aka.ms/vcpython27

3) paramiko module can be installed by running install_module.py file or using "pip install paramiko" command.
_____

4) Start program by running easyconnect.py file.

i) Type IP, port, user-name and password of staging server (called middle_sever)

ii) Type IP, port, user-name and password of any server behind the staging server (called last_server)

iii) send file should be chosen using "Choose file" button. This is the local file that you want to copy to remote server.

iv) send file remote location. Linux server path will look something like this:
/tmp/server.php

v) Type the command that you want to execute on last server or middle_server (if last server is not mentioned) For e.g. "ls" for list of directories as shown in the screen-shot.

v) receive file from remote location. path will look something like this:
/home/myfile.csv

vi) Receive file location will look something like this on windows...
C:\Users\Webzone\Downloads\x1.py
_____
Important note:

a) All locations should have read/write permission to the current user.
b) If the last server is not mentioned, the copy file function and command execution will happen on the server mentioned in the "middle_server" IP only.
_____

Here is screen-shot of how the dialog box and the pop-up window will look like...

http://i.stack.imgur.com/aJFIq.png

The above screen-shot is showing the output of "ls" command executed on 10.0.0.240 server that is accessible from gateway server 123.456.789.0
