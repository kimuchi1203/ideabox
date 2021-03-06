from google.appengine.dist import use_library
use_library('django', '1.2')

import os
import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from idea import Idea
from idea import idea_create
from idea import idea_delete

import json

class MainPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            login_out_url = users.create_logout_url(self.request.uri)
        else:
            login_out_url = users.create_login_url(self.request.uri)

        idea_query = Idea.all()
        idea_list = idea_query.fetch(10)

        template_values = {
            'login_out_url': login_out_url,
            'idea_list' : idea_list,
            'user_name' : users.get_current_user(),
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class IdeaPost(webapp.RequestHandler):
    def post(self):
	if self.request.get('post_id') != "0":
            idea_target = Idea.get(db.Key.from_path('Idea', int(self.request.get('post_id'))))
            idea_target.idea_edit(self.request.get('content'))
	elif self.request.get('reply_id') != "0":
	    idea_target = Idea.get(db.Key.from_path('Idea', int(self.request.get('reply_id'))))
	    reply_idea = idea_create(self.request.get('content'), idea_target)
        else:
            new_idea = idea_create(self.request.get('content'), None)
        self.redirect('/')

class IdeaDelete(webapp.RequestHandler):
    def post(self):
        #idea_target = Idea.get_by_id(int(self.request.get('idea_id')))
        idea_target = Idea.get(db.Key.from_path('Idea', int(self.request.get('idea_id'))))
        # idea_delete(idea_target) is not work
        # idea_target.delete() is work
        idea_target.idea_delete_content()
        idea_target.put()
        self.redirect('/')

class IdeaList(webapp.RequestHandler):
    def get(self):
        idea_query = Idea.all()
        idea_list = idea_query.fetch(10)
        data = json.encode(idea_list)
        idlist = "[" + "{ user_name: \"" + str(users.get_current_user()) + "\"}, "
        for i in idea_list:
            idlist += "{ id: "
            idlist += str(i.key().id()) + " }, "

        idlist = idlist.rsplit(",", 1)[0]
        idlist += "]"
        data = data.split("[", 1)[1]
        data = "[" + idlist + ", " + data
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'  
        self.response.out.write(data)

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/ideapost', IdeaPost),
                                      ('/ideadelete', IdeaDelete),
                                      ('/idealist', IdeaList)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

