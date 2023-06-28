import os
from flask import render_template, url_for, flash, redirect, request
from .app import app, db, mail
from .models import Posts, Comment, Likes, Subscribers, Messages
from datetime import datetime
from .forms import CommentForm, SubscribeForm, ContactForm, PostForm
from flask_mail import Message
import re


@app.route("/", methods=["GET", "POST"])
def index():
    page = request.args.get('page', 1, type=int)
    # get posts data
    posts = Posts.query.order_by(Posts.created_at.desc())\
    .with_entities(Posts.id, Posts.title, Posts.url_title, Posts.summary, Posts.created_at, Posts.cover_img, Posts.views, Posts.likes, Posts.comments)\
    .paginate(page=page, per_page=3)
    no_of_pages = int((posts.total / posts.per_page)+1)

    liked=[]
    posts_for_likes = Posts.query.all()
    for post in posts_for_likes:
        like = Likes.query.filter_by(post_no = post.id).filter_by(ip_address = request.remote_addr).first()
        if like is None:
            liked.append(False)
        else:
            liked.append(True)
    return render_template("index.html", posts=posts, liked=liked, no_of_pages=no_of_pages)


@app.route("/post/<string:post_url>", methods=['GET', 'POST'])
def post(post_url):
    user_ip=request.remote_addr
    
    # get post details
    post = Posts.query.filter_by(url_title=post_url)\
        .with_entities(Posts.id, Posts.title, Posts.url_title, Posts.content, Posts.created_at, Posts.cover_img, Posts.views, Posts.likes, Posts.comments, Posts.related_1, Posts.related_2, Posts.related_3)\
        .first_or_404()

    like = Likes.query.filter_by(post_no = post.id).filter_by(ip_address = user_ip).first()
    if like is None:
        liked = False
    else:
        liked = True

    # get comments
    comments = Comment.query.order_by(Comment.comment_no.desc())\
    .with_entities(Comment.id, Comment.comment, Comment.name, Comment.date, Comment.comment_no, Comment.ip_address)\
    .filter_by(post_no = post.id)\
    .all()

    by_user={}
    for comment in comments:
        if comment.ip_address == user_ip:
            by_user[comment.id] = True 
        else:
            by_user[comment.id] = False
    
    # get related post details
    related_post_1 = Posts.query.filter_by(id=post.related_1)\
        .with_entities(Posts.id, Posts.title, Posts.url_title, Posts, Posts.cover_img, Posts.views, Posts.comments, Posts.likes)\
        .first_or_404()
    related_post_2 = Posts.query.filter_by(id=post.related_2)\
        .with_entities(Posts.id, Posts.title, Posts.url_title, Posts.cover_img, Posts.views, Posts.comments, Posts.likes)\
        .first_or_404()
    related_post_3 = Posts.query.filter_by(id=post.related_3)\
        .with_entities(Posts.id, Posts.title, Posts.url_title, Posts.cover_img, Posts.views, Posts.comments, Posts.likes)\
        .first_or_404()

    like_rp1 = Likes.query.filter_by(post_no = related_post_1.id).filter_by(ip_address = user_ip).first()
    like_rp2 = Likes.query.filter_by(post_no = related_post_2.id).filter_by(ip_address = user_ip).first()
    like_rp3 = Likes.query.filter_by(post_no = related_post_3.id).filter_by(ip_address = user_ip).first()
    if like_rp1 is None:
        liked_rp1 = False
    else:
        liked_rp1 = True
    if like_rp2 is None:
        liked_rp2 = False
    else:
        liked_rp2 = True
    if like_rp3 is None:
        liked_rp3 = False
    else:
        liked_rp3 = True

    # register view
    update_post_views = Posts.query.filter_by(id=post.id).update(dict(views= post.views+1))
    db.session.commit()
    
    # register comment 
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        update_post_comment = Posts.query.filter_by(id=post.id).update(dict(comments= post.comments+1))
        comment = Comment(post_no=post.id, comment_no=post.comments + 1, comment=comment_form.text.data, name=comment_form.name.data, ip_address=user_ip)
        
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post',  post_url=post.url_title))
    # return
    return render_template("post_page.html", comment_form=comment_form, post=post, liked=liked, liked_rp1=liked_rp1, liked_rp2=liked_rp2, liked_rp3=liked_rp3, comments=comments, rp1 = related_post_1, rp2 = related_post_2, rp3 = related_post_3, by_user=by_user)


