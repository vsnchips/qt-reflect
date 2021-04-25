'''
General purpose decorators for exploring and interacting with the state of python objects
'''

from PyQtt.QtWidgets import QWidgets
from forbiddenfruit import curse 

class numBox(QWidget):
    def __init__(self,value,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setLayout(QVBoxLayout())
        lab=self.label=QLabel();
        lab.setText(str(value))

'''An object which contains builtin '''
def refreshWidgets(self):
    for name in dir(self):
        makeMonitorWidget(getattr(self,name))


''' Hacking an object viewer '''
obj=object()
class objectViewer(QWidget):
    def __init__(self,obj,*args,**kwargs):
        super().__init__(*args,**kwargs)
        labels=self.labels = []
        attrvals =self.attrvals = []
        
        self.setLayout(QVBoxLayout())
        for name in dir(obj):
            attr=getattr(obj,name)
            lab = QLabel()
            font=QFont()
            font.setPointSize(12)
            lab.setFont(font)

            
            lab.setText(f'{name}:{str(attr) }')
            
            self.labels.append(lab)
            self.attrvals.append(attr)
            self.layout().addWidget(lab)
            self.show()

objv = objectViewer(obj)

def makeObjectView(self,*args,**kwargs):
        
        
        for name in dir(self):
            if isinstance(float):
                
        
        super().__init(*args,**kwargs):
        self.setLayout(QVBoxLayout())
        
        
class extendObj():
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

exobj=extendObj()

''' Experimental '''
from forbiddenfruit import curse

def addWidget(self):
    self.widget=numBox(self)
    
curse(int,'addWidget',addWidget)

dir((0))
print(dir(0))

g=0
g.addWidget()
