from django.shortcuts import render
from .models import AIFeedModel
from rest_framework.generics import ListCreateAPIView , GenericAPIView
from  .serializers import AIFeedSerializer , UserSerializer , LoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
import re
import os
from google import genai
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# Create your views here.

API_KEY = "AIzaSyBdNNLAMqq95zJ5sj8bAGyDl1sApcVqrzs"
client = genai.Client(api_key = API_KEY)

def clean_text(text):
    return re.sub(r"[^\w\s]","",text)


class register(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class Login(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes  = [AllowAny]
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username,password=password)
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key},status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)

class AskAI(ListCreateAPIView):
    queryset  = AIFeedModel.objects.all()
    serializer_class = AIFeedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIFeedModel.objects.filter(user=self.request.user).order_by('id')

    def create(self, request,*args,**kwargs):
        question = request.data.get("question")
        user= request.user
        try:
            response = client.models.generate_content(
                model = "gemini-2.0-flash",
                contents = question
            )
            clean_answer = clean_text(response.text)
        except Exception as e:
            clean_answer = f"Something Went Wrong: {e}"
        serializer = self.get_serializer(data={
            "question": question,
            "answer": clean_answer
        })
        serializer.is_valid(raise_exception = True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


