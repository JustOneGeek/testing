from . import bp as api
from app.blueprints.social.models import Post
from app.blueprints.auth.models import User

from flask import request, make_response

# this is so another application can talk to our social media service

# this will return all posts in our database
@api.get('/all_posts')
def get_all_posts():
    posts=Post.query.all()
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
def get_post_api():
    data_from_request=request.get_json()
    post = Post.query.get(data_from_request['id'])
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
    posted_data=request.get_json()
    u = User.query.get(posted_data['user_id'])
    if not u:
        return make_response(f"User id: {posted_data['user_id']} does not exist",404)
    post=Post(**posted_data)
    post.save()
    return make_response(f"Post id:{post.id} Created",200)



# this will replace a post with a new version of the post
@api.put('/posts')
def put_post():
    posted_data=request.get_json()
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
    posted_data=request.get_json()
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
def delete_post():
    posted_data=request.get_json()
    post = Post.query.get(posted_data['id'])
    if not post:
        return make_response(f"Post id: {posted_data['id']} does not exist",404)
    p_id=post.id
    post.delete()
    return make_response(f"Post id: {p_id} has been deleted",200)

