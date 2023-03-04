
import hashlib

from flask import jsonify


TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VyTmFtZSI6ImFkbWluIiwiZXhwIjoxNjU5NjM1NTgwLCJpYXQiOjE2NTk2MzE5ODAsInN1YiI6InVzZXIgdG9rZW4ifQ.I-MAcc_fHkyTr6dzIZu8Sq0u3kILKIpH9VFQOnXjL_4'

TOKENS = {}

def EncryptPassword(password):
    encode_password = password.encode()
    return hashlib.md5(encode_password).hexdigest()


def make_response(code, result, message):
    if message:
        message = repr(message)
    return jsonify({'code': code, 'result': result, 'message': message})


def make_success(result):
    return make_response(200, result, '')


def make_failure(err):
    return make_response(400, '', err)


def to_user_dict(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'description': user.description,
    }


def to_report_dict(report):
    return {
        'id': report.id,
        'name': report.name,
        'status': report.status,
        'progress': report.progress,
        'create_at': report.create_at,
        'owner': report.owner,
    }
