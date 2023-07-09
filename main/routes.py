import os
import json
from operator import attrgetter
from flask import render_template, url_for, flash, redirect, request
from main import db, mail, app, bcrypt
from flask_login import current_user, login_user, logout_user, login_required
from main.models import Posts, Comment, Likes, Subscribers, Messages, MessageReply, User, Notification
from main.forms import CommentForm, SubscribeForm, ContactForm, PostForm, MessageReplyForm, RegistrationForm, LoginForm
from flask_mail import Message
from sqlalchemy.sql.expression import func
import re

@app.route("/", methods=["GET", "POST"])
def index():
    page = request.args.get('page', 1, type=int)
    # get posts data
    posts = Posts.query.order_by(Posts.created_at.desc())\
    .with_entities(Posts.id, Posts.title, Posts.url_title, Posts.summary, Posts.created_at, Posts.cover_img, Posts.views, Posts.likes, Posts.comments)\
    .paginate(page=page, per_page=3)
    no_of_pages = int((posts.total / posts.per_page)+1)

    liked={}
    for post in posts.items:
        like = Likes.query.filter_by(post_no = post.id).filter_by(ip_address = request.remote_addr).first()
        if like is None:
            liked[post.id]=False
        else:
            liked[post.id]=True
    return render_template("index.html", posts=posts, liked=liked, no_of_pages=no_of_pages)


@app.route("/post/<string:post_url>", methods=['GET', 'POST'])
def post(post_url):
    user_ip=request.remote_addr
    
    # get post details
    post = Posts.query.filter_by(url_title=post_url)\
        .with_entities(Posts.id, Posts.title, Posts.url_title, Posts.content, Posts.created_at, Posts.cover_img, Posts.views, Posts.likes, Posts.comments, Posts.related_1, Posts.related_2, Posts.related_3)\
        .first_or_404()

    # get related posts
    related_posts = Posts.query.filter(
        Posts.id.in_([post.related_1, post.related_2, post.related_3])
    ).with_entities(
        Posts.id, Posts.title, Posts.url_title, Posts.cover_img,
        Posts.views, Posts.comments, Posts.likes
    ).all()

    # if less than three related posts, then add random posts
    random_posts = []
    if len(related_posts) < 3:
        num_random_posts = 3 - len(related_posts)
        exclude_post_ids = [post.id] + [related_post.id for related_post in related_posts]
        random_posts = Posts.query.filter(
            ~Posts.id.in_(exclude_post_ids)  # Exclude the current post and related posts
        ).with_entities(
            Posts.id, Posts.title, Posts.url_title, Posts.cover_img,
            Posts.views, Posts.comments, Posts.likes
        ).order_by(func.random()).limit(num_random_posts).all()

    related_posts += random_posts

    related_posts = list(set(related_posts))
    related_posts = [related_post for related_post in related_posts if related_post.id != post.id]

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
    
    liked_related_posts = {}
    for related_post in related_posts:
        like = Likes.query.filter_by(post_no=related_post.id, ip_address=user_ip).first()
        if like is None:
            liked_related_posts[related_post.id] = False
        else:
            liked_related_posts[related_post.id] = True

    # register view
    Posts.query.filter_by(id=post.id).update(dict(views= post.views+1))

    # send notification when views reach a particular milestone
    if post.views % 10 == 0:
        notification_message = f"Your post '{post.title}' has reached {post.views} views!"
        notification = Notification(message=notification_message)
        db.session.add(notification)

    db.session.commit()
    
    # register comment 
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        Posts.query.filter_by(id=post.id).update(dict(comments= post.comments+1))
        comment = Comment(post_no=post.id, comment_no=post.comments + 1, comment=comment_form.text.data, name=comment_form.name.data, ip_address=user_ip)
        
        db.session.add(comment)

        notification_message = f"New comment on your post: {post.title}"
        notification = Notification(message=notification_message)

        db.session.add(notification)

        db.session.commit()
        return redirect(url_for('post', post_url=post.url_title))

    return render_template("post_page.html", comment_form=comment_form, post=post, liked=liked, comments=comments, related_posts=related_posts, liked_related_posts=liked_related_posts, by_user=by_user)

@app.route('/like/<string:post_id>')
def register_like(post_id):
    # get post details
    post = Posts.query.filter_by(id=post_id)\
        .with_entities(Posts.title, Posts.likes)\
        .first_or_404()
    user_ip = request.remote_addr

    likes = Likes.query.filter_by(post_no = post_id)\
    .filter_by(ip_address = user_ip)\
    .first()
    
    if likes is not None:
        Posts.query.filter_by(id=post_id).update(dict(likes = post.likes-1))
        like = Likes.query.filter_by(post_no = post_id).filter_by(ip_address = user_ip).first_or_404()
        db.session.delete(like)
        db.session.commit()
    else:
        Posts.query.filter_by(id=post_id).update(dict(likes = post.likes+1))
        like = Likes(post_no=post_id, ip_address = user_ip)
        db.session.add(like)
        db.session.commit()

        post = Posts.query.filter_by(id=post_id)\
        .with_entities(Posts.title, Posts.likes)\
        .first_or_404()
        
        if post.likes % 10 == 0:
            notification_message = f"Your post '{post.title}' has received {post.likes} likes!"
            notification = Notification(message=notification_message)
            db.session.add(notification)
            db.session.commit()

    return ('0')


