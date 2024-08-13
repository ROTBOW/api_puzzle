from django.utils import timezone
from ..models import Attempt


def expiration_check(email: str) -> bool:
    # if it doesn't exist or has been deleted due to being expired this will return True
    # if the attempt is still vaild then it will return False
    if Attempt.objects.filter(email__exact=email).exists():
        
        # get the apt
        apt = Attempt.objects.get(email__exact=email)
        # check if the apt is expired, deleting it if so
        if apt.expires < timezone.now():
            apt.delete()
            return True
        # attempt isn't expired, return False
        return False
    
    else:
        # There is no attempt under that email, return True
        return True
    
def clean_expired() -> int:
    """
        checks the db for expired attempts and deletes them
    """
    
    apts = Attempt.objects.filter(expires__lte=timezone.now())
    n = len(apts)
    apts.delete()
    
    
    return n