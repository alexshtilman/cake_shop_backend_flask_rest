from flask_restful import Resource, reqparse
from flask import Flask, redirect, request, url_for
import json
import requests
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity,
                                jwt_refresh_token_required,
                                get_raw_jwt)
from oauthlib.oauth2 import WebApplicationClient
from app import app

from models.user import UserModel
from flask import render_template, make_response

# OAuth 2 client setup
client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])


class GoogleLogin(Resource):

    def get(self):
        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)


class GoogleLoginCallback(Resource):

    def get(self):
        # Get authorization code Google sent back to you
        code = request.args.get("code")

        # Find out what URL to hit to get tokens that allow you to ask for
        # things on behalf of a user
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        # Prepare and send request to get tokens! Yay tokens!
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
        )

        # Parse the tokens!
        client.parse_request_body_response(json.dumps(token_response.json()))

        # Now that we have tokens (yay) let's find and hit URL
        # from Google that gives you user's profile information,
        # including their Google Profile Image and Email
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        # We want to make sure their email is verified.
        # The user authenticated with Google, authorized our
        # app, and now we've verified their email through Google!
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index.html', access_token='', refresh_token=''), 200, headers)

        # Create a user in our db with the information provided
        # by Google

        user = UserModel.find_by_id(unique_id)
        # Doesn't exist? Add to database
        if not UserModel.find_by_id(unique_id):
            user = UserModel(unique_id, generate_password_hash(unique_id).decode('utf-8'), False, users_name,
                             users_email, picture)
            user.save_to_db()

        access_token = create_access_token(identity={'unique_id': user.unique_id,
                                                     'is_admin': user.is_admin,
                                                     'users_name': user.users_name,
                                                     'users_email': user.users_email,
                                                     'profile_pic': user.profile_pic
                                                     }, fresh=True)

        refresh_token = create_refresh_token(user.unique_id)
        print(refresh_token)
        return redirect('/callback?access_token='+access_token+'&refresh_token='+refresh_token)




def get_google_provider_cfg():
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()
