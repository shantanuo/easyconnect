import web
from web import form

# install web.py
# use pip install or easy_install web.py
# or download source
# wget http://webpy.org/static/web.py-0.37.tar.gz
# tar xvf web.py-0.37.tar.gz
# cd web.py-0.37
# python setup.py install
##############
# run this file:
# python code.py
##############
# visit this page on port 8080
# http://23.21.167.60:8080/

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form(
    form.Dropdown('mydrop', [('value1', 'first server'), ('value2', 'second server')]),
    form.Textbox("middle_server"),
    form.Textbox("middle_port",
        form.regexp('\d+', 'Usually port 22')),
    form.Textbox('middle_user'),
    form.Textbox('middle_password'),

    form.Textbox("second_server"),
    form.Textbox("second_port"),
    form.Textbox('second_user'),
    form.Textbox('second_password'),
    form.Textbox('exec_command'))

def myfirstconnect(middle_server, middle_port, middle_user, middle_password, mycommand, file_send, file_rec, rece_f_loc, send_f_loc):
    myreturn=''
    try:
        import paramiko
    except:
        print "import error"
    try:
        proxy_client = paramiko.SSHClient()
        proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    except:
        print "error1 "
    myline= "proxy_client.connect('%s', port=%s, username='%s',  password='%s')" % (middle_server, int(middle_port), middle_user, middle_password)
    try:
        exec myline
    except:
        print "error myfirstconnect"

    try:
        sftp = proxy_client.open_sftp()
        sftp.put(file_send, send_f_loc)
        sftp.close()
    except:
        print "error while put %s %s " % (file_send, send_f_loc)
        put_error = "error while sending file %s to %s " % (file_send, send_f_loc)
        #tkMessageBox.showerror("command failed", put_error)

    try:
        (sshin1, sshout1, ssherr1) = proxy_client.exec_command(mycommand)
        mytext=sshout1.read()
        mytext_error=ssherr1.read()
        if mytext:
            myreturn += mytext
            #tkMessageBox.showinfo("command output", mytext)
        elif mytext_error:
            myreturn += mytext_error
            #tkMessageBox.showerror("command failed", mytext_error)
    except:
        print "error while executing the command on remote host"

    try:
        sftp = proxy_client.open_sftp()
        sftp.get(file_rec, rece_f_loc)
        sftp.close()
    except:
        print "error while get %s %s " % (file_rec, rece_f_loc)
        get_error = "error while receiving file from %s to %s " % (file_rec, rece_f_loc)
        #tkMessageBox.showerror("command failed", get_error)

    return myreturn

def mysecondconnect(middle_server, middle_port, middle_user, middle_password, second_server, second_port, second_user, second_password, mycommand, file_send, file_rec, rece_f_loc, send_f_loc):
    myreturn=''
    try:
        import paramiko
    except:
        print "import error"
    try:
        proxy_client = paramiko.SSHClient()
        proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    except:
        print "error1 "
    myline= "proxy_client.connect('%s', port=%s, username='%s',  password='%s')" % (middle_server, int(middle_port), middle_user, middle_password)
    try:
        exec myline
    except:
        print "error myfirstconnect in function mysecondconnect"
        exit
    transport = proxy_client.get_transport()
    try:
        myline2="dest_addr = ('%s', %d)" % (second_server, int(second_port))
        print myline2
        exec myline2
    except:
        print "error in myline2"
    try:
        local_addr = ('127.0.0.1', 1234)
        channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)
        last_server = paramiko.SSHClient()
        last_server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        myline3="last_server.connect(hostname='localhost', username='%s', password='%s', sock=channel)" % (second_user, second_password)
        exec myline3
        print myline3
    except:
        print "error in myline3"


    try:
        sftp = proxy_client.open_sftp()
        sftp.put(file_send, send_f_loc)
        sftp.close()
    except:
        print "error while put %s %s " % (file_send, send_f_loc)
        put_error = "error while sending file %s to %s " % (file_send, send_f_loc)
        #tkMessageBox.showerror("command failed", put_error)

    try:
        (sshin1, sshout1, ssherr1) = last_server.exec_command(mycommand)
        mytext=sshout1.read()
        mytext_error=ssherr1.read()
        if mytext:
            myreturn += mytext
            #tkMessageBox.showinfo("command output", mytext)
        elif mytext_error:
            myreturn += mytext_error
            #tkMessageBox.showerror("command failed", mytext_error)
    except:
        print "error while executing the command on remote host"

    try:
        sftp = proxy_client.open_sftp()
        sftp.get(file_rec, rece_f_loc)
        sftp.close()
    except:
        print "error while get %s %s " % (file_rec, rece_f_loc)
        get_error = "error while receiving file from %s to %s " % (file_rec, rece_f_loc)
        #tkMessageBox.showerror("command failed", get_error)

    return myreturn


class index:
    def GET(self):
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.formtest(form)

    def POST(self):
        form = myform()
        if not form.validates():
            return render.formtest(form)
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            middle_server=form['middle_server'].value.encode('ascii', 'ignore') or None
            middle_port=int(form['middle_port'].value.encode('ascii', 'ignore')) or None
            middle_user=form['middle_user'].value.encode('ascii', 'ignore') or None
            middle_password=form['middle_password'].value.encode('ascii', 'ignore') or None
            mycommand=form['exec_command'].value.encode('ascii', 'ignore') or None
            file_send = file_rec = rece_f_loc = send_f_loc = None
            second_server=form['second_server'].value.encode('ascii', 'ignore') or None
            second_port=form['second_port'].value.encode('ascii', 'ignore') or None
            second_user=form['second_user'].value.encode('ascii', 'ignore') or None
            second_password=form['second_password'].value.encode('ascii', 'ignore') or None
            user_option=form['mydrop'].value
            print middle_server.encode('ascii','ignore'), middle_port, middle_user, middle_password, mycommand, file_send, file_rec, rece_f_loc, send_f_loc
            if user_option == 'value2':
                toshow=mysecondconnect(middle_server, middle_port , middle_user , middle_password , second_server, second_port, second_user, second_password, mycommand , file_send, file_rec, rece_f_loc, send_f_loc)
            else:
                print "error myscondconnect"
                toshow=myfirstconnect(middle_server, middle_port , middle_user , middle_password , mycommand , file_send, file_rec, rece_f_loc, send_f_loc)
            #return "Grrreat success! boe: %s, bax: %s" % (form['middle_server'].value, form['middle_port'].value)
            return toshow
    
if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
