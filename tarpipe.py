"""

TarPipe Python API

http://code.google.com/p/tarpipe-python/

(c) 2008 Alcides Aguiar Fonseca
	(Under LGPL)

To get you started:

import tarpipe

t = tarpipe.TarPipe(token="your workflow token")
t.upload(title="hello from python",body="testing TarPipe from Python",image="/Users/youruser/Images/test.png")

That's it :)

"""

import urllib
import urllib2
import httplib
import mimetypes
import mimetools

endpoint = "http://rest.receptor.tarpipe.net:8000/"


class NoWorkflowToken(Exception):
	def __str__(self):
		return "TarPipe API requires your Workflow Token"

class TarPipe:
	""" Representative class for TarPipe Uploader """
	
	def __init__(self,token=""):
		self.token = token
		
	def upload(self,title="",body="",image="",token=""):
		""" Function that does the upload to TarPipe. It can take title, body, image path and the token if not defined in the class."""
		if token:
			self.token = token
		if self.token == "":
			raise NoWorkflowToken
		else:		
			return self.post(endpoint + "?key=" + self.token, {'title':title,'body':body},{'image':image})
				
	def post(self,url,values,files):
		""" Abstraction of HTTP POST """
		
		def post_multipart(req, fields, files):
			content_type, body = encode_multipart_formdata(fields, files)
			h = httplib.HTTPConnection(req.get_host())  
			headers = {
				'User-Agent': 'TarPipe-Python',
				'Content-Type': content_type
				}
			h.request('POST', req.get_selector(), body, headers)
			res = h.getresponse()
			return res.read()
			
		def encode_multipart_formdata(fields, files, BOUNDARY = '-----'+mimetools.choose_boundary()+'-----'):
			"""
			fields is a sequence of (name, value) elements for regular form fields.
			files is a sequence of (name, filename, value) elements for data to be uploaded as files
			Return (content_type, body) ready for httplib.HTTP instance
			"""
			CRLF = '\r\n'
			L = []
			for (key, value) in fields:
				L.append('--' + BOUNDARY)
				L.append('Content-Disposition: form-data; name="%s"' % key)
				L.append('')
				L.append(value)
			for (key, filename, value) in files:
				L.append('--' + BOUNDARY)
				L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
				L.append('Content-Type: %s' % get_content_type(filename))
				L.append('')
				L.append(value)
			L.append('--' + BOUNDARY + '--')
			L.append('')
			body = CRLF.join(L)
			content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
			return content_type, body

		def get_content_type(filename):
			return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
		
		
		data = [ (k,values[k]) for k in values if values[k] ]		
		files = [ (k,files[k],open(files[k],"rb").read()) for k in files if files[k] ]
		
		req = urllib2.Request(url)
		response = post_multipart(req,data,files)
		
		return response
		
		
if __name__ == '__main__':
	t = TarPipe(token = raw_input("Your workflow token:\t"))
	print t.upload(title=raw_input("Title:\t"),body=raw_input("Body:\t"),image=raw_input("Image URL:\t"))
	