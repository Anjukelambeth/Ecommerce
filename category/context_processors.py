from .models import category

def nav_links(request):
    links=category.objects.all()
    return dict(links=links)