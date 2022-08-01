import json
from jose import jwt
from urllib.request import urlopen
from flask import request
from functools import wraps

import os
from dotenv import load_dotenv

load_dotenv()
#AUTH0 = os.getenv('AUTH0')
#ALGORITHMS = os.getenv('ALGORITHMS')
#API_AUDIENCE = os.getenv('API_AUDIENCE')

AUTH0_DOMAIN = 'solate.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'castingagency'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    if not auth:
        print('Missing authorization header')
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    authorization_header_parts = auth.split()

    if authorization_header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    if len(authorization_header_parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    
    if len(authorization_header_parts) > 2:
        raise AuthError({
            'code': 'header_malformed',
            'description': 'Authorization token must be a bearer token.'
        }, 401)

    token = authorization_header_parts[1]

    #print('TOKEN IS:', token)
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception as e:
        print(e)
        raise AuthError({
            'code': 'error_with_get_unverified_header',
            'description': "Can't read unverified token header."
        }, 400)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)
    
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms = ALGORITHMS,
                audience = API_AUDIENCE,
                issuer = f'https://{AUTH0_DOMAIN}/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please check the audience and issuer.'
            }, 401)

        except Exception as e:
            print(e)
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def check_permissions(permission, payload):

    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found'
        }, 403)

    return True

'''
def verify_permission(permission=''):
    def get_payload(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                jwt = get_token_auth_header()
            except Exception as e:
                print('JWT Exception in Wrapper', e)
            try:
                payload = verify_decode_jwt(jwt)
            except Exception as e:
                print('PAYLOAD Exception in Wrapper', e)
            try:
                perm = check_permissions(permission, payload)

                if perm == True:
                    return f(payload, *args, **kwargs)
                else:
                    return abort(401)

            except Exception as e:
                print('PERM Exeception in Wrapper', e)
                return abort(401)

        return wrapper
    return get_payload
'''

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            payload = verify_decode_jwt(jwt)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

