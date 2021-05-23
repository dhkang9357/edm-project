from django.shortcuts import HttpResponse

def response(file, type='text/javascript'):
    with open(file, 'rb') as f:
        return HttpResponse(f.read(), content_type=type)

def script(request):
    return response('app/script/script.js')

def dropdown(request):
    return response('app/script/semantic_ui/dist/components/dropdown.js')

def semantic_css(request):
    return response('app/script/semantic_ui/dist/semantic.css', type='text/css')

def semantic_js(request):
    return response('app/script/semantic_ui/dist/semantic.js')