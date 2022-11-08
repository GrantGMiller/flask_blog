import flask_dictabase
import flask_login_dictabase_blueprint
from collections import namedtuple
from flask import Flask, render_template, redirect

import admin
import config
from post_model import Post

app = Flask('Blog')
app.config['SECRET_KEY'] = config.get(SECRET_KEY, '')

app.db = flask_dictabase.Dictabase(app)

app.register_blueprint(flask_login_dictabase_blueprint.bp)

Social = namedtuple('Social', ['url', 'type'])


@app.route('/')
def index():
    return render_template(
        'index.html',
        title=config.get('TITLE', 'Blog Title'),
        subtitle=config.get('SUBTITLE', 'Blog Subtitle'),
        posts=app.db.FindAll(Post, _reverse=True, public=True),
        socialMedia=[
            # Social('http://twitter.com', 'twitter'),
            # Social('http://facebook.com', 'facebook'),
            # Social('http://github.com', 'github'),
        ],
    )


@app.route('/post/<UUID>')
def view_post(UUID):
    post = app.db.FindOne(Post, uuid=UUID, public=True)
    if not post or not UUID:
        return redirect('/')
    else:
        return render_template(
            'post.html',
            post=post,
            title=config.get('TITLE', 'Blog Title'),
            subtitle=config.get('SUBTITLE', 'Blog Subtitle'),
        )


admin.setup(app)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
