from __future__ import print_function
from subprocess import call

def installPip(log=print):
    """
    Pip is the standard package manager for Python. Starting with Python 3.4
    it's included in the default installation, but older versions may need to
    download and install it. This code should pretty cleanly do just that.
    """
    log("Installing pip, the standard Python Package Manager, first")
    from os     import remove
    from urllib import urlretrieve
    urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
    call(["python", "get-pip.py"])

    # Clean up now...
    remove("get-pip.py")

def getPip(log=print):
    """
    Pip is the standard package manager for Python.
    This returns the path to the pip executable, installing it if necessary.
    """
    from os.path import isfile, join
    from sys     import prefix
    # Generate the path to where pip is or will be installed... this has been
    # tested and works on Windows, but will likely need tweaking for other OS's.
    # On OS X, I seem to have pip at /usr/local/bin/pip?
    pipPath = join(prefix, 'Scripts', 'pip.exe')

    # Check if pip is installed, and install it if it isn't.
    if not isfile(pipPath):
        installPip(log)
        if not isfile(pipPath):
            raise("Failed to find or install pip!")
    return pipPath

def installIfNeeded(moduleName, nameOnPip=None, notes="", log=print):
    """ Installs a Python library using pip, if it isn't already installed. """
    from pkgutil import iter_modules

    # Check if the module is installed
    if moduleName not in [tuple_[1] for tuple_ in iter_modules()]:
        log("Installing " + moduleName + notes + " Library for Python")
        call([getPip(log), "install", nameOnPip if nameOnPip else moduleName])



from datetime  import datetime 

# I like to have my messages timestamped so I can get an idea of how long they take.
def log(message):
    print(datetime.now().strftime("%a %b %d %H:%M:%S") + " - " + str(message))

# The name fabric doesn't really convey to the end user why the module is needed,
# so I include a very quick note that it's used for SSH.
installIfNeeded("paramiko", notes = " (ssh)", log = log)

# SoftLayer is actually named softlayer on pip.
installIfNeeded("SoftLayer", "softlayer", log = log)
