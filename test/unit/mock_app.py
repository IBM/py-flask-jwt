from flask import Flask
from flask_restful import Api, Resource
from lib.wds_auth.decorators import public, private


class MockApp:

    RESPONSE = {'message': 'success'}

    PUBLIC_API = '/public'

    PRIVATE_API = '/private'

    def run(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(MockApp.PrivateApi, self.PRIVATE_API)
        api.add_resource(MockApp.PublicApi, self.PUBLIC_API)
        return app

    class PrivateApi(Resource):

        @private
        def get(self):
            return MockApp.RESPONSE
    
    class PublicApi(Resource):

        @public
        def get(self):
            return MockApp.RESPONSE
