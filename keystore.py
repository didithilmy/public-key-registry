import redis
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0))
)

def addKey(keyId, b64key):
    if (r.get(keyId) != None):
        return False

    r.set(keyId, b64key)
    return True


def getKey(keyId):
    return r.get(keyId)


def getAllKeys():
    keyIds = r.keys()
    keys = dict()
    for keyId in keyIds:
        keyId = keyId.decode('ascii')
        key = r.get(keyId)
        keys[keyId] = key

    return keys


def updateKey(keyId, b64key):
    if (r.get(keyId) == None):
        return False

    r.set(keyId, b64key)
    return True


def deleteKey(keyId):
    if (r.get(keyId) == None):
        return False

    r.delete(keyId)
    return True

