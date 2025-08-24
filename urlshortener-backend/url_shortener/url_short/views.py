from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from .models import Link
from .serializers import LinkSerializers

# Create your views here.

@api_view(['POST'])
def shorten(request):
    url = request.data.get('url')
    days = request.data.get('days')
    if not url:
        return Response({"error": "URL is required"}, status=400)
    link = Link(url=url)
    if days:
        link.expires = timezone.now() + timezone.timedelta(days=int(days))
    link.save()
    return Response({"short_url": f"http://127.0.0.1:8000/{link.code}", "code": link.code})

@api_view(['GET'])
def link_info(request, code):
    link = get_object_or_404(Link, code=code)
    serializer = LinkSerializers(link)
    return Response(serializer.data)

def redirect_link(request, code):
    link = get_object_or_404(Link, code=code)
    if link.is_expired():
        return Response({"error": "Link expired"}, status=410)
    link.clicks += 1
    link.save()
    return redirect(link.url)