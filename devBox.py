
import traceback as tb

from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqode.core.widgets import TextCodeEdit

class liveEditor(TextCodeEdit):

    ''' A liveEditor is a TextCodeEdit box which executes highlighted code.
        F5 for execution in local scope, F6 to send to the Jupyter/IPython interpreter.
    '''
    def __init__(self,*args,overrideself=None,scopeConsole=None,**kwargs):

        ''' overrideself: the object from within which execution is to be scoped
            scopeConsole: IPython console to send variables and commands to            
        '''

        super().__init__(*args,**kwargs)
        self.key_pressed.connect(self.liveEditorKeyPressed)
        self.scopeConsole=scopeConsole
        
        if(overrideself is None):
            self.overrideself=self
        else:
            self.overrideself=overrideself

    #New methods are defined in the global namespace
    def scopeConsoleExecute(self,overrideself):
        ''' 
        Pushes overrideself to the console as self
        Sends the console highlighted code for execution
        '''
        code = self.textCursor().selectedText().replace('\u2029','\n')
        try:
                self.scopeConsole.pushVariables({'self':overrideself})
                self.scopeConsole.execute(code)

        except AttributeError:
            print("No console is bound to this editor!!")      

    def localExecute(self,overrideself):
        """
        Locally overrides self with overrideself
        Locally executes highlighted code
        """

        code = self.textCursor().selectedText().replace('\u2029','\n')
        try:
            self=overrideself
            exec(code)
        except:
            exc = tb.format_exc()
            print(exc)
            try:
                self.scopeConsole.printText(exc)
            except AttributeError:
                pass
        
    def liveEditorKeyPressed(self,event):
        ''' Keypress slot for F5 and F6'''
        if (event.key() == 16777268): #F5
            self.localExecute(self.overrideself)
        if (event.key() == 16777269): #F6
            self.scopeConsoleExecute(self.overrideself)

def liveEditorFactory(name='liveEdit',rootCons=None):
    ''' Decorator Factory creates a named live editor decorator '''
    def withLiveEditorDecorator(baseClass,name=name):

        ''' Returned decorator definition. Passes Factory arguments (name & rootCons) through kwargs '''
        # (I think this is a bit messy but it works. TODO: review this. )

        class liveVersion(baseClass):
            def __init__(self,scopeConsole=None,*args,_name=name,rootCons=rootCons,**kwargs):
                super(liveVersion,self).__init__(*args,**kwargs)
                
                self.editor = editor = liveEditor(scopeConsole=rootCons,overrideself=self)
                
                if (_name is None):
                    _name = baseClass.__str__()
                self.editor.setWindowTitle(_name)

                #If the hackable class is a QWidget, put it in a split with the liveEditor
                if (issubclass(baseClass,QWidget)):
                    try:
                        layout=self.layout()
                        if(layout is not None):
                            self.layout().addWidget(editor)
                        else:
                            self.container=container=QWidget()
                            container.setLayout(QHBoxLayout())
                            qs=self.devSplitter=QSplitter(Qt.Horizontal)
                            container.layout().addWidget(qs)
                            qs.addWidget(editor)
                            qs.addWidget(self)
                            container.show()
                            
                    except:
                        exc = tb.format_exc()
                        print(exc)
                editor.show()
                self.show()

            def linkConsole(self,console):
                self.editor.scopeConsole = console
        return liveVersion
    return withLiveEditorDecorator

# To put an object into a dev window, construct the split container, construct its liveEditor, put them in the split, and put the split into its parents' layout. 
def liveDevify(self,rootCons=None):
        self.editor = editor = liveEditor(scopeConsole=rootCons,overrideself=self)
        
        name=None
        if (hasattr(self,"name")):
            if self.name is not None:
                name=self.name
        if (name is None):
            name = self.name = self.__str__()
        self.editor.setWindowTitle(name)

        #If the hackable class is a QWidget, put it in a split with the liveEditor
        if (issubclass(self.__class__,QWidget)):
            try:
                layout=self.layout()
                if(layout is not None):
                    self.layout().addWidget(editor)
                else:
                    self.container=container=QWidget()
                    container.setLayout(QHBoxLayout())
                    qs=self.devSplitter=QSplitter(Qt.Horizontal)
                    container.layout().addWidget(qs)
                    
                    qs.addWidget(editor)
                    
                    #Swap it in
                    parent=self.parent()
                    qs.addWidget(self)
                    container.setParent(parent)
                    container.show()
                    
            except:
                exc = tb.format_exc()
                print(exc)
        editor.show()
        self.show()
