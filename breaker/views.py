from datetime import datetime, timedelta
from django.utils import timezone

from django.http import JsonResponse

from .models import Attempt, Completion
from .utils.db_checks import expiration_check
from .utils.problem_generator import gen_problem
from .utils.utils import time_till_expires


# Create your views here.
def ping(req) -> JsonResponse:
    now = datetime.now()
    return JsonResponse({"INFO": f"STATUS REQUEST RECIVED AT {now}"})


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
            'curr_gate': 1,
            'hint': hint,
            'problem_str': problem,
            'expires': time_till_expires(apt.expires)
        })
    else:
        # false means attempt in progress
        return JsonResponse({'INFO': 'you already have an attempt in progress, complete it or let it expire'})
    
    
    

# _and_attempt challenge
def attempt(req, email, ans) -> JsonResponse:
    return JsonResponse({'params': [email, ans]})