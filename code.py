import web
from web import form

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form( 
    form.Textbox("middle_server"), 
    form.Textbox("middle_port", 
        form.notnull,
        form.regexp('\d+', 'usually is 22'),
    form.Textbox('middle_user'),
    form.Textbox('middle_password'),
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
            print middle_server.encode('ascii','ignore'), middle_port, middle_user, middle_password, mycommand, file_send, file_rec, rece_f_loc, send_f_loc
            toshow=myfirstconnect(middle_server, middle_port , middle_user , middle_password , mycommand , file_send, file_rec, rece_f_loc, send_f_loc)
            #return "Grrreat success! boe: %s, bax: %s" % (form['middle_server'].value, form['middle_port'].value)
            return toshow

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
