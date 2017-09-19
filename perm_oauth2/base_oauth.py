import oauth2_provider.views.application as application
import oauth2_provider.views.base as base
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Permission, Group
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from . import permissions
import json

@method_decorator(csrf_exempt, name="dispatch")
class CusTokenView(base.TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        correct, token_correct, body, status =  permissions.allowed_scope(request)
        if not correct:
            return  HttpResponseForbidden("not allowed")
        url, headers, body, status = self.create_token_response(request)
        body = parse_body(body, request)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response

def parse_body(body, request):
    """Get rid of refersh token for security"""
    d = permissions.parse_request(request)
    if permissions.is_member(d, 'refresh')\
        or d.get(b'grant_type')== b'refresh_token':
        return body
    try:
        d = json.loads(body)
    except ValueError:
        return body
    else:
        if d.get('refresh_token'):
            del(d['refresh_token'])
        return json.dumps(d)

class ApplicationRegistration(application.ApplicationRegistration):
    """
    subclass ApplicationRegistration to use custom permissions.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


