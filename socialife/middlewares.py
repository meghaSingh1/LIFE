import json

def check_user_with_token(request):
    user_email = request.user.email
    data = json.loads(request.body.decode('utf-8'))
    request_email = data['email']
    if user_email == request_email:
        return True
    else:
        return False