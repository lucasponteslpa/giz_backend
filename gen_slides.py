import numpy as np

def add_frame(doc, text, title=None):
    doc += '\\begin{frame}\n'
    if title != None:
        doc += '\\frametitle{'+title+'}\n'
    doc += text+'\n'
    doc += '\\end{frame}\n'
    return doc

def load_head(doc):
    doc += '\\documentclass{beamer}\n\\usetheme{CambridgeUS}\n\\useinnertheme{rectangles}\n\\title{Aula}\n\\date{\\today}\n'
    return doc

def load_text(doc, text, title):
    text_split = text.split('.')
    for txt in text_split[:-1]:
        doc = add_frame(doc, txt, title=title)
    return doc

def load_cards(doc, cards):
    doc += '\\begin{document}\n'
    doc = add_frame(doc,'\\titlepage')
    for text in cards:
        doc = load_text(doc, text['texto'], text['título'])
    doc += '\\end{document}'
    return doc

# slide_file = open("cards_slide.tex","w")
# text = "Text of example.Text of example.Text of example.Text of example."
# doc = ""
# doc = load_head(doc)
# doc = load_doc(doc,text)

# slide_file.write(doc)
# slide_file.close()