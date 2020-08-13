#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from blacklist import BLACKLIST
from flask import jsonify
from flask_jwt_extended import JWTManager
from app import app

import views
jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'msg': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'msg': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'msg': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'msg': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'msg': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


