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
from idea import idea_*
# (TODO) model の他も import する

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
        idea = Idea()
        if users.get_current_user():
            idea.author = users.get_current_user()

        idea.content = self.request.get('content')
        idea.put()
        self.redirect('/')

class IdeaDelete(webapp.RequestHandler):
    def post(self):
        # (TODO) まず delete_idea を呼ぶようにして試す
        # post に ID を入れて、 selected_idea を検索
        # idea_delete(selected_idea)
        # (TODO) その後 delete_idea_content にする
        self.redirect('/')

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/ideapost', IdeaPost),
                                      ('/ideadelete', IdeaDelete)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

