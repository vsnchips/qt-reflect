"""
By Maxim Ellison, maxim@realityvirtual.co
v. alpha 1.0.0
This script simply creates a logger for any other script in the App
"""

# Imports
from logging import StreamHandler
import os
if not os.path.exists(os.getcwd() + '/App/logs'):
    os.mkdir(os.getcwd() + '/App/logs')
import time
import logging

import zmq

class logtoGuiHandler(logging.StreamHandler):
    
    def __init__(self,widget=None):
        self.level=10
        
        super().__init__(self)
        self.widget=widget

        # Logging Queue Server
         #TODO: Override for the multiprocessing case
        zmqContext = widget.zmqContext
        self.logSendSocket=zmqContext.socket(zmq.PAIR)
        address=f'inproc://{widget.name}_WidgetLogSock'
        print(f"Logger Connecting to address: {address}")
        
        self.logSendSocket.connect(address.format(widget.name))


    def flush(self):
        self.widget.logView.setText('')

    def emit(self,record):
        try:
        #TODO: Extend this with exception info for critical errors
            self.logSendSocket.send_string(str(record.msg)) 
            pass
        except:
            print("Failed to log this to the gui widget: {} ".format(record))
            raise   

   
# Definitions
def create_logger(name,widget=None):
    # Create a logger for JIT Orchestrator
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # Create a log file handler to write all logs
    try:
        os.remove(os.getcwd() + f'/App/logs/{name}.log')
    except:
        pass
    file_logger = logging.FileHandler(os.getcwd() + f'/App/logs/{name}.log')
    file_logger.setLevel(logging.DEBUG)
    # Create a console log handler to handle only ERROR level logs
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    # Create formatter and apply it to both handlers
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_logger.setFormatter(log_formatter)
    console_logger.setFormatter(log_formatter)
    # Add handlers to the logger
    logger.addHandler(file_logger)
    logger.addHandler(console_logger)

    if(widget is not None):
        logger.addHandler(logtoGuiHandler(widget=widget))

    return logger
