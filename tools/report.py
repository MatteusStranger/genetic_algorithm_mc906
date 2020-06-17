def clear_report():
    f = open("report.txt", "w")
    f.write('')
    f.close()

def write_text(text=""):
    # print(text)

    f = open("report.txt", "a")
    f.write(str(text) + '\n')
    f.close()