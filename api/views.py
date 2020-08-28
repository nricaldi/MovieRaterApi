from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, ) # DO NOT USE IsAuthenticated ****** it will save you a headache
    # blocks access to movies unless logged in with valid token
    # AllowAny gives access to non users

    permission_classes = (IsAuthenticated, )

    # the @action decorating our def with extra values
    # detail=True means it will need a specific movie
    # and it will not work on the movies/
    # detail=False means on the list of the movies
    # pk = primary key
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            stars = request.data['stars']
            user = request.user
            movie = Movie.objects.get(id=pk)
            
            # Use try bc it might fail and it might break the method
            # one method for both update and create
            try: 
                # Foreign keys are stored as id numbers not objects
                # Gets existing rating and updates the star rating
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                # use serializer from serializers.py return a json of updated rating
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            except: 
                # If rating does not exist it will create a new rating
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)

                # use serializer from serializers.py return a json of created rating
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
                 
        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    # blocks access to movies unless logged in with valid token
    permission_classes = (IsAuthenticated, )

    # Overriding default django create method 
    def create(self, request, *args, **kwargs):
        response = {'message': "You can't create rating like that"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
    # Overriding default django update method 
    def update(self, request, *args, **kwargs):
        response = {'message': "You can't update rating like that"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)