from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, 'admin/404-page/error-page.html', status=404)   

def custom_500(request):
    return render(request, 'admin/404-page/error-page.html', status=500)




