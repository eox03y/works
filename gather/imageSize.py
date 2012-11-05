import urllib

def getsize(uri):
    file = urllib.urlopen(uri)
    print file.headers
    size = file.headers.get("content-length")
    file.close()
    return int(size)

#print getsize("https://www.djangoproject.com/m/img/site/hdr_logo.gif")
print getsize("http://upload.ybmbooks.com/action/loadFile.asp?dType=pub&siteCode=WW_BOK&subDir=www\upfile\DataRoom\&pVal=CB5AA1BFA8F25E4DDEEC994AEAC770EE2637191B6A6ED7019A664BFB6DA7FA5739AEFF417DFF6199B21522D5C57BF25A8C15E56490A5BF7C437A9F96EE02678219C4B66DD958C1FA32CA023C9ABA6A42")
# 10965
