# easyconnect
connect to a server behind firewall and copy files, execute commands

Windows users:

1) Install Latest Python 2.6+

2) Microsoft Visual C++ 9.0 is required. If not already installed then get it from http://aka.ms/vcpython27

3) paramiko module can be installed using install_module.py file or using "pip install paramiko" command.

4) Start program by running easyconnect.py file.

i) Type IP, port, user-name and password of staging server (called middle_sever)

ii) Type IP, port, user-name and password of any server behind the staging server (called last_server)

iii) send file should be chosen using "Choose file" button.

iv) send file remote location location will look something like this:
/tmp/server.php

v) Type the command that you want to execute on last server or middle_server (if last server is not mentioned)

v) receive file from remote location. path will look something like this:
/home/myfile.csv

vi) Receive file location will look something like this on windows...
C:\Users\Webzone\Downloads\x1.py

Important note:

All locations should have read/write permission to the current user.

Here is screen-shot of how the dialog box and the pop-up window will look like...

http://i.stack.imgur.com/aJFIq.png

