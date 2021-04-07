from django.urls import path, reverse_lazy
from . import views

app_name='novels'

urlpatterns = [
    path('', views.BookListView.as_view(), name='all'),

    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/create',
        views.BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/update',
         views.BookUpdateView.as_view(success_url=reverse_lazy('novels:all')), name='book_update'),
    path('book/<int:pk>/delete',
        views.BookDeleteView.as_view(success_url=reverse_lazy('novels:all')), name='book_delete'),

    path('chapter/<int:ck>', views.ChapterDetailView.as_view(), name='chapter_detail'),
    path('book/<int:pk>/write', views.ChapterCreateView.as_view(), name='chapter_create'),
    path('chapter/<int:ck>/update',views.ChapterUpdateView.as_view(), name='chapter_update'),
    path('chapter/<int:ck>/delete',views.ChapterDeleteView.as_view(), name='chapter_delete'),


    path('book_cover/<int:pk>', views.stream_file, name='book_cover'),

    path('book/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='book_comment_create'),

    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('novels')), name='book_comment_delete'),

    path('book/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='book_favorite'),
    path('book/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='book_unfavorite'),

    ]