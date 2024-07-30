from django.http import JsonResponse

# Create your views here.
def ping(req) -> JsonResponse:
    return JsonResponse({"STATUS": "GOOD"})


# start and attempt challenge
def start_and_attempt(req) -> JsonResponse:
    pass