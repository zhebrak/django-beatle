from functools import wraps
import hmac
import importlib

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .conf import settings


def get_signature(params):
    msg = ''.join(map(str, sorted(params.values()))).encode()
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

    errors = []
    for task in request.GET.get('TASKS').strip('[]').split(', '):
        try:
            str_module, str_function = task.strip('\'\"').rsplit('.', 1)
            module = importlib.import_module(str_module)
            getattr(module, str_function)()
        except Exception as e:
            errors.append(str(e))

    if errors:
        return JsonResponse({
            'response': 'Error',
            'errors': errors
        })

    return JsonResponse({'response': 'OK'})
