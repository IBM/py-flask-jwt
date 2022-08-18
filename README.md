:warning: This project is under development and is incomplete.

# IBM Flask JWT
This project provides a simple Python library for securing Flask APIs with JWT authentication.

[![Build](https://github.com/IBM/py-flask-jwt/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/IBM/py-flask-jwt/actions/workflows/build.yaml)

## JSON Web Tokens
Secure endpoints are accessed by passing a [JSON Web Token](https://jwt.io/introduction) (JWT).

## API Decorators
The follow Python decorators are available for use on Flask API endpoints.
* `private` - Secures an API endpoint. Requests to the endpoint will return a `401 Unauthorized` response unless a valid JWT is attached to the HTTP request. The JWT must be sent as a bearer token in the standard authorization header: `Authorization: Bearer <token>`.
* `public` - This is a marker decorator to identify an endpoint as intentionally public.

### Example
The following example shows how to secure a private endpoint for a simple API built with the [Flask RESTful](https://flask-restful.readthedocs.io/en/latest/) framework. In this example, requests to the resource will return a `401 Unauthorized` response unless a valid JWT token is attached to the HTTP request.
```
from flask_restful import Resource
from ibm_flask_jwt.decorators import private


class PrivateApi(Resource):

    @private
    def get(self):
        return 'Success'
```

## Configuration
The following environment variables are loaded by the library:
* `JWT_PUBLIC_KEY` - (Required) RSA256 public key for JWT signature verification.

## Development

### Dependencies
Use [Pipenv](https://pipenv.pypa.io/en/latest/) for managing dependencies. Install all dependencies with `pipenv install --dev`.

### Testing
Run the unit tests with code coverage with `pipenv run pytest --cov lib test`.

### Building
Run the `build.py` file to generate the `setup.py` file. This allows us to read the required dependencies from `Pipfile.lock` so they are available in the `install_requires` configuration field of `setup.py`.
