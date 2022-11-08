import datetime
import uuid

from flask import render_template, redirect, request, jsonify
from flask_login_dictabase_blueprint import VerifyAdmin, AddAdmin
from flask_login_dictabase_blueprint.menu import GetMenu

from post_model import Post


def setup(app):
    AddAdmin('grant@grant-miller.com')

    @app.route('/admin')
    @VerifyAdmin
    def admin():
        return redirect('/admin/list_all_posts')

    @app.route('/admin/list_all_post')
    @app.route('/admin/list_all_posts')
    def admin_list_post():
        return render_template(
            'admin_list_post.html',
            posts=app.db.FindAll(Post, _reverse=True),
            menu=GetMenu()
        )

    @app.route('/admin/new_post')
    @VerifyAdmin
    def admin_new_post():
        return redirect(f'/admin/edit_post/{uuid.uuid4()}')

    @app.route('/admin/edit_post/<UUID>', methods=['GET', 'POST'])
    @VerifyAdmin
    def admin_edit_post(UUID):
        post = app.db.NewOrFind(
            Post,
            uuid=UUID or request.form['uuid'])

        if request.method == 'POST':

            post.Update(dict(
                title=request.form.get('title', ''),
                subtitle=request.form.get('subtitle', ''),
                body=request.form.get('body', ''),
                created=post.get('created', None) or datetime.datetime.now(),
                modified=datetime.datetime.now(),
            ))

            return redirect('/admin/list_all_posts')

        elif request.method == 'GET':
            return render_template(
                'admin_edit_post.html',
                post=post,
                menu=GetMenu(),
                uuid=post['uuid'],
            )

    @app.route('/admin/delete_all')
    @VerifyAdmin
    def admin_delete_all():
        app.db.Drop(Post, confirm=True)
        return redirect('/admin/list_all_posts')

    @app.route('/post/public/<UUID>/<value>')
    def post_public(UUID, value):
        print('UUID=', UUID, ', value=', value)
        post = app.db.FindOne(Post, uuid=UUID)
        if post:
            if value == 'true':
                post['public'] = True
            else:
                post['public'] = False
            return jsonify(post.ui_safe())
