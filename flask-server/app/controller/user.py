# -*- coding: utf-8 -*-
import json
import hashlib

from flask import Blueprint, request

from common.util import EncryptPassword
from common.util import make_response, make_failure,make_success
from common.util import to_user_dict
from common.util import TOKEN, TOKENS
from db.models import User
from db.interface import db

user_route = Blueprint('user', __name__, url_prefix='/user', template_folder='templates', static_folder='static')


@user_route.route('/login', methods=['POST'])
def login():
    try:
        body_args = json.loads(request.data)
        user = User.query.filter_by(name=body_args.get('name')).first()
        if not user:
            return make_response(400, '', 'user {user_name} not exists'.format(user_name=body_args.get('name')))

        # 检查密码是否正确
        if user.password != EncryptPassword(body_args.get('password')):
            return make_response(400, '', 'user {user_name} wrong password'.format(user_name=body_args.get('name')))

        # 存储用户和token
        TOKENS[user.name] = TOKEN

        # 登陆成功，返回临时 token
        return make_response(200, TOKEN, '')
    except Exception as e:
        return make_response(400, '', e)


@user_route.route('/logout', methods=['POST'])
def logout():
    try:
        body_args = json.loads(request.data)
        del TOKENS[body_args.get('name')]
        return make_success('')
    except Exception as e:
        return make_failure(e)


@user_route.route('/register', methods=['POST'])
def register():
    try:
        body_args = json.loads(request.data)

        # 判断两次配置是否一直，可前端做，后端兜底，传入后端时，密码不能为空，前端兜底
        password = body_args.get("password")
        confirm_password = body_args.get("confirm_password")
        if password != confirm_password:
            return make_response(400, '', 'register {user_name} failed: ambiguous password'.format(user_name=body_args.get('name')))

        # 存储加密密码
        encryptPassword = EncryptPassword(password)

        # 创建用户记录
        db.session.add(User(
            name=body_args.get('name'),
            password=encryptPassword,
            email=body_args.get('email', ''),
            description=body_args.get('description', '')))
        db.session.commit()
        return make_response(200, '', '')
    except Exception as e:
        # db.session.rollback() # 回滚
        # db.session.flush() # 重置
        return make_response(400, '', e)


@user_route.route('/password', methods=['POST'])
def change_password():
    try:
        body_args = json.loads(request.data)

        user_id = body_args.get('user_id')
        old_password = body_args.get('old_password')
        password = body_args.get('password')
        confirm_password = body_args.get('confirm_password')

        if password != confirm_password:
            return make_failure('password is different from confirm password')
        user = User.query.filter_by(id=user_id).first()
        if user.password != EncryptPassword(old_password):
            return make_failure('invalid old password')

        User.query.filter_by(id=user_id).update({'password': EncryptPassword(password)})
        db.session.commit()
        return make_success('')
    except Exception as e:
        return make_response(400, '', e)


@user_route.route('/update', methods=['PUT'])
def update():
    try:
        body_args = json.loads(request.data)

        email = body_args.get("email")
        description = body_args.get("description")
        updates = {
            "email": email,
            "description": description,
        }
        User.query.filter_by(id=body_args.get("id")).update(updates)
        db.session.commit()
        return make_response(200, '', '')
    except Exception as e:
        # db.session.rollback() # 回滚
        # db.session.flush() # 重置
        return make_response(400, '', e)


@user_route.route('/detail', methods=['GET'])
def get_user():
    user_id = request.args.get("user_id")
    if not user_id:
        return make_response(400, '', 'invaild empty user id')

    try:
      user = User.query.filter_by(id=user_id).first()
      return make_response(200, to_user_dict(user), '')
    except Exception as e:
        return make_response(400, '', e)


@user_route.route('/delete', methods=['DELETE'])
def delete_user():
    user_id = request.args.get("user_id")
    if not user_id:
        return make_failure('invaild empty user id')
    try:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return make_success('')
    except Exception as e:
        return make_failure(e)


@user_route.route('/list', methods=['GET'])
def get_users():
    try:
        user_name = request.args.get('user_name')

        users = User.query.filter_by(name=user_name).all()
        user_list = []
        for user in users:
            user_list.append(to_user_dict(user))

        return make_response(200, user_list, '')
    except Exception as e:
        return make_response(400, '', e)
