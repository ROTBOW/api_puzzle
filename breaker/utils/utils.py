from django.utils import timezone
from hashlib import sha256

def time_till_expires(expires) -> str:
    now = timezone.now()
    
    if expires < now:
        return '00:00:00'
    
    delta = expires - now
    
    return str(delta)


def create_hash(string: str) -> str:
    hashed_str = sha256(string.encode('utf-8'))
    
    return hashed_str.hexdigest()