from django.shortcuts import render

def api_documentation(request):
    context = {
        'scalar_config': {
            'url': '/schema/',
            'proxyUrl': '',
            'showDeveloperTools': "never",
            'hideClientButton': True
        }
    }

    return render(request, 'scalar.html', context)