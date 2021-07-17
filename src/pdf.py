import os
import pathlib

def gen_pdf(company_name, user = ["CV", "Jan", "Lipski"]):
    [words_list, ending] = format(company_name)
    filename = "_".join(user + words_list)
    pdf_filename = filename + ".pdf"
    rodo_name = " ".join(words_list)
    if ending:
        rodo_name += " " + ending

    with open('template.tex', 'r') as file :
        filedata = file.read()
    filedata = filedata.replace("$company", rodo_name)
    with open('pdfbuild/template.tex', 'w') as file:
        file.write(filedata)

    genCmd = "mkdir pdfbuild ; cd pdfbuild ; pdflatex ./template.tex ; mv template.pdf " + pdf_filename
    cleanCmd = "rm template.out template.log template.aux template.tex"
    os.system("; ".join([genCmd, cleanCmd]))
    return str(pathlib.Path(__file__).parent.resolve()) + "/pdfbuild/" + pdf_filename

def format(txt):
    words_list = list(map(lambda x: x.capitalize() if x.isupper() or x.islower() else x, txt.split()))
    ending = ""
    cut_at = None
    for ind, word in enumerate(words_list):
        if "Sp" in word:
            ending = "Sp. z.o.o."
            cut_at = ind
        if "S." in word:
            ending = "S.A."
            cut_at = ind

    return [words_list[:cut_at], ending]


if __name__=="__main__":
    gen_pdf("HEX OCEAN lkj aaaa s.a.")
