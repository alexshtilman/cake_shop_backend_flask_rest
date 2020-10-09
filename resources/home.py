import os

from flask_restful import Resource
from flask import render_template, make_response, redirect, url_for


class Home(Resource):

    def get(self):
        #return redirect('/apidocs')
        headers = {'Content-Type': 'text/html'}
        mode = os.environ.get('FLASK_ENV')
        return make_response(render_template('index.html', callback_access_token='',
                                             callback_refresh_token=''), 200, headers)