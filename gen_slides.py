from bs4 import BeautifulSoup as bs

def add_frame(doc, text, title=None):
    doc += '\\begin{frame}[allowframebreaks]\n'
    if title != None:
        doc += '\\frametitle{'+title+'}\n'
    doc += text+'\n'
    doc += '\\end{frame}\n'
    return doc

def load_head(doc):
    doc += '\\documentclass{beamer}\n\\usepackage[T1]{fontenc}\n\\usepackage[utf8]{inputenc}\n\\usepackage[brazilian]{babel}\n\\useinnertheme{rectangles}\n\\title{Aula}\n\\date{\\today}\n'
    return doc

def load_text(doc, text, title):
    #text_split = text.split('.')
    #for txt in text_split[:-1]:
    soup = bs(text)
    soup.encode("utf8")
    h1_title = soup.findAll("h1")[0].renderContents() 
    breakpoint()
    doc = add_frame(doc, text, title=title)
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
