"""
jupyter_app - run Jupyter lab as a desktop app

Usage:
    
* jupyter_app                   run Jupyter as an app
* jupyter_app --webruntime=xx   specify the runtime, (see webruntime module)
* jupyter_app --version         print version and exit
* jupyter_app --help            print this help and exit
"""

import os
import sys
import time
import threading
import _thread as thread
 
from tornado.httputil import url_concat
from notebook import DEFAULT_STATIC_FILES_PATH
from jupyterlab.labapp import LabApp
from webruntime import launch

__version__ = '0.1'


# Get location of Jupyter icon
iconfile = os.path.join(DEFAULT_STATIC_FILES_PATH, 'favicon.ico')
if not os.path.isfile(iconfile):
    iconfile = None

# Init web runtime
runtime = 'app'  # Good default that tries Firefox, NW.js (and Chrome on win)


class MyLabApp(LabApp):
    """ Subclass LabApp so we can launch our webruntime instead of the browser.
    """
    
    def start(self):
        url = self.connection_url
        if self.token and self._token_generated:
            url = url_concat(url, {'token': self.token})
        
        rt = launch(url, runtime,
                    title="Jupyterlab",
                    icon=iconfile,
                    size=(1024, 768)
                    )
        
        self._watcher = Watcher(rt._proc)
        self._watcher.start()
        
        self.open_browser = False
        super().start()


class Watcher(threading.Thread):
    """ Thread that stops Python when a given process (the runtime has stopped)
    """
    
    def __init__(self, process):
        super().__init__()
        self.process = process
        self.setDaemon(True)
    
    def run(self):
        while True:
            time.sleep(0.2)
            if self.process.poll() is not None:
                thread.interrupt_main()
                break


def main():
    
    global runtime
    
    for x in sys.argv[1:]:
        if x.startswith('--webruntime='):
            runtime = x.split('=', 1)[-1]
        elif x in ('-h', '--help'):
            print(__doc__.lstrip())
            return
        elif x in ('--version'):
            print(__version__)
            return
    
    assert runtime.endswith('app'), "Runtime needs to end in 'app'"
    MyLabApp.launch_instance()


if __name__ == '__main__':
    main()
