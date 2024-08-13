from datetime import datetime, timedelta
from django.utils import timezone

from django.http import JsonResponse

from .models import Attempt, Completion
from .utils.db_utils import expiration_check, clean_expired
from .utils.problem_generator import gen_problem
from .utils.utils import time_till_expires, create_hash


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
        apt = Attempt.objects.get(email__exact=email)
        # need to also account for the attempt being expired
        
        if create_hash(ans) == apt.curr_ans:
            apt.gate += 1
            apt.expires = timezone.now() + timedelta(hours=1)
            
            # check if challenge is done (reached the last gate)
            # send them a congrats and mark their time on the leaderboard
            # will prob do this with a helper func
            if apt.gate >= 3:
                
                return JsonResponse({})
            
            else:
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
            # need to delete the apt when they submit a wrong ans
            return JsonResponse({"Info": "incorrect ans, terminating attempt"})
        
    except:
        return JsonResponse({"Info": "There is no attempt with that email, start a new attempt by calling gate/<email>"})