@app.route('/delete_comment/<string:post_id>/<string:comment_id>', methods=['GET', 'POST'])
def delete_comment(comment_id, post_id):
    comment = Comment.query.filter_by(id = comment_id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    post = Posts.query.filter_by(id=post_id).with_entities(Posts.comments, Posts.url_title).first_or_404()
    Posts.query.filter_by(id=post_id).update(dict(comments = post.comments-1))
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

            notification_message = f"You got a new subscriber!"
            notification = Notification(message=notification_message)
            db.session.add(notification)
            db.session.commit()

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

        notification_message = f"You got a new message!"
        notification = Notification(message=notification_message)
        db.session.add(notification)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template("contact.html", contact_form=contact_form)


@app.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    posts = Posts.query.order_by(Posts.created_at.desc()).all()
    
    choices = [(post.id, post.title) for post in posts]

    if len(choices) == 0:
        default_choice = ('', 'No posts available')
        choices = [default_choice]
    else:
        choices.insert(0, ('', 'Random Post'))

    post_form = PostForm(selection_choices=choices)


    if post_form.validate_on_submit():
        flash("Post Created Successfully!", 'success')

        url_title = post_form.title.data
        url_title = re.sub('[^-.~0-9a-zA-Z ]', '', url_title)
        
        f = post_form.cover_img.data
        if f:
            filename = url_title + '.' + f.filename.rsplit('.', 1)[1].lower()
            f.save(os.path.join(app.root_path + '/static/post_img/' + filename))
        else:
            flash("Please provide a cover image.")
            return redirect(url_for("create_post", post_form=post_form))

        related_1 = int(post_form.related_1.data) if post_form.related_1.data else None
        related_2 = int(post_form.related_2.data) if post_form.related_2.data else None
        related_3 = int(post_form.related_3.data) if post_form.related_3.data else None

        post = Posts(title = post_form.title.data, url_title = url_title, content = post_form.content.data, summary = post_form.summary.data, cover_img = filename, related_1 = related_1, related_2 = related_2, related_3 = related_3)
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
    
    if len(recipients) != 0:
        subject = "New Post - "+post.title
        body = f"""New post out!
        {post.title}
        <hr>
        {post.summary}"""
        
        msg = Message(subject = subject, sender=app.config['MAIL_USERNAME'], recipients = recipients, body=body)
        mail.send(msg)

@app.route("/notifications")
@login_required
def view_notifications():
    notification_query = Notification.query.all()
    
    notifications = []
    for notification in notification_query:
        notifications.append(notification)

    if len(notifications) == 0:
        return render_template("notifications.html", no_notifications=True)
    else:
        notifications.sort(key=attrgetter('date'), reverse=True)
        notifications.sort(key=attrgetter('is_read'))
        return render_template("notifications.html", notifications=notifications, no_notifications=False)

@app.route('/read_notification/<string:notification_id>', methods=['GET', 'POST'])
@login_required
def read_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)

    if notification.is_read:
        notification.is_read = False
        flash('Notification marked as unread.', 'success')
    else:
        notification.is_read = True
        flash('Notification marked as read.', 'success')

    db.session.commit()
    return redirect(url_for('view_notifications'))

@app.route("/messages")
@login_required
def view_messages():
    message_query = Messages.query.all()
    reply_query = MessageReply.query.all()
    
    messages = []
    replies = {}
    for message in message_query:
        messages.append(message)
    for reply in reply_query:
        replies[reply.message_id] = reply.reply
    if len(messages) == 0:
        return render_template("messages.html", msg_len=len(messages))
    else:
        messages.sort(key=attrgetter('date'), reverse=True)
        messages.sort(key=attrgetter('replied'))
        messages.sort(key=attrgetter('read'))
        return render_template("messages.html", messages=messages, msg_len=len(messages), replies=replies)
    
@app.route('/delete_message/<string:message_id>', methods=['GET', 'POST'])
@login_required
def delete_message(message_id):
    message_id = int(message_id)
    message = Messages.query.filter_by(id = message_id).first_or_404()
    message_reply = MessageReply.query.filter_by(message_id = message_id).first()
    db.session.delete(message)
    db.session.delete(message_reply)
    db.session.commit()
    flash("Message deleted successfully.")
    return redirect(url_for('view_messages'))

@app.route('/read_message/<string:message_id>', methods=['GET', 'POST'])
@login_required
def read_message(message_id):
    message_id = int(message_id)
    message = Messages.query.filter_by(id = message_id).first_or_404()
    Messages.query.filter_by(id = message_id).update(dict(read = (not message.read)))
    db.session.commit()
    if message.read:
        flash("Message marked as unread.")
    else:
        flash("Message marked as read.")
    return redirect(url_for('view_messages'))

