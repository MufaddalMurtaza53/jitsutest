import jwt
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

# Put your JAAS credentials here or better in environment variables for production
APP_ID = 'your_app_id_here'
APP_SECRET = 'your_app_secret_here'

@api_view(['POST'])
def generate_token(request):
    meeting_name = request.data.get('meetingName')
    user_name = request.data.get('userName')

    if not meeting_name or not user_name:
        return Response({'error': 'meetingName and userName are required'}, status=status.HTTP_400_BAD_REQUEST)

    payload = {
        'context': {
            'user': {
                'name': user_name
            }
        },
        'aud': 'jitsi',
        'iss': APP_ID,
        'sub': '8x8.vc',
        'room': meeting_name,
        'exp': int(time.time()) + 3600  # expires in 1 hour
    }

    try:
        token = jwt.encode(payload, APP_SECRET, algorithm='HS256')
        return Response({'token': token})
    except Exception as e:
        return Response({'error': 'Failed to generate token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
