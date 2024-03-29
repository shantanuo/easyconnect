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
    form.Dropdown('mydrop', [('value1', 'first server'), ('value2', 'second server'), ('value3', 'third server')]),
    form.Textbox("middle_server"),
    form.Textbox("middle_port",
        form.regexp('\d+', 'Usually port 22')),
    form.Textbox('middle_user'),
    form.Textbox('middle_password'),

    form.Textbox("second_server"),
    form.Textbox("second_port"),
    form.Textbox('second_user'),
    form.Textbox('second_password'),

    form.Textbox("third_server"),
    form.Textbox("third_port"),
    form.Textbox('third_user'),
    form.Textbox('third_password'),

    form.Textbox('exec_command'),

    form.File('myfile'),
    form.Textbox('file_send_location'),

    form.Textbox('file_receive'),
    form.Textbox('file_receive_location'))
    #form.Textbox('file_send'),

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
        if send_f_loc:
            myreturn+="file uploaded successfully to   "+send_f_loc 
            myreturn+="\n############################################\n" 

    except:
        print "error while put %s %s " % (file_send, send_f_loc)
        put_error = "error while sending file %s to %s " % (file_send, send_f_loc)
        myreturn += '\n'+put_error

    try:
        (sshin1, sshout1, ssherr1) = proxy_client.exec_command(mycommand)
        mytext=sshout1.read()
        mytext_error=ssherr1.read()
        if mytext:
            myreturn += mytext
        elif mytext_error:
            myreturn += mytext_error
    except:
        myreturn +="\n error while executing the command on remote host \n"

    try:
        sftp = proxy_client.open_sftp()
        sftp.get(file_rec, rece_f_loc)
        sftp.close()
        if rece_f_loc:
            myreturn+="\n\n###########################################################\n\n" 
            myreturn+="download your file from http://23.21.167.60:8000/"+rece_f_loc.split('/')[-1] 

    except:
        print "error while get %s %s " % (file_rec, rece_f_loc)
        get_error = "error while receiving file from %s to %s " % (file_rec, rece_f_loc)
        myreturn += '\n'+get_error
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
        sftp = last_server.open_sftp()
        sftp.put(file_send, send_f_loc)
        sftp.close()
        if send_f_loc:
            myreturn+="file uploaded successfully to   "+send_f_loc 
            myreturn+="\n############################################\n" 

    except:
        print "error while put %s %s " % (file_send, send_f_loc)
        put_error = "error while sending file %s to %s " % (file_send, send_f_loc)
        myreturn += '\n'+put_error

    try:
        (sshin1, sshout1, ssherr1) = last_server.exec_command(mycommand)
        mytext=sshout1.read()
        mytext_error=ssherr1.read()
        if mytext:
            myreturn += mytext
        elif mytext_error:
            myreturn += mytext_error
    except:
        myreturn += "\n error myfirstconnect in function mysecondconnect \n"


    try:
        sftp = last_server.open_sftp()
        sftp.get(file_rec, rece_f_loc)
        sftp.close()
        if rece_f_loc:
            myreturn+="\n\n###########################################################\n\n" 
            myreturn+="download your file from http://23.21.167.60:8000/"+rece_f_loc.split('/')[-1] 

    except:
        print "error while get %s %s " % (file_rec, rece_f_loc)
        get_error = "error while receiving file from %s to %s " % (file_rec, rece_f_loc)
        myreturn += '\n'+get_error

    return myreturn





















