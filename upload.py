import web

urls = ('/upload', 'Upload')

class Upload:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = '/tmp/' 
        if 'myfile' in x: 
            filepath=x.myfile.filename.replace('\\','/') 
            filename=filepath.split('/')[-1] 
            fout = open(filedir +'/'+ filename,'w') 
            fout.write(x.myfile.file.read()) 
            fout.close()

if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()