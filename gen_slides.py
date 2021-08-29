from bs4 import BeautifulSoup as bs
import re

def add_section(doc, text):
    doc += '\\section{'+text+'}\n'
    return doc


def add_subsection(doc, text):
    doc += '\\subsection{'+text+'}\n'
    return doc


def add_subsubsection(doc, text):
    doc += '\\subsubsection{'+text+'}\n'
    return doc

def add_frame(doc, text, title=None):
    if text != None:
        doc += '\\begin{frame}\n'
        if title is not None:
            doc += '\\frametitle{'+title+'}\n'
        doc += text+'\n'
        doc += '\\end{frame}\n'
    return doc

def add_image(doc, text, title=None):
    #split_tag = text.split('=')
    #img_path = split_tag[1][1:-3]
    img_path = re.findall('src="([^"]+)"', text, flags=0)[0]
    if img_path[-3:] != 'gif':
        text_frame= "\\begin{figure}[h]\\centering\\includegraphics[width=\\linewidth,height=0.8\\textheight,keepaspectratio]{"+img_path+"}\\end{figure}"
    # else:
    #     text_frame="\\begin{figure}[h]\\centering\\includemovie{\\linewidth}{\\textheight}{"+img_path+"}\\end{figure}"
        doc = add_frame(doc, text_frame, title=title)
    return doc

def load_head(doc):
    doc += '\\documentclass{beamer}\n\\usetheme{Hannover}\\usepackage[T1]{fontenc}\n\\usepackage[utf8]{inputenc}\n\\usepackage[brazilian]{babel}\n\\usepackage{movie15}\n\\useinnertheme{rectangles}\n\\title{Aula}\\author{Professor}\n\\institute{Escola}\n\\date{\\today}\n'
    return doc

def load_text(doc, text, title):
    #text_split = text.split('.')
    #for txt in text_split[:-1]:
    soup = bs(text, 'html.parser')
    #soup.encode("utf8")
    parsed_tag= {'h1_title' : soup.findAll("h1"),
                 'h2_title' : soup.findAll("h2"),
                 'h3_title' : soup.findAll("h3"),
                 'img_content' : soup.findAll("img"),
                 'content' : soup.findAll("p")}
    pos_cont_list = []
    for k_tag in parsed_tag.keys():
        tag = parsed_tag[k_tag]
        if tag != None:
            pos_cont_list += [(k_tag, (t.sourceline, t.sourcepos), t.string if k_tag != 'img_content' else str(t)) for t in tag]

    pos_list = [pos[1] for pos in pos_cont_list]

    def sort_list(lista):
        lista = sorted(lista, key=lambda x: x[0])
        aux = []
        aux2 = []
        aux3 = []

        for l in lista:
            if l[0] not in aux:
                aux.append(l[0])
                aux2 = sorted(aux2, key=lambda x: x[1])
                aux3 += aux2
                aux2 = [l]
            else:
                aux2.append(l)
        aux3 += aux2
        return aux3

    pos_list = sort_list(pos_list)
    content_dic = {pos: (k_tag, cont) for k_tag, pos, cont in pos_cont_list}
    
    #breakpoint()
    actual_title = title
    for p in pos_list:
        if content_dic[p][0] == 'h1_title':
            actual_title = content_dic[p][1]
            doc = add_section(doc, content_dic[p][1])
        elif content_dic[p][0] == 'h2_title':
            actual_title = content_dic[p][1]
            if parsed_tag['h1_title'] != None:
                doc = add_subsection(doc, content_dic[p][1])
            else:
                doc = add_section(doc, content_dic[p][1])
        elif content_dic[p][0] == 'h3_title':
            actual_title = content_dic[p][1]
            if (parsed_tag['h1_title'] != None and parsed_tag['h2_title'] == None) or (parsed_tag['h1_title'] == None and parsed_tag['h2_title'] != None):
                doc = add_subsection(doc, content_dic[p][1])
            elif parsed_tag['h1_title'] == None and parsed_tag['h2_title'] == None:
                doc = add_section(doc, content_dic[p][1])
            else:
                doc = add_subsubsection(doc, content_dic[p][1])
        elif content_dic[p][0] == 'img_content':
                doc = add_image(doc, content_dic[p][1], title=actual_title)
        elif content_dic[p][0] == 'content':
            doc = add_frame(doc, content_dic[p][1], title=actual_title)
    return doc

def load_cards(doc, cards):
    doc += '\\begin{document}\n'
    doc = add_frame(doc,'\\titlepage')
    doc = add_frame(doc, '\\tableofcontents',title='Sumário')
    for text in cards:
        doc = load_text(doc, text['texto'], text['titulo'])
    doc += '\\end{document}'
    return doc

# slide_file = open("cards_slide.tex","w")
# text = "Text of example.Text of example.Text of example.Text of example."
# doc = ""
# doc = load_head(doc)
# doc = load_doc(doc,text)

# slide_file.write(doc)
# slide_file.close()
