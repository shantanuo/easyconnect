from Tkinter import *
import tkMessageBox
send_file=''

def myconnect(middle_server, middle_port, middle_user, middle_password, last_server, last_port, last_user, last_password, mycommand, file_send, file_rec, rece_f_loc, send_f_loc):
    import paramiko
    proxy_client = paramiko.SSHClient()
    proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    proxy_client.connect(middle_server, port=middle_port, username=middle_user,  password=middle_password)
    transport = proxy_client.get_transport()
    dest_addr = (last_server, last_port)
    local_addr = ('127.0.0.1', 1234)
    channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)
    remote_client = paramiko.SSHClient()
    remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        remote_client.connect('localhost', port=last_port, username=last_user, password=last_password, sock=channel)
    except:
        print "error while connecting to remote host"

    try:
        sftp = remote_client.open_sftp()
        sftp.put(file_send, send_f_loc)
        sftp.close()
    except:
        print "error while put %s %s " % (file_send, send_f_loc)
        put_error = "error while sending file %s to %s " % (file_send, send_f_loc)
        tkMessageBox.showerror("command failed", put_error)

    try:
        (sshin1, sshout1, ssherr1) = remote_client.exec_command(mycommand)
        mytext=sshout1.read()
        mytext_error=ssherr1.read()
        if mytext:
            tkMessageBox.showinfo("command output", mytext)
        elif mytext_error:
            tkMessageBox.showerror("command failed", mytext_error)
    except:
        print "error while executing the command on remote host"


    try:
        sftp = remote_client.open_sftp()
        sftp.get(file_rec, rece_f_loc)
        sftp.close()
    except:
        print "error while get %s %s " % (file_rec, rece_f_loc)
        get_error = "error while receiving file from %s to %s " % (file_rec, rece_f_loc)
        tkMessageBox.showerror("command failed", get_error)

    return 0


def myfirstconnect(middle_server, middle_port, middle_user, middle_password, mycommand, file_send, file_rec, rece_f_loc, send_f_loc):
    import paramiko
    try:
        proxy_client = paramiko.SSHClient()
        proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        proxy_client.connect(middle_server, port=middle_port, username=middle_user,  password=middle_password)
    except:
        print "error myfirstconnect"
        
    try:
        sftp = proxy_client.open_sftp()
        sftp.put(file_send, send_f_loc)
        sftp.close()
    except:
        print "error while put %s %s " % (file_send, send_f_loc)
        put_error = "error while sending file %s to %s " % (file_send, send_f_loc)
        tkMessageBox.showerror("command failed", put_error)

    try:
        (sshin1, sshout1, ssherr1) = proxy_client.exec_command(mycommand)
        mytext=sshout1.read()
        mytext_error=ssherr1.read()
        if mytext:
            tkMessageBox.showinfo("command output", mytext)
        elif mytext_error:
            tkMessageBox.showerror("command failed", mytext_error)
    except:
        print "error while executing the command on remote host"

    try:
        sftp = proxy_client.open_sftp()
        sftp.get(file_rec, rece_f_loc)
        sftp.close()
    except:
        print "error while get %s %s " % (file_rec, rece_f_loc)
        get_error = "error while receiving file from %s to %s " % (file_rec, rece_f_loc)
        tkMessageBox.showerror("command failed", get_error)

    return 0


def close_window():
    root.destroy()

def choose_file():
    global send_file
    from tkFileDialog import askopenfilename
    send_file = askopenfilename()

def submit_window():
    print "success"
    ms= middle_s.get()
    mp= int(middle_p.get())
    mu= middle_u.get()
    mpass= middle_pass.get()
    myc= mycommand.get()
    rec_file=receive_file.get()
    r_f_loc=receive_file_loc.get()
    s_f_loc=send_file_loc.get()

    if last_s.get().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        ls= last_s.get()
        lp= int(last_p.get())
        lu= last_u.get()
        lpass= last_pass.get()
        #print(ms, mp, mu, mpass, ls, lp, lu, lpass, myc, send_file, rec_file, r_f_loc, s_f_loc)
        myconnect(ms, mp, mu, mpass, ls, lp, lu, lpass, myc, send_file, rec_file, r_f_loc, s_f_loc)
    else:
        #print(ms, mp, mu, mpass, myc, send_file, rec_file, r_f_loc, s_f_loc)
        myfirstconnect(ms, mp, mu, mpass, myc, send_file, rec_file, r_f_loc, s_f_loc)
        

root=Tk()

middle_s=StringVar()
middle_p=StringVar()
middle_u=StringVar()
middle_pass=StringVar()

last_s=StringVar()
last_p=StringVar()
last_u=StringVar()
last_pass=StringVar()

mycommand=StringVar()
receive_file=StringVar()
receive_file_loc=StringVar()
send_file_loc=StringVar()

Label(root, text='middle_server' ).grid(row=0, column=0)
Entry(root, textvariable=middle_s).grid(row=0, column=1)
Label(root, text='middle_port').grid(row=1, column=0)
Entry(root, textvariable=middle_p).grid(row=1, column=1)
Label(root, text='middle_user' ).grid(row=2, column=0)
Entry(root, textvariable=middle_u).grid(row=2, column=1)
Label(root, text='middle_password' ).grid(row=3, column=0)
Entry(root, textvariable=middle_pass).grid(row=3, column=1)
Label(root, text='last_server').grid(row=4, column=0)
Entry(root, textvariable=last_s).grid(row=4, column=1)
Label(root, text='last_port' ).grid(row=5, column=0)
Entry(root, textvariable=last_p).grid(row=5, column=1)
Label(root, text='last_user' ).grid(row=6, column=0)
Entry(root, textvariable=last_u).grid(row=6, column=1)
Label(root, text='last_password' ).grid(row=7, column=0)
Entry(root, textvariable=last_pass).grid(row=7, column=1)
Label(root, text='send file').grid(row=8, column=0)

button = Button(root)
button['text'] ="Choose file"
button['command'] = choose_file
button.grid(row=8, column=1)

Label(root, text='send file location').grid(row=8, column=2)
Entry(root, textvariable=send_file_loc).grid(row=8, column=3)

Label(root, text='Exec command').grid(row=9, column=0)
Entry(root, textvariable=mycommand).grid(row=9, column=1)

Label(root, text='receive file').grid(row=10, column=0)
Entry(root, textvariable=receive_file).grid(row=10, column=1)

Label(root, text='receive file location').grid(row=10, column=2)
Entry(root, textvariable=receive_file_loc).grid(row=10, column=3)

button = Button(root)
button['text'] ="submit"
button['command'] = submit_window
button.grid(row=11, column=0)

button = Button(root)
button['text'] ="cancel"
button['command'] = close_window
button.grid(row=11, column=1)

root.mainloop()
