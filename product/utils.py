from django.http import JsonResponse

def error_400(request, message):
    response = JsonResponse(data={'message': message})
    response.status_code = 400
    return response