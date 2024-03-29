import router
import json
from router import Response

from Crypto.PublicKey import RSA
from base64 import b64decode

import keystore
import utils
from jwcrypto.jwk import JWK, JWKSet

@router.post("/v1/keys/{keyId}")
def post_createPublicKey(request):
    reqBody = json.loads(request.body)
    publicKey = reqBody['publicKey']
    keyId = request.args['keyId']

    if len(keyId) <= 4:
        return Response(responseBody=json.dumps({'error': 'Key ID too short'}),
                        contentType="application/json", statusCode=400)
    try:
        keyDER = b64decode(publicKey)
        RSA.importKey(keyDER)

        if (keystore.addKey(keyId, publicKey)):
            return Response(responseBody=json.dumps({'keyId': keyId, 'publicKey': publicKey}),
                            contentType="application/json")
        else:
            return Response(responseBody=json.dumps({'error': 'Key with the same ID exists'}),
                            contentType="application/json", statusCode=400)
    except:
        return Response(responseBody=json.dumps({'error': 'Invalid key format'}), contentType="application/json", statusCode = 400)

@router.put("/v1/keys/{keyId}")
def put_updatePublicKey(request):
    reqBody = json.loads(request.body)
    publicKey = reqBody['publicKey']
    keyId = request.args['keyId']

    if len(keyId) <= 4:
        return Response(responseBody=json.dumps({'error': 'Key ID too short'}),
                        contentType="application/json", statusCode=400)
    try:
        keyDER = b64decode(publicKey)
        RSA.importKey(keyDER)

        if (keystore.updateKey(keyId, publicKey)):
            return Response(responseBody=json.dumps({'keyId': keyId, 'publicKey': publicKey}),
                            contentType="application/json")
        else:
            return Response(responseBody=json.dumps({'error': 'Key not found'}),
                            contentType="application/json", statusCode=404)
    except:
        return Response(responseBody=json.dumps({'error': 'Invalid key format'}), contentType="application/json", statusCode = 400)

@router.delete("/v1/keys/{keyId}")
def delete_deletePublicKey(request):
    keyId = request.args['keyId']
    if not keystore.deleteKey(keyId):
        return Response(responseBody=json.dumps({'error': 'Key not found'}),
                        contentType="application/json", statusCode=404)
    else:
        return Response(responseBody=json.dumps({'success': True}), contentType="application/json")

@router.get("/v1/keys/jwks")
def get_getPublicKeysJwks(request):
    keys = keystore.getAllKeys()

    jwks = []
    for keyId in keys.keys():
        pemEncoded = "-----BEGIN PUBLIC KEY-----\r\n" + utils.insert_newlines(keys[keyId].decode("ascii"), 64) + "\r\n-----END PUBLIC KEY-----"
        jwk = JWK.from_pem(pemEncoded.encode("ascii"))
        jwkDecoded = json.loads(jwk.export_public())
        jwkDecoded['kid'] = keyId
        jwkDecoded['kty'] = "RSA"
        jwkDecoded['use'] = "sig"
        jwks.append(jwkDecoded)

    return Response(responseBody = json.dumps({'keys': jwks}, indent = 4), contentType = "application/json")

@router.get("/v1/keys/{keyId}")
def get_getPublicKey(request):
    keyId = request.args['keyId']
    publicKey = keystore.getKey(keyId)

    if publicKey == None:
        return Response(responseBody=json.dumps({'error': 'Key not found'}),
                        contentType="application/json", statusCode=404)
    else:
        return Response(responseBody = publicKey.decode("utf-8"))


@router.get("/v1/keys/{keyId}/pem")
def get_getPublicKeyPem(request):
    keyId = request.args['keyId']
    publicKey = keystore.getKey(keyId)

    if publicKey == None:
        return Response(responseBody=json.dumps({'error': 'Key not found'}),
                        contentType="application/json", statusCode=404)
    else:
        pemEncoded = "-----BEGIN PUBLIC KEY-----\n" + utils.insert_newlines(publicKey.decode("ascii"), 64) + "\n-----END PUBLIC KEY-----"
        return Response(responseBody = pemEncoded)

@router.get("/v1/keys/{keyId}/jwk")
def get_getPublicKeyJwk(request):
    keyId = request.args['keyId']
    publicKey = keystore.getKey(keyId)

    if publicKey == None:
        return Response(responseBody=json.dumps({'error': 'Key not found'}),
                        contentType="application/json", statusCode=404)
    else:
        pemEncoded = "-----BEGIN PUBLIC KEY-----\r\n" + utils.insert_newlines(publicKey.decode("ascii"), 64) + "\r\n-----END PUBLIC KEY-----"
        jwk = JWK.from_pem(pemEncoded.encode("ascii"))
        jwkDecoded = json.loads(jwk.export_public())
        jwkDecoded['kid'] = keyId
        jwkDecoded['kty'] = "RSA"
        return Response(responseBody = json.dumps(jwkDecoded, indent=4), contentType = "application/json")

