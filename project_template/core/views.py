from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import *
import json
from datetime import datetime, timedelta
# from django.db.models import Max
import base64
import logging
import requests

logger = logging.getLogger("filehandler")