def mythirdconnect(middle_server, middle_port, middle_user, middle_password, second_server, second_port, second_user, second_password, third_server, third_port, third_user, third_password, mycommand, file_send, file_rec, rece_f_loc, send_f_loc):
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
###
    transport1 = last_server.get_transport()
    try:
        myline2="dest_addr1 = ('%s', %d)" % (third_server, int(third_port))
        print myline2
        exec myline2
    except:
        print "error in myline2"
    try:
        local_addr = ('127.0.0.1', 1234)
        channel1 = transport1.open_channel("direct-tcpip", dest_addr1, local_addr)
        etim_server = paramiko.SSHClient()
        etim_server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        myline3="etim_server.connect(hostname='localhost', username='%s', password='%s', sock=channel1)" % (third_user, third_password)
        exec myline3
        print myline3
    except:
        print "error in myline3"

    try:
        sftp = etim_server.open_sftp()
        sftp.put(file_send, send_f_loc)
        sftp.close()
        if send_f_loc:
            myreturn+="file uploaded successfully to   "+send_f_loc 
            myreturn+="\n############################################\n" 

    except:
        print "error while put %s %s " % (file_send, send_f_loc)
        put_error = "error while sending file %s to %s " % (file_send, send_f_loc)
        myreturn += '\n'+put_error

    try:
        (sshin1, sshout1, ssherr1) = etim_server.exec_command(mycommand)
        mytext=sshout1.read()
        mytext_error=ssherr1.read()
        if mytext:
            myreturn += mytext
        elif mytext_error:
            myreturn += mytext_error
    except:
        print "error while executing the command on remote host"
        myreturn += "\n error while executing the command on remote host \n"

    try:
        sftp = etim_server.open_sftp()
        sftp.get(file_rec, rece_f_loc)
        sftp.close()
        if rece_f_loc:
            myreturn+="\n\n###########################################################\n\n" 
            myreturn+="download your file from http://23.21.167.60:8000/"+rece_f_loc.split('/')[-1] 

    except:
        print "error while get %s %s " % (file_rec, rece_f_loc)
        get_error = "error while receiving file from %s to %s " % (file_rec, rece_f_loc)
        myreturn += '\n'+get_error

    return myreturn






















class index:
    def GET(self):
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.formtest(form)

    def POST(self):
        toshow=''
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
            third_server=form['third_server'].value.encode('ascii', 'ignore') or None
            third_port=form['third_port'].value.encode('ascii', 'ignore') or None
            third_user=form['third_user'].value.encode('ascii', 'ignore') or None
            third_password=form['third_password'].value.encode('ascii', 'ignore') or None
            user_option=form['mydrop'].value
            file_rec=form['file_receive'].value.encode('ascii', 'ignore') or None
            rece_f_loc=form['file_receive_location'].value.encode('ascii', 'ignore') or None
            #file_send=form['file_send'].value.encode('ascii', 'ignore') or None
            send_f_loc=form['file_send_location'].value.encode('ascii', 'ignore') or None

            x = web.input(myfile={})
            filedir = '/tmp/' 
            if 'myfile' in x: 
                filepath=x.myfile.filename.replace('\\','/') 
                filename=filepath.split('/')[-1] 
                file_send = '/tmp/' + filename
                fout = open(filedir +'/'+ filename,'w') 
                fout.write(x.myfile.file.read()) 
                fout.close()


            print middle_server.encode('ascii','ignore'), middle_port, middle_user, middle_password, mycommand, file_send, file_rec, rece_f_loc, send_f_loc
            if user_option == 'value3':
                toshow+="############output of command  "+mycommand+"  ############## on server "+third_server+"  ####### \n\n"
                toshow+=mythirdconnect(middle_server, middle_port , middle_user , middle_password , second_server, second_port, second_user, second_password, third_server, third_port, third_user, third_password, mycommand , file_send, file_rec, rece_f_loc, send_f_loc)
            elif user_option == 'value2':
                toshow+="############output of command  "+mycommand+"  ############## on server "+second_server+"  ####### \n\n"
                toshow+=mysecondconnect(middle_server, middle_port , middle_user , middle_password , second_server, second_port, second_user, second_password, mycommand , file_send, file_rec, rece_f_loc, send_f_loc)
            else:
                toshow+="############output of command  "+mycommand+"  ############## on server "+middle_server+"  ####### \n\n"
                toshow+=myfirstconnect(middle_server, middle_port , middle_user , middle_password , mycommand , file_send, file_rec, rece_f_loc, send_f_loc)
            #return "Grrreat success! boe: %s, bax: %s" % (form['middle_server'].value, form['middle_port'].value)
            return toshow
 
              

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()

