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

def updateKey(keyId, b64key):
    if (r.get(keyId) == None):
        return False

    r.set(keyId, b64key)
    return True

def deleteKey(keyId):
    r.delete(keyId)

