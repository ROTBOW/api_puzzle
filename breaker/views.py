from datetime import datetime, timedelta
from django.utils import timezone

from django.http import JsonResponse

from .models import Attempt, Completion
from .utils.db_utils import expiration_check, clean_expired
from .utils.problem_generator import gen_problem
from .utils.utils import time_till_expires


# Create your views here.
def ping(req) -> JsonResponse:
    amount_del = clean_expired()
    return JsonResponse({"INFO": f"Cleased db, amount removed: {amount_del}"})


# start challenge
def start(req, email) -> JsonResponse:
    # check if the email already exist in the db, if so they have already started
    # their challenge
    
    if expiration_check(email):
        # true means we create a new attempt
        apt = Attempt()
        apt.email = email
        apt.gate = 1
        apt.expires = timezone.now() + timedelta(hours=1)
        
        # use this gate (the starting one) to gen a problem
        hint, problem, hashed_ans = gen_problem(apt.gate)
        apt.curr_ans = hashed_ans
        apt.save()
        
        return JsonResponse({
            'curr_gate': apt.gate,
            'hint': hint,
            'problem_str': problem,
            'expires': time_till_expires(apt.expires)
        })
    else:
        # false means attempt in progress
        apt = Attempt.objects.get(email__exact=email)
        return JsonResponse({
            'expires': time_till_expires(apt.expires),
            'info': 'your hint, and q string are gen at your init request, and are not saved in our db, if you need to restart, call gate1/email/restart to start a new trial'
        })
    
# called to restart a challenge
def restart(req, email) -> JsonResponse:
    try:
        apt = Attempt.objects.get(email__exact=email)
        apt.delete()
        return JsonResponse({"Info": "attempt was successfully deleted, you can call gate1/<email> to try again"})
    except:
        return JsonResponse({"Error": "No attempt found with that email"})

# _and_attempt challenge
def attempt(req, email, ans) -> JsonResponse:
    try:
        pass
    except:
        pass
    
    return JsonResponse({'params': [email, ans]})