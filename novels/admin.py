from django.contrib import admin

# Register your models here.
from .models import Tag,Book,Fav,Chapter,Comment,Category
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(Fav)
admin.site.register(Chapter)
admin.site.register(Comment)
admin.site.register(Category)