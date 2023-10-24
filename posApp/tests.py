from django.test import TestCase
from .models import *

# Create your tests here.
def test(request):
    categories = Category.objects.all()
    