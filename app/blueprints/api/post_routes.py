from . import bp as api
from app.blueprints.social.models import Post
from app.blueprints.auth.models import User
from app.blueprints.auth.auth import token_auth
from flask import request, make_response, g
# import base64

# # helper functions
# def get_basic_auth_creds(auth_header):
#     encoded_username_password = auth_header.replace('Basic ','').strip()
#     username_password=base64.b64decode(encoded_username_password).decode('ascii')
#     username, password = username_password.split(':')
#     username=username.strip()
#     return username, password

# def get_user_from_header(auth_header):
#     # get the token from the header
#     # token=auth_header.replace('Bearer ','').strip()
#     # look up user by the token
#     # user=User.query.filter_by(token=token).first()
#     user=token_auth.current_user()
#     return user



# this is so another application can talk to our social media service

# this will return all posts in our database that the user is following and their own
@api.get('/all_posts')
@token_auth.login_required()
def get_all_posts():
    # get the token from the header
    # auth_header=request.headers.get('Authorization')
    user=g.current_user

    posts=user.followed_posts()
    response_list=[]
    for post in posts:
        post_dict={
            "id":post.id,
            "body":post.body,
            "date_created":post.date_created,
            "date_updated":post.date_updated,
            "author":post.author.first_name + ' ' + post.author.last_name,
        }
        response_list.append(post_dict)
    return make_response({"posts":response_list},200)


# this will return a post
@api.get('/posts')
@token_auth.login_required()
def get_post_api():
    user=g.current_user
    # Get Data from request body
    data_from_request=request.get_json()
    post = Post.query.get(data_from_request['id'])

    # Check if the user has privs to see this post
    if not user.is_following(post.author):
        return make_response("Cannot get a post for the user is not following", 403)

    if not post:
        return make_response(f"Post id: {post.id} does not exist",404)
    response_dict={
        "id":post.id,
        "body":post.body,
        "date_created":post.date_created,
        "date_updated":post.date_updated,
        "author":post.author.first_name + ' ' + post.author.last_name,
    }

    return make_response(response_dict,200)

# this creates a post
@api.post('/posts')
def post_post():
    user=g.current_user
    posted_data=request.get_json()
    if not user:
        return make_response(f"User id: {posted_data['user_id']} does not exist",404)
    if user.id != posted_data['user_id']:
        return make_response("Posted user and logged in user must be the same", 403)

    post=Post(**posted_data)
    post.save()
    return make_response(f"Post id:{post.id} Created",200)



# this will replace a post with a new version of the post
@api.put('/posts')
def put_post():
    user=g.current_user
    posted_data=request.get_json()
    if not user:
        return make_response(f"User id: {posted_data['user_id']} does not exist",404)
    if user.id != posted_data['user_id']:
        return make_response("User can only edit their own posts", 403)

    post = Post.query.get(posted_data['id'])
    if not post:
        return make_response(f"Post id: {posted_data['id']} does not exist",404)
    post.user_id = posted_data['user_id']
    post.body = posted_data['body']
    post.save()
    return make_response(f"Post id: {post.id} has been updated",200)


# this will update a post with new information
@api.patch('/posts')
def patch_post():
    # get the token from the header
    user=g.current_user
    posted_data=request.get_json()
    if not user:
        return make_response(f"User id: {posted_data['user_id']} does not exist",404)
    if user.id != posted_data['user_id']:
        return make_response("User can only edit their own posts", 403)
    post = Post.query.get(posted_data['id'])
    if not post:
        return make_response(f"Post id: {posted_data['id']} does not exist",404)
    u = User.query.get(posted_data.get('user_id'))
    if not u:
        return make_response(f"User id: {posted_data['user_id']} does not exist",404)
    post.user_id = posted_data['user_id'] if posted_data.get('user_id') and posted_data['user_id'] !=post.user_id else post.user_id
    post.body = posted_data['body'] if posted_data.get('body') and posted_data['body'] !=post.body else post.body
    post.save()
    return make_response(f"Post id: {post.id} has been changed",200)


# this will delete a post
@api.delete('/posts')
def get_post():
    posted_data=request.get_json()
    post = Post.query.get(posted_data['id'])
    # get the token from the header
    user=g.current_user
    if not user:
        return make_response(f"User id: {posted_data['user_id']} does not exist",404)
    if user.id != post.user_id:
        return make_response("User can only Delete their own posts", 403)
    if not post:
        return make_response(f"Post id: {posted_data['id']} does not exist",404)
    p_id=post.id
    post.delete()
    return make_response(f"Post id: {p_id} has been deleted",200)

