import json
import os
import datetime
import python_jwt as jwt
import jws
import Crypto.PublicKey.RSA as RSA


JWT_TOKEN_NOT_BEFORE_TIMEDELTA = 10
print '##### Generating token'
private_key_file = os.path.join(os.path.dirname(__file__), 'keypair.priv')
# private_key_file = os.path.join(os.path.dirname(__file__), 'other.priv')
with open(private_key_file, 'r') as fd:
    private_key = RSA.importKey(fd.read())

payload = {'userId': '1234', 'role': 'admin'}
print 'payload =', json.dumps(payload)
token = jwt.generate_jwt(payload, private_key, 'RS256', datetime.timedelta(minutes=5))
print 'token:', token


print '##### Validating token'
public_key_file = os.path.join(os.path.dirname(__file__), 'keypair.pub')
with open(public_key_file, 'r') as fd:
    public_key = RSA.importKey(fd.read())

try:
    header, claims = jwt.verify_jwt(token, public_key, ['RS256'])
except jws.exceptions.SignatureError:
    print 'invalid token signature!'
    raise SystemExit()

print 'token OK'
print 'header:', json.dumps(header)
print 'claims:', json.dumps(claims)

for k in payload:
    assert claims[k] == payload[k]
