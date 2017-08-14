from django.contrib.auth.models import User, Permission, Group
from urllib.parse import parse_qsl
import json

def parse_request(request):
    return {i[0]:i[1] for i in parse_qsl(request.body)}

def is_member(d, group):
    user = d.get(b"username")
    if not user:
        return False
    user = user.decode('utf8')
    try:
        user = User.objects.get(username=user)
    except:
        return False
    return user.groups.filter(name=group).exists()

def allowed_scope(request):
    d = parse_request(request)
    if d.get(b'grant_type')== b'refresh_token':
        return True, True, None, None
    elif d.get(b'scope') == b'read' and not is_member(d, 'reader'):
        return False, True, json.dumps({"error": "scope not allowed for this user"}), 401
    elif d.get(b'scope') == b'write' and not is_member(d, 'writer'):
        return False, True, json.dumps({"error": "scope not allowed for this user"}), 401
    elif d.get(b'scope') == None:
        return False, True, json.dumps({"error": "scope of token must be defined"}), 401
    else:
        return True, False, None, None


