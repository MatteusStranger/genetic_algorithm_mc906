def clear_report():
    f = open("report.docx", "w")
    f.write('')
    f.close()

def write_text(text=""):
    print(text)

    f = open("report.docx", "a")
    f.write(str(text) + '\n')
    f.close()