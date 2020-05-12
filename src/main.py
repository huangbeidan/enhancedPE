import csv
import requests
from tika import parser
import re

import os.path
from os import path


def tika_parser(filename):
    raw = parser.from_file(filename)
    if 'content' in raw:
        text = raw['content']
    else:
        return
    safe_text = text.encode('utf-8', errors='ignore')
    safe_text = str(safe_text.strip())
    safe_text = str(safe_text).replace('\\', '\\\\').replace('"', '\\"').replace('\n', "")
    safe_text = re.sub(' +', ' ', safe_text)
    return safe_text



def getURL(filename):
    urls = []
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader)
        for row in spamreader:
            urls.append(row[4])
    return urls


def downloadPDFs(urls):
    i = 0
    for url in urls:
        if i < 30:
            r = requests.get(url, allow_redirects=True)
            filename = r.url.split('/')[-2]

            pathf = '../files/downloads' + filename

            if not path.exists(pathf):
                with open('../files/downloads/%s' % filename, 'wb') as f:
                    f.write(r.content)
                print("successfully download no. %s file" % i)
        i += 1


if __name__ == '__main__':
    ## Download pdfs from csv
     # urls = getURL("../files/SearchResults.csv")
     # downloadPDFs(urls)
     # print(urls)

     #tika_parser('../files/downloads/IF10553.pdf')

     # parse and write the contents to txt one by one
    mydir = '../files/downloads'
    outF = open('../out/corpus.txt', 'wb')
    for filename in os.listdir(mydir):
        if filename.endswith(".pdf"):
            safe_text = tika_parser(mydir + '/' + filename)
            outF.write(safe_text)
            outF.write('\n')
            print("successfully write filename %s" %filename)
    outF.close()








