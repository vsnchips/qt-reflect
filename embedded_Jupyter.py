
import sys
from qtpy import QtWidgets

from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.manager import QtKernelManager

# The ID of an installed kernel, e.g. 'bash' or 'ir'.
USE_KERNEL = 'python3'

def make_jupyter_widget_with_kernel():
    """Start a kernel, connect to it, and create a RichJupyterWidget to use it
    """
    kernel_manager = QtKernelManager(kernel_name=USE_KERNEL)
    kernel_manager.start_kernel()

    kernel_client = kernel_manager.client()
    kernel_client.start_channels()

    jupyter_widget = RichJupyterWidget()
    jupyter_widget.kernel_manager = kernel_manager
    jupyter_widget.kernel_client = kernel_client
    return jupyter_widget


def pushVariables(self,variableDict):
    """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
    self.kernel_manager.kernel.shell.push(variableDict)
RichJupyterWidget.pushVariables=pushVariables

def clearTerminal(self):
    """ Clears the terminal """
    self._control.clear()    
RichJupyterWidget.clearTerminal=clearTerminal

'''
def printText(self,text):
    """ Prints some plain text to the console """
    self._append_plain_text(text)        
def executeCommand(self,command):
    """ Execute a command in the frame of the console widget """
    self._execute(command,False)
'''

class MainWindow(QtWidgets.QMainWindow):
    """A window that contains a single Qt console."""
    def __init__(self):
        super().__init__()
        self.jupyter_widget = make_jupyter_widget_with_kernel()
        self.setCentralWidget(self.jupyter_widget)

    def shutdown_kernel(self):
        print('Shutting down kernel...')
        self.jupyter_widget.kernel_client.stop_channels()
        self.jupyter_widget.kernel_manager.shutdown_kernel()