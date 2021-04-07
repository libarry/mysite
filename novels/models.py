from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    # Picture
    cover = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
                       through='Comment', related_name='comments_owned')

    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       through='Fav', related_name='favorite_ads')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Shows up in the admin list

    def __str__(self):
        return self.title


class Fav(models.Model) :
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('book', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.book.title[:10])


class Chapter(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField(
        validators=[MinLengthValidator(50, "content must be greater than 50 characters")]
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15: return self.text
        return self.text[:11] + ' ...'


class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15: return self.text
        return self.text[:11] + ' ...'