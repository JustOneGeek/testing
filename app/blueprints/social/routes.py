from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from .models import Post
from .import bp as social
from app.blueprints.auth.models import User

#Routes
# Homepage Shows all posts
@social.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method=='POST':
        body=request.form.get('body')
        new_post=Post(user_id=current_user.id,body=body)
        new_post.save()
        #add redirect here to avoid double post

    posts= current_user.followed_posts()
    return render_template('index.html.j2', posts=posts)
    
# Page for one post 
@social.route('/post/<int:id>')
@login_required
def get_post(id):
    post= Post.query.get(id)
    return render_template('single_post.html', post=post, view_all=True)

# Page to show all user posts
@social.route('/post/my_posts')
@login_required
def my_posts():
    posts = current_user.posts
    return render_template('my_posts.html.j2',posts=posts)

@social.route('/show_users')
@login_required
def show_users():
    users=User.query.all()
    print(users)
    return render_template('show_users.html.j2' , users = users)

@social.route('/follow/<int:id>')
@login_required
def follow(id):
    user_to_follow=User.query.get(id)
    current_user.follow(user_to_follow)
    flash(f"You are now following {user_to_follow.first_name} {user_to_follow.last_name}", 'success')
    return redirect(url_for('social.show_users'))

@social.route('/unfollow/<int:id>')
@login_required
def unfollow(id):
    user_to_follow=User.query.get(id)
    current_user.unfollow(user_to_follow)
    flash(f"You are no longer following {user_to_follow.first_name} {user_to_follow.last_name}", 'warning')
    return redirect(url_for('social.show_users'))

@social.route('/edit_post/<int:id>', methods=["GET","POST"])
@login_required
def edit_post(id):
    post= Post.query.get(id)
    if request.method == 'POST':
        post.edit(request.form.get("body"))
        flash("Your post has been edited","success")
        ### Add a Redirect here.....to prevent post on refresh
    return render_template('edit_post.html', post=post)
