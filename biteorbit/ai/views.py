from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class DeliveryAIAPIView(APIView):

    def post(self, request):

        message = request.data.get("message")

        message = message.lower()

        # =========================================
        # AI RESPONSES
        # =========================================

        if "late" in message:

            reply = """
            Rider is delayed due to traffic 🚦
            Estimated arrival:
            10 minutes.
            """

        elif "where" in message:

            reply = """
            Rider is near your location 📍
            Please keep phone available.
            """

        elif "cancel" in message:

            reply = """
            Order cancellation is available
            before preparation starts.
            """

        elif "hello" in message:

            reply = """
            Hello 👋
            Welcome to BiteOrbit AI Assistant.
            """

        elif "help" in message:

            reply = """
            I can help with:
            • Delivery Status
            • ETA
            • Rider Support
            • Order Issues
            """

        else:

            reply = """
            BiteOrbit AI is analyzing your request 🤖
            """

        return Response({

            "success": True,

            "reply": reply
        })