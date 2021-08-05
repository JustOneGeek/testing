from . import bp as api
from app.blueprints.auth.models import User
from .models import Item, Category
from app.blueprints.auth.auth import token_auth
from flask import request, make_response, g




##########
## CATEGORY API CALLS
##########

@api.get('/category')
@token_auth.login_required()
def get_categories():
    cats = Category.query.all()
    cats_dicts=[cat.to_dict() for cat in cats]
    return make_response({"categories":cats_dicts},200)

# create a new category
@api.post('/category')
@token_auth.login_required()
def post_category():
    if not g.current_user.is_admin:
        return make_response(f"You are not an admin",403)    
    cat_name=request.get_json().get('name')
    cat=Category(name=cat_name)
    cat.save()
    return make_response(f"category {cat.id} with name {cat.name} created",200)

# change a category
@api.patch('/category')
@token_auth.login_required()
def patch_category():
    if not g.current_user.is_admin:
        return make_response(f"You are not an admin",403)    
    cat_name=request.get_json().get('name')
    cat_id = request.get_json().get('id')
    if not cat_id or not cat_name:
        return make_response("Invalid Request payload",400)
    cat=Category.query.get(cat_id)
    if not cat:
        return make_response("Invalid category id",400)
    cat.name = cat_name
    cat.save()
    return make_response(f"category {cat.id} has a new name {cat.name}",200)

# Delete a category
@api.delete('/category')
@token_auth.login_required()
def delete_category():
    if not g.current_user.is_admin:
        return make_response(f"You are not an admin",403)    
    cat_id = request.get_json().get('id')
    if not cat_id:
        return make_response("Invalid Request payload",400)
    cat=Category.query.get(cat_id)
    if not cat:
        return make_response("Invalid category id",400)
    cat_id=cat.id
    cat.delete()
    return make_response(f"category {cat_id} has been deleted",200)


##########
## ITEM API CALLS
##########
# Get a list of all the items in our shop
@api.get('/all_items')
@token_auth.login_required()
def get_all_items():
    all_items=Item.query.all()
    items = [item.to_dict() for item in all_items]
    return make_response({"items":items},200)

# Get a list of all items in a category
@api.get('/items_by_category_id')
@token_auth.login_required()
def get_items_by_category():
    id = request.get_json().get('id')
    if not id:
        return make_response("Invalid Request payload",400)
    all_items=Item.query.filter_by(category_id=id).all()
    items = [item.to_dict() for item in all_items]
    return make_response({"items":items},200)

# look up a specific item by its id
@api.get('/item')
@token_auth.login_required()
def get_item():
    id = request.get_json().get('id')
    if not id:
        return make_response("Invalid Request payload",400)
    item=Item.query.filter_by(id=id).first()
    return make_response(item.to_dict(),200)

# create a new item by sending a payload with all the needed info
                                                    # name
                                                    # description
                                                    # price
                                                    # img
                                                    # category_id
@api.post('/item')
@token_auth.login_required()
def post_item():
    if not g.current_user.is_admin:
        return make_response(f"You are not an admin",403)    
    item_dict = request.get_json()
    print(item_dict)
    if 'name'  not in item_dict or 'description'  not in item_dict or 'price'  not in item_dict or 'img'  not in item_dict or 'category_id'  not in item_dict:
        return make_response("Invalid Request payload",400)
    item=Item(**item_dict)
    item.save()
    return make_response(f"Item {item.name} was created with the id {item.id}",201)

# This will Alter an item by looking up item fom an item_id
@api.patch('/item')
@token_auth.login_required()
def patch_item():
    if not g.current_user.is_admin:
        return make_response(f"You are not an admin",403)    
    item_dict = request.get_json()
    if not item_dict.get('id'):
        return make_response("Invalid Request payload",400)
    item = Item.query.get(item_dict['id'])
    item.from_dict(item_dict)
    item.save()
    return make_response(f"Item {item.id} was edited",200)

# This will delete an item by its id
@api.delete('/item')
@token_auth.login_required()
def delete_item():
    if not g.current_user.is_admin:
        return make_response(f"You are not an admin",403)    
    id = request.get_json().get('id')
    if not id:
        return make_response("Invalid Request payload",400)
    item_to_del=Item.query.get(id)
    item_to_del.delete()
    return make_response(f"Item id {id} has been deleted", 201)