@app.route('/like/<string:post_id>')
def register_like(post_id):
    # get post details
    post = Posts.query.filter_by(id=post_id)\
        .with_entities(Posts.likes)\
        .first_or_404()
    user_ip = request.remote_addr

    likes = Likes.query.filter_by(post_no = post_id)\
    .filter_by(ip_address = user_ip)\
    .first()
    
    if likes is not None:
        update_post_like = Posts.query.filter_by(id=post_id).update(dict(likes = post.likes-1))
        like = Likes.query.filter_by(post_no = post_id).filter_by(ip_address = user_ip).first_or_404()
        db.session.delete(like)
        db.session.commit()
    else:
        update_post_like = Posts.query.filter_by(id=post_id).update(dict(likes = post.likes+1))
        like = Likes(post_no=post_id, ip_address = user_ip)
        db.session.add(like)
        db.session.commit()

    return ('0')


@app.route('/delete_comment/<string:post_id>/<string:comment_id>', methods=['GET', 'POST'])
def delete_comment(comment_id, post_id):
    comment = Comment.query.filter_by(id = comment_id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    post = Posts.query.filter_by(id=post_id).with_entities(Posts.comments, Posts.url_title).first_or_404()
    update_post_comment = Posts.query.filter_by(id=post_id).update(dict(comments = post.comments-1))
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect(url_for('post',  post_url=post.url_title))

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
     # register subscriber
    subscriber_form=SubscribeForm()
    if subscriber_form.validate_on_submit():
        search = Subscribers.query.filter_by(email = subscriber_form.email.data).first()
        if search is None:
            subscriber = Subscribers(email = subscriber_form.email.data)
            db.session.add(subscriber)
            db.session.commit()
            flash('Thank you for subscribing!', 'success')
            return redirect(url_for('index'))
        else:
            flash('This email address is already subscribed.', 'error')
            return redirect(url_for('subscribe'))
    return render_template("subscribe.html", subscriber_form=subscriber_form)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form=ContactForm()
    if contact_form.validate_on_submit():
        contact=Messages(name=contact_form.name.data, email=contact_form.email.data, message=contact_form.message.data)
        db.session.add(contact)
        db.session.commit()
        flash('Message sent.', 'success')
        return redirect(url_for('index'))
    return render_template("contact.html", contact_form=contact_form)


@app.route("/create_post", methods=['GET', 'POST'])
def create_post():
    posts = Posts.query.order_by(Posts.created_at.desc())\
        .with_entities(Posts.title)
    
    choices = []
    for post in posts:
        for x in post:
            choices.append(x)
    
    post_form=PostForm(selection_choices=choices)

    if post_form.validate_on_submit():
        flash("Post Created Successfully!", 'success')

        url_title = post_form.title.data
        url_title = url_title.replace(" ", "_")
        url_title = re.sub('[^-._~0-9a-zA-Z]', '', url_title)
        
        f = post_form.cover_img.data
        filename = url_title + '.' + f.filename.rsplit('.', 1)[1].lower()
        f.save(os.path.join(app.root_path+ '\static\post_img\\' + filename))

        post = Posts(title = post_form.title.data, url_title = url_title, content = post_form.content.data, summary = post_form.summary.data, cover_img = filename, related_1 = post_form.related_1.data, related_2 = post_form.related_2.data, related_3 = post_form.related_3.data)
        db.session.add(post)
        db.session.commit()

        send_email_for_new_post(post)

        return redirect(url_for('index'))
        
    return render_template("new_post.html", post_form=post_form)

def send_email_for_new_post(post):
    query = Subscribers.query.with_entities(Subscribers.email)
    recipients = []
    for recipient in query:
        recipients.append(recipient[0])
    print(recipients)
    
    subject = "New Post - "+post.title
    body = f"""New post out!
    {post.title}
    <hr>
    {post.summary}"""
    
    msg = Message(subject = subject, sender=os.getenv('MAIL_USERNAME'), recipients = recipients, body=body)
    # mail.send(msg)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404    
