#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import httplib


import wsgiref.handlers


from google.appengine.ext import webapp

URL = 'http://httpstatus.appspot.com/'
#URL = 'http://localhost:8083/'

LOCATION_HEADER_CODES = (300, 301, 302, 303, 307)


class MainHandler(webapp.RequestHandler):

  def get(self, code=200):
    self.response.headers['Content-Type'] = 'text/plain'
    code = int(code)
    
    if code is not 200 and httplib.responses.get(code):
        self.response.set_status(code)
        self.response.out.write(code)
        
        # Location header for redirect codes
        if code in LOCATION_HEADER_CODES:
            self.response.headers['Location'] = URL
    else:
        self.response.out.write("""USAGE
    http://httpstatus.appspot.com/[code]

DESCRIPTION
    Return HTTP response with status [code].
    Redirect loops can be tested by appending '/loop' to code 300-303 and 307.

EXAMPLES
    http://httpstatus.appspot.com/400
    http://httpstatus.appspot.com/301/loop

CODES
""")

        for response in httplib.responses:
            self.response.out.write("    %s: %s\n" % (response, httplib.responses[response]))

class MultipleRedirectHandler(webapp.RequestHandler):
    """Handle multiple redirect cases"""
    def get(self, code=300):
        code = int(code)
        if code in LOCATION_HEADER_CODES:
            self.response.set_status(code)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers['Location'] = '%s%d/loop' % (URL, code)
    
def main():
  application = webapp.WSGIApplication([('/', MainHandler), 
                                        ('/(?P<code>\d+)', MainHandler),
                                        ('/(?P<code>\d+)/loop', MultipleRedirectHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
