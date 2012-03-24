import cgi
from google.appengine.api import users
from google.appengine.ext import db

class Idea(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    parent_id = db.IntegerProperty()
    delete_flag = db.BooleanProperty()

    def idea_delete_content(self):
    # delete only content by user
        if self.author is not None and self.author == users.get_current_user():
            # self.content = "(deleted)"
            self.delete_flag = True

def idea_create(content_text, parent_idea):
	idea = Idea()
	if users.get_current_user():
		idea.author = users.get_current_user()
	idea.content = content_text
	idea.parent = parent_idea
        idea.delete_flag = False
	idea.put()

def idea_delete(idea):
	# delete tree for maintenance
	_childs = Idea.gql("WHERE ANCESTOR IS = :parent", parent=idea)
	childIds=[]
	for c in _childs:
		childIds.append(c.key().id())
	childs = Idea.get_by_id(ids=childIds, parent=idea)
	db.run_in_transaction(delete_cascade, idea, childs)

def delete_cascade(parent, childs):
	db.delete(childs)
	parent.delete()

# cf. http://sites.google.com/site/shin1ogawa/appengine
# cf. http://blog.livedoor.jp/chuhei1107/archives/51228163.html

