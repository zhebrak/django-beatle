from functools import wraps
import hmac

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from beatle.conf import settings


def get_signature(params):
    msg = ''.join(map(str, sorted(params.values()))).encode()
    print msg
    return hmac.new(settings.SECRET_KEY.encode(), msg=msg).hexdigest()


def validate_signature(view):

    @wraps(view)
    def wrapped(request, *args, **kwargs):
        params = request.GET.dict()
        try:
            signature = params.pop('SIGNATURE')
        except KeyError:
            return HttpResponseBadRequest()

        if signature != get_signature(params):
            return HttpResponseBadRequest()

        return view(request, *args, **kwargs)

    return wrapped


@validate_signature
@csrf_exempt
def endpoint(request):
    if request.method == 'GET':
        configuration = settings.get_configuration()
        return JsonResponse(configuration)

    print 'Making calls', request.GET.get('TASKS')

    return JsonResponse({'response': 'OK'})
