'''
Created on 2017415

@author: zhou
'''

# from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash, abort, request, make_response, g
from flask import jsonify
from .. import db
from ..models import User, Role, Permission, Post, Comment
from . import main
from .forms import NameForm, ChangePw, EditProfileForm, EditProfileAdminForm, PostForm, CommentForm, SearchForm
from datetime import datetime
from flask_login import login_required
from flask_login.utils import current_user
from ..decorators import admin_required, permission_required
from jinja2.compiler import UndeclaredNameVisitor
from .forms import EditProfileAdminForm
# from PIL import Image
import os
# from ..useredis import mark_online, get_online_users, get_user_last_activity
# from ..API.queryIP import queryip
from ..api.check_mobile import checkMobile


@main.route('/author/<authorname>')
def author_search(authorname):
    results = Post.query.filter_by(original=authorname).all()
    return render_template('authorlist.html', results=results, query=authorname)


@main.route('/search_result/<query>')
def search_results(query):
    results = Post.query.msearch(query, fields=['body'], limit=20).all()
    return render_template('search_results.html', results=results, query=query)


@main.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('search', '')
    if query == '':
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.search_results', query=query))


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(page,
                                                                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/post/publish', methods=['GET', 'POST'])
@login_required
def publish_blog():
    return render_template('publish_blog.html')


@main.route('/publish/post', methods=['GET', 'POST'])
@login_required
def publish_post():
    postname = request.form.get('postname', '')
    novelname = request.form.get('novelname', '')
    body = request.form.get('postbody', '')
    original = request.form.get('original', '')
    picture = request.form.get('picture', '')
    tag = request.form.get('tag', '')
    # print(body)
    if postname is not None and body is not None and current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body=body, postname=postname, author=current_user._get_current_object(), novelname=novelname,
                    original=original, picture=picture, tag=tag)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.profile', username=current_user.username))


def add_ele(e):
    return '<p>%s</p>' % e


@main.route('/publish/api/post', methods=['POST'])
def publish_api_post():
    data = request.get_json()
    if data['key'] is None or data['key'] != current_app.config['SECRET_KEY']:
        return jsonify(
            {
                "code": 1000,
                "message": "You have no permission to access this api"
            }
        ), 403
    name = data['name']
    chapter = data['chapter']
    print(chapter)
    postname = data['postname']
    novelname = data['novelname']
    get_body = data['postbody']
    body_list = list(map(add_ele, get_body))
    body = "".join(body_list)
    original = data['original']
    picture = data['picture']
    author_id = data['author_id']
    tag = data['tag']
    if postname is not None and body is not None:
        if chapter is "" or name is "":
            post = Post(body=body, postname=postname, author_id=author_id,
                        original=original, picture=picture, tag=tag, novelname=novelname)
            db.session.add(post)
            db.session.commit()
        else:
            post = Post(body=body, postname=name + '-' + chapter + '-' + postname, author_id=1,
                        original=original, picture=picture, tag=tag, novelname=novelname)
            db.session.add(post)
            db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Success"
            }
        ), 200


@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page,
                                                                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                     error_out=False)
    posts = pagination.items
    last = user.last_seen.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('profile.html', user=user, posts=posts, pagination=pagination, last=last)


@main.route('/novelnamelist/<novelname>')
def novel_by_name(novelname):
    page = request.args.get('page', 1, type=int)
    novel = Post.query.filter_by(novelname=novelname).paginate(page,
                                                                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                     error_out=False)
    if novel is None:
        abort(404)
    posts = novel.items
    return render_template('novel_list_by_name.html', posts=posts, novelname=novelname)


@main.route('/noveltaglist/<tag>')
def novel_by_tag(tag):
    page = request.args.get('page', 1, type=int)
    novel = Post.query.filter_by(tag=tag).paginate(page,
                                                    per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                            error_out=False)
    if novel is None:
        abort(404)
    posts = novel.items
    return render_template('novel_list_by_tag.html', posts=posts, tag=tag)


@main.route('/manage-profile')
@login_required
def manage_profile():
    return render_template('manage_profile.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page,
                                                                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                     error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)


@main.route('/changepw',methods=['GET', 'POST'])
@login_required
def changepw():
    form = ChangePw()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your have changed your password!')
            return redirect(url_for('main.profile'))
        else:
            flash('Enter invalid password')
    return render_template('/changepw.html', form=form)


@main.route('/admin')
@login_required
@admin_required
def admin_only():
    return "For admin only!"


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/admin/mange-user')
@login_required
@admin_required
def manage_user():
    users = User.query.all()
    print(users)
    return render_template('manage_user.html', users=users)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    post.readtimes += 1
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated is False:
            comment = Comment(body=form.body.data, post=post)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('.post', id=post.id, page=-1))
        comment = Comment(body=form.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False
        )
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        post.postname = form.postname.data
        post.novelname = form.noveLname.data
        post.original = form.original.data
        post.picture = form.picture.data
        post.tag = form.tag.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    form.postname.data = post.postname
    form.noveLname.data = post.novelname
    form.original.data = post.original
    form.picture.data = post.picture
    form.tag.data = post.tag
    return render_template('edit_post.html', form=form, post=post)


@main.route('/edit/post/delete/<int:id>')
@login_required
def edit_delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.is_administrator:
        abort(403)
    com = Comment.query.filter_by(post_id=id).first()
    if com:
        db.session.delete(com)
    db.session.delete(post)
    return redirect(url_for('main.user', username=current_user.username))


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
                                         error_out=False)
    follows = [{'user':item.follower, 'timestamp':item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of", endpoint='.followers',
                           pagination=pagination, follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]    
    return render_template('followers.html', user=user, title="Followed by", endpoint='.followed_by',
                           pagination=pagination, follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False
        )
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))
