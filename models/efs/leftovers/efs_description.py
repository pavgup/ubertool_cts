# -*- coding: utf-8 -*-
#"""
#Created on Tue Jan 03 13:30:41 2012#
#
#@author: mg
#"""
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os

class EFSDescriptionPage(webapp.RequestHandler):
    def get(self):
        text_file2 = open('efs/efs_text.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01cts_uberheader.html', {'title'})
        html = html + template.render(templatepath + '02cts_uberintroblock_wmodellinks.html', {'model':'efs','page':'description'})
        html = html + template.render (templatepath + '03cts_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04ubertext_start.html', {
	#		'model_page':'http://www.epa.gov/oppefed1/models/terrestrial/sip/sip_user_guide.html',
			'model_attributes':'EFS Overview',
                 'text_paragraph':xx})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05cts_ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06cts_uberfooter.html', {'links': ''})
	
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', EFSDescriptionPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
