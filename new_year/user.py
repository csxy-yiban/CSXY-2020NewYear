from requests import get, post
from pages.application.activity.new_year.db import (
    insert_user, delete_user, get_user_info_by_id
)
from flask import session

"""
请求用户授权获取令牌code
https://openapi.yiban.cn/oauth/authorize?client_id=184035e1b699329d&redirect_uri=http://127.0.0.1:5000/login
获取已授权用户的access_token
https://openapi.yiban.cn/oauth/access_token
主动取消用户的授权
https://openapi.yiban.cn/oauth/revoke_token
"""

client_id = "(0.0)"
redirect_uri = "http://arukione.cn/login"


def get_access_token(code):
    url = 'https://openapi.yiban.cn/oauth/access_token'
    header = {
        'client_id': client_id,
        'client_secret': "2a6cc11e88578b460f39c1b23c6cac20",
        'code': code,
        'redirect_uri': redirect_uri
    }
    response = post(url, header)
    return response


def request_user_info(access_token):
    real_url = 'https://openapi.yiban.cn/user/me'
    header = {'access_token': access_token}
    response_info = get(real_url, header).json()
    if response_info['status'] == "success":
        return {
            "status": "success",
            "info": {
                "yb_id": response_info['info']['yb_userid'],
                "name": response_info['info']['yb_username'],
                "head": response_info['info']['yb_userhead']
            }
        }
    else:
        return response_info


def user_info(access_json):
    if 'access_token' not in access_json:
        return None
    return request_user_info(access_json['access_token'])


def update_user(access_token):
    info = request_user_info(access_token)['info']
    delete_user(info["yb_id"])
    insert_user(info)
    set_session(info, access_token)


def get_user_info_from_database(yb_id):
    user_info = get_user_info_by_id(yb_id)
    return {
        'name': user_info[0],
        'yb_id': str(user_info[1]),
        'head': user_info[2]
    }


def remove_token(access_token):
    url = "https://openapi.yiban.cn/oauth/revoke_token"
    header = {
        "client_id": "184035e1b699329d",
        "access_token": access_token
    }
    return post(url, header).json()["status"]


def set_session(info, access_token):
    session['name'] = info['name']
    session['yb_id'] = info['yb_id']
    session['head'] = info['head']
    session['access_token'] = access_token


def get_session():
    return session


def drop_session():
    session.pop('access_token')
    session.pop('name')
    session.pop('yb_id')
    session.pop('head')


def is_login():
    if 'access_token' not in session:
        return False
    else:
        return session['access_token']
