from pyqode.core.widgets import TextCodeEdit

editor = TextCodeEdit()
editor.show()

def execute(state):
    global rootCons
    code = state.textCursor().selectedText().replace('\u2029','\n')
    rootCons.execute(code)
    from pyqode.core.widgets import TextCodeEdit

def editorKeyPressed(event):
    global rootCons,editor
    if (event.key() == 16777268):
        execute(editor)
    #print(event.key())

editor.key_pressed.connect(editorKeyPressed)
