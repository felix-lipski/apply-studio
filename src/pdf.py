import os, pathlib, csv

from ui import print_center_msg

def gen_pdf(term, offer, user = ["CV", "Jan", "Lipski"]):
    company_name = offer["company"]
    job_title = offer["title"]
    [words_list, ending] = format(company_name)
    filename = "_".join(user + words_list)
    pdf_filename = filename + ".pdf"
    rodo_name = " ".join(words_list)
    if ending:
        rodo_name += " " + ending

    print_center_msg(term, "Generating " + filename + "...", term.black_on_yellow)

    with open('data/pdf/template.tex', 'r') as file :
        filedata = file.read()
    filedata = filedata.replace("$company", rodo_name)
    with open('data/pdf/with_company.tex', 'w') as file:
        file.write(filedata)
        
    genCmd = "mkdir data/pdf ; cd data/pdf ; pdflatex ./with_company.tex ; mv with_company.pdf " + pdf_filename
    cleanCmd = "rm with_company.out with_company.log with_company.aux"
    os.system("; ".join([genCmd, cleanCmd]))

    with open('data/pdf/generated.csv', 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([company_name, job_title])

    print_center_msg(term, filename + "generated!", term.black_on_green)
    
    return str(pathlib.Path(__file__).parent.resolve()) + "/data/pdf/" + pdf_filename

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
    offer = {
            "title" : "Computer Developer",
            "company" : "A Good Company"
            }
    gen_pdf(offer)
