from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import handle_deposit_webhook


class DepositWebhookView(APIView):

    def post(self, request):

        handle_deposit_webhook(request.data)

        return Response(status=200)

# Create your views here.
