from django.shortcuts import HttpResponse

def response(file, type='text/javascript'):
    with open(file, 'rb') as f:
        return HttpResponse(f.read(), content_type=type)

def script(request):
    return response('app/script/script.js')