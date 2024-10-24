import pytest
from app import app
import jwt
from datetime import datetime, timezone

@pytest.fixture
def client():
    with app.test_client() as test:
        yield test

# Test to ensure that /auth returns a valid JWT
def test_Valid_JWT_authentication(client):
    response = client.post('/auth')
    assert response.status_code == 200
    token = response.get_json().get('token')
    assert token is not None

    # Decode the token without verifying expiration
    decoded = jwt.decode(token, '3ba010226cd84939b9eed91aa6bd9519', algorithms=['HS256'], options={"verify_exp": False})
    assert decoded['Fullname'] == "username"

# Test to ensure that /auth returns an expired JWT when expired=true
def test_Expired_JWT_authentication(client):
    response = client.post('/auth?expired=true')
    assert response.status_code == 200
    token = response.get_json().get('token')
    assert token is not None

    # Decode the token without verifying expiration
    decoded = jwt.decode(token, '3ba010226cd84939b9eed91aa6bd9519', algorithms=['HS256'], options={"verify_exp": False})
    
    # Ensure that the token is expired
    assert decoded['exp'] < datetime.now(timezone.utc).timestamp()

# Test to ensure that the valid JWT's kid is found in JWKS
def test_Valid_JWK_Found_In_JWKS(client):
    response = client.post('/auth')
    token = response.get_json().get('token')
    header = jwt.get_unverified_header(token)
    
    jwks_keys = client.get('/.well-known/jwks.json').get_json()['keys']
    
    # Check if the 'kid' in the JWT header is found in the JWKS keys
    assert header.get('kid') in [key['kid'] for key in jwks_keys]

# Test to ensure that expired JWT's kid is not found in JWKS
def test_Expired_JWK_Not_Found_In_JWKS(client):
    response = client.post('/auth?expired=true')
    token = response.get_json().get('token')
    header = jwt.get_unverified_header(token)
    
    jwks_keys = client.get('/.well-known/jwks.json').get_json()['keys']
    
    # Ensure that the 'kid' in the expired JWT header is NOT in the JWKS keys
    assert header.get('kid') not in [key['kid'] for key in jwks_keys]

# Test to ensure that the JWT exp claim is in the past for expired tokens
def test_Expired_JWK_is_expired(client):
    response = client.post('/auth?expired=true')
    token = response.get_json().get('token')
    
    # Decode the token without verifying expiration
    decoded = jwt.decode(token, '3ba010226cd84939b9eed91aa6bd9519', algorithms=['HS256'], options={"verify_exp": False})
    
    # Ensure the token is expired
    assert decoded['exp'] < datetime.now(timezone.utc).timestamp()