from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator,MinValueValidator
from django.conf import settings
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model) :
    title = models.CharField(
            max_length=255,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    description = models.TextField(validators=[MaxLengthValidator(1000, "Title must be less than 1000 characters")])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    # Picture
    cover = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=255, null=True, help_text='The MIMEType of the file')
    flowers = models.IntegerField(default=0, validators=[MinValueValidator(0,"flower number must be greater than 0!")])
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


class SignIn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(
            max_length=255,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    created_at = models.DateTimeField(auto_now_add=True)


class User_info(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # users get flowers from another user or sign in every day.
    name = models.CharField(max_length=255)
    flowers = models.IntegerField(validators=[MinValueValidator(0, "flower number cannot be less than 0!")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Chapter(models.Model):
    index = models.IntegerField(default=0,validators=[MinValueValidator(1,"chapter number must be greater than 0!")])
    name = models.CharField(max_length=50)
    text = models.TextField(
        validators=[MinLengthValidator(50, "content must be greater than 50 characters")]
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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


class Gifted(models.Model):
    flower = models.IntegerField(validators=[MinValueValidator(1,"flower number must be greater than 0!")])
    giver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Book, on_delete=models.CASCADE)
