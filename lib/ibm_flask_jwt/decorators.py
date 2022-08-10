import logging
from functools import wraps, partial
from flask import request, abort
import jwt
from jwt.exceptions import PyJWTError
from .auth_props import AuthProps


LOGGER = logging.getLogger(__name__)

AUTH_HEADER = 'Authorization'

AUTH_SCHEME = 'bearer'

JWT_ALG_RS256 = 'RS256'

TOKEN_TYPE_KEY = 'type'

ACCESS_TOKEN_TYPE = 'access_token'


_props = AuthProps()


def public(api_func=None):
    '''
    Marker decorator for public API endpoints.
    '''
    decorated = api_func
    if not api_func:
        decorated = partial(public)
    @wraps(decorated)
    def decorator(self, *args, **kwargs):
        LOGGER.debug('This API endpoint is public and does not require authentication')
        return decorated(self, *args, **kwargs)
    return decorator


def private(api_func=None):
    '''
    Decorator for private API endpoints. A valid JWT bearer token must be attached
    to the HTTP request in the Authorization header.
    '''
    decorated = api_func
    if not api_func:
        decorated = partial(private)
    @wraps(decorated)
    def decorator(self, *args, **kwargs):
        LOGGER.debug('This API endpoint is private and requires authentication')
        if AUTH_HEADER in request.headers:
            header = request.headers[AUTH_HEADER]
            _validate_header_format(header)
            _authenticate_token(header, _props)
        else:
            LOGGER.error('Request is missing authentication header')
            abort(401)
        return decorated(self, *args, **kwargs)
    return decorator


def _validate_header_format(header):
    parts = header.split()
    if len(parts) != 2:
        LOGGER.error('Malformed authentication header')
        abort(401)
    if parts[0].strip().lower() != AUTH_SCHEME:
        LOGGER.error(f'Invalid authentication scheme: not a {AUTH_SCHEME} token')
        abort(401)


def _authenticate_token(header, props):
    token = header.split()[1].strip()
    try:
        decoded = jwt.decode(token, props.jwt_public_key(), algorithms=JWT_ALG_RS256)
        if (not TOKEN_TYPE_KEY in decoded) or (decoded[TOKEN_TYPE_KEY] != ACCESS_TOKEN_TYPE):
            LOGGER.error('Supplied authorization token is not an access token')
            abort(401)
    except PyJWTError:
        LOGGER.exception('Failed to authenticate JWT')
        abort(401)
