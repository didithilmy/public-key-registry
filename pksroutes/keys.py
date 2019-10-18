import router
import json
from router import Response

from Crypto.PublicKey import RSA
from base64 import b64decode

import keystore
import utils

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
        pemEncoded = "-----BEGIN RSA PUBLIC KEY-----\n" + utils.insert_newlines(publicKey.decode("utf-8"), 64) + "\n-----END RSA PUBLIC KEY-----"
        return Response(responseBody = pemEncoded)
