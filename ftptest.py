from ftplib import FTP
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import os

ftp = FTP('ec2-52-43-60-46.us-west-2.compute.amazonaws.com')
ftp.login(user='eqohireftp', passwd= 'eQoHire1234')

print(ftp.dir)

def read_file(filename):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pagenos = set()

    print("start of " + filename)
    ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write)

    fp = open(filename, 'rb')
    for page in PDFPage.get_pages(fp, pagenos):
        interpreter.process_page(page)
    fp.close()
    os.remove(filename)
    text = retstr.getvalue()
    print(text)

    device.close()
    retstr.close()

    print("end of " + filename)


def grab_file(folder, filename):
    ftp.retrbinary('RETR ' + filename, open(folder + filename, 'wb').write)


ftp.cwd('/resumes')
for filename in ftp.nlst():
    read_file(filename)

folder = 'resumes/'
ftp.cwd(folder)
for filename in ftp.nlst():
    grab_file(folder, filename)


ftp.quit()