@app.route('/reply_message/<string:message_id>', methods=['GET', 'POST'])
@login_required
def reply_message(message_id):
    message = Messages.query.filter_by(id = message_id).first_or_404()
    # reply if exists
    reply = MessageReply.query.filter_by(message_id = message_id).first()
    reply_form = MessageReplyForm()

    if reply_form.validate_on_submit():
        subject = "Reply to your message"
        body = f"""Hello { message.name }!
        I am mailing regarding your message on my blog, The Bland Mirror.
        
        { reply_form.reply.data }"""
        
        msg = Message(subject = subject, sender=app.config['MAIL_USERNAME'], body=body, recipients=[message.email])
        mail.send(msg)

        Messages.query.filter_by(id = message_id).update(dict(replied = True, read = True))
        db.session.commit()
        reply = MessageReply(message_id = message_id, reply=reply_form.reply.data)
        db.session.add(reply)
        db.session.commit()

        flash("Replied sucessfully.")
        return redirect(url_for('view_messages'))

    return render_template("reply_message.html", reply_form = reply_form, message = message, reply= reply)

@app.route('/manage_posts', methods=['GET', 'POST'])
@login_required
def manage_posts(): 
    posts = Posts.query.order_by(Posts.created_at.desc())\
    .with_entities(Posts.id, Posts.title, Posts.url_title, Posts.summary, Posts.created_at, Posts.cover_img, Posts.views, Posts.likes, Posts.comments)\
    .all()
    posts_len=len(posts)
    return render_template("manage_posts.html", posts=posts, posts_len=posts_len)

@app.route('/delete_post/<string:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post_id = int(post_id)

    post = Posts.query.filter_by(id = post_id).first_or_404()
    likes = Likes.query.filter_by(post_no=post.id).all()
    comments =  Comment.query.filter_by(post_no=post.id).all()
    db.session.delete(post)
    for like in likes:
        db.session.delete(like)
    for comment in comments:
        db.session.delete(comment)
    db.session.commit()

    os.remove(os.path.join(app.root_path + '/static/post_img/' + post.cover_img))


    flash("Post deleted successfully.")
    return redirect(url_for('manage_posts'))

@app.route('/edit_post/<string:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post_id = int(post_id)
    old_post = Posts.query.filter_by(id = post_id).first_or_404()
    posts = Posts.query.order_by(Posts.created_at.desc()).all()#
    
    r1 = Posts.query.filter_by(id=old_post.related_1).first()
    r2 = Posts.query.filter_by(id=old_post.related_2).first()
    r3 = Posts.query.filter_by(id=old_post.related_3).first()

    choices = [(post.id, post.title) for post in posts]

    if len(choices) == 0:
        [('', 'No posts available')]
    else:
        choices.insert(0, ('', 'Random Post'))
        choices.remove((r1.id, r1.title))
        choices.insert(0, (r1.id, r1.title))
        
        choices.remove((r2.id, r2.title))
        choices.insert(0, (r2.id, r2.title))

        choices.remove((r3.id, r3.title))
        choices.insert(0, (r3.id, r3.title))

    post_form = PostForm(selection_choices=choices)

    if post_form.validate_on_submit():

        url_title = post_form.title.data
        url_title = re.sub('[^-.~0-9a-zA-Z ]', '', url_title)
        
        f = post_form.cover_img.data
        if f:
            os.remove(os.path.join(app.root_path + 'static','post_img', old_post.cover_img))
            filename = url_title + '.' + f.filename.rsplit('.', 1)[1].lower()
            f.save(os.path.join(app.root_path, 'static', 'post_img', filename))
        else:
            filename=old_post.cover_img

        related_1 = int(post_form.related_1.data) if post_form.related_1.data else None
        related_2 = int(post_form.related_2.data) if post_form.related_2.data else None
        related_3 = int(post_form.related_3.data) if post_form.related_3.data else None

        new_post = Posts(id = old_post.id, title = post_form.title.data, created_at = old_post.created_at, url_title = url_title, content = post_form.content.data, summary = post_form.summary.data, cover_img = filename, related_1 = related_1, related_2 = related_2, related_3 = related_3)
        
        likes = Likes.query.filter_by(post_no=old_post.id).all()
        comments =  Comment.query.filter_by(post_no=old_post.id).all()
        db.session.delete(old_post)
        for like in likes:
            db.session.delete(like)
        for comment in comments:
            db.session.delete(comment)
            
        db.session.add(new_post)
        db.session.commit()

        flash("Post Updated Successfully!", 'success')

        return redirect(url_for('index'))
    
    return render_template("edit_post.html", post_form=post_form, old_post=old_post)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('authors_home'))
        else:
            flash('Login unsuccessful, please check your email and password', 'danger')

    return render_template('login.html', form=form)

@app.route('/authors_home')
@login_required
def authors_home():
    unread_notifications = Notification.query.filter_by(is_read=False).count()
    flash(f'You have {unread_notifications} unread notifications')

    return render_template('authors_home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))