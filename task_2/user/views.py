from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class User(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "name": "Monil",
            "email": "monilsojitra903@gmail.com",
            "phone_no": "98797-52696",
            "HINT": "Your rate limit is limited"
        }
        return Response(data=data, status=status.HTTP_200_OK)