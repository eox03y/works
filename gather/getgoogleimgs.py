#!/usr/bin/env python
import geturl

def strip_google_img_info_field(field):
        field = field.strip()
        field = field.strip('"')
        return field
        
class googleimg:
	def __init__(self, query, debug=0):
		"""
		get HTML contents at a given url 'urlstr'
		"""			
		self.debug = debug
		urlstr = "http://images.google.com/images?svnum=10&hl=en&gbv=2&q=%s" % (query)
		self.geturl = geturl.geturl(urlstr)
		if debug: 
			print '### DATA size:', len(self.geturl.data)
			
		self.getimglist(self.geturl.data)

        def getimglist(self, htmldata):
            #print htmldata
            ptr = 0
            self.imgcnt = 0
            while ptr < len(htmldata):
                pos = htmldata.find("dyn.Img", ptr)
                if pos < 0: break

                spos = htmldata.find("(", pos)
                if spos < 0: break

                epos = htmldata.find(")", spos)
                if epos < 0: break

                imginfo = htmldata[spos+1:epos]
                ptr = epos + 1
                self.imgcnt += 1

                try:
                    self.parimginfo(imginfo)
                except:
                    pass
                
        def parimginfo(self, imginfo):
                print imginfo
                flds = imginfo.split(",")
                flds = map(strip_google_img_info_field, flds)
                print "ORG = ", flds[3]
                print "DESC = ", flds[6]
                print "GOOGLE IMG ID = ", flds[2]
                print "GOOGLE IMG HOST = ", flds[-1]
                print "GOOGLE IMG CACHE = ", "%s?q=tbn:%s%s" % (flds[-1], flds[2], flds[3]) 
                

if __name__ == "__main__":
	import sys

	if len(sys.argv) > 1: query = sys.argv[1]
	else: query = "anydict"


	a = googleimg(query, debug=1)			
