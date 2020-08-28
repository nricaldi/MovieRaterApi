from django.db import models
# # import User model directly from django
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            sum += rating.stars

        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
#     # Only accepted values will be if the user and movie arent already in the db when creating a Rating
#     # Basically a user cannot create a new review for the same movie more than once
    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)
