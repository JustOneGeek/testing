from . import bp as api
from app.blueprints.auth.models import User
from app.blueprints.auth.auth import token_auth, basic_auth
from flask import request, make_response, g
# Make a user an Admin ... But we will need to start with an admin user

# UPDATE public.user
# SET is_admin = TRUE
# WHERE id = 1

@api.patch('/make_admin')
@token_auth.login_required()
def make_admin():
    user_id_to_be_admin=request.get_json().get('id')
    if not user_id_to_be_admin:
        return make_response("Invalid Request payload",400)
    if not g.current_user.is_admin:
        return make_response("This action requires Admin privs",403)
    user=User.query.get(user_id_to_be_admin)
    user.is_admin=True
    user.save()
    return make_response(f"{user.first_name} {user.last_name} is now an Admin",200)

# All the API user to pass login creds for user and retrieve a token for that user
@api.get('/token')
@basic_auth.login_required()
def get_token():
    # auth_header=request.headers.get('Authorization')
    # username, password=get_basic_auth_creds(auth_header)
    # user=User.query.filter_by(email=username).first()
    # user_email = basic_auth.current_user()
    # user = User.query.filter_by(email=user_email).first()
    user= g.current_user
    token=user.get_token()
    return make_response({"token":token},200)
