from django.shortcuts import render
from .models import Song
from .serializers import SongSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
# Create your views here.


class SongList(APIView):

    def get(self, request):
        try:
            song = Song.objects.all()
            serializer = SongSerializer(song, many=True)
            return Response(serializer.data)
        except Song.DoesNotExist:
            raise Http404

    def post(self, request):
        try:
            serializer = SongSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Song.DoesNotExist:
            raise Http404


class SongDetail(APIView):

    def get_object(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            song = self.get_object(pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        try:
            song = self.get_object(pk)
            serializer = SongSerializer(song, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Song.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        try:
            song = self.get_object(pk)
            song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Song.DoesNotExist:
            raise Http404


class SongLikes(APIView):

    def get_object(self, pk, title):
        try:
            return Song.objects.get(pk=pk, title=title)
        except Song.DoesNotExist:
            raise Http404

    def get(self, request, pk, title):
        try:
            song = self.get_object(pk, title=title)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist:
            raise Http404

    def patch(self, request, pk, title):
        try:
            song = self.get_object(pk, title=title)
            data = {"likes": song.likes + int(1)}
            serializer = SongSerializer(song, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Song.DoesNotExist:
            raise Http404
