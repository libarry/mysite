from novels.models import Book,Comment,Chapter,Tag,Fav
from novels.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from novels.forms import CreateBookForm,CreateChapterForm,CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

def tagJson(request):
    book = Book.objects.get(id=request.POST.get('pk'))
    if(book.tags.filter(name=request.POST.get('tag')).count() == 0
            and request.POST.get('tag') != ''):
        tag, _ = Tag.objects.get_or_create(name=request.POST.get('tag'))
        book.tags.add(tag)
        tag.save();
        book.save();
        return JsonResponse({'tag_exist': False})
    return JsonResponse({'tag_exist': True})


def tagJsonDel(request):
    book = Book.objects.get(id=request.POST.get('pk'))
    tag = Tag.objects.get(name=request.POST.get('tag'))
    book.tags.remove(tag)
    if(tag.book_set.count()==0):
        tag.delete()
    return JsonResponse({None:None})


def tag_list(request,tag_name):
    print(tag_name)
    template_name = "novels/book_list_back.html"
    tag = Tag.objects.get(name=tag_name)
    book_list = Book.objects.filter(tags=tag)
    favorites = list()
    title = tag_name
    if request.user.is_authenticated:
        # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
        rows = request.user.favorite_ads.values('id')
        # favorites = [2, 4, ...] using list comprehension
        favorites = [row['id'] for row in rows]
    ctx = {'title': title, 'book_list': book_list, 'favorites': favorites}
    return render(request, template_name, ctx)


class BookListView(OwnerListView):
    model = Book
    template_name = "novels/book_list_back.html"

    def get(self, request) :
        book_list = Book.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        ctx = {'title': 'All Book', 'book_list' : book_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)


class BookDetailView(OwnerDetailView):
    model = Book
    template_name = 'novels/book_detail.html'

    def get(self, request, pk) :
        x = Book.objects.get(id=pk)
        comments = Comment.objects.filter(book=x).order_by('-updated_at')
        tags = Tag.objects.filter(book=x)
        chapters = Chapter.objects.filter(book=x).order_by('created_at')
        comment_form = CommentForm()
        context = {'book': x, 'comments': comments, 'comment_form': comment_form,
                    'chapters': chapters, 'tags':tags}
        return render(request, self.template_name, context)


class BookDeleteView(OwnerDeleteView):
    model = Book
    template_name = 'novels/book_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy("novels:all")


class BookCreateView(LoginRequiredMixin, View):
    template_name = 'novels/book_form.html'

    def get(self, request, pk=None):
        form = CreateBookForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateBookForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        success_url = reverse_lazy('novels:book_detail', kwargs={'pk': pic.id})
        return redirect(success_url)


class BookUpdateView(LoginRequiredMixin, View):
    template_name = 'novels/book_form.html'

    def get(self, request, pk):
        pic = get_object_or_404(Book, id=pk, owner=self.request.user)
        form = CreateBookForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Book, id=pk, owner=self.request.user)
        form = CreateBookForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()
        success_url = reverse_lazy('novels:book_detail', kwargs={'pk': pic.id})
        return redirect(success_url)


class ChapterDetailView(OwnerDetailView):
    model = Chapter
    template_name = 'novels/chapter_detail.html'

    def get(self, request, ck):
        x = Chapter.objects.get(id=ck)
        context = {'chapter': x}
        return render(request, self.template_name, context)


class ChapterCreateView(LoginRequiredMixin, View):
    template_name = 'novels/chapter_form.html'

    def get(self, request, pk):
        form = CreateChapterForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        form = CreateChapterForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.book = Book.objects.get(id=pk)
        pic.save()
        success_url = reverse_lazy('novels:book_detail', kwargs={'pk': pic.book.id})
        return redirect(success_url)

class ChapterUpdateView(LoginRequiredMixin, View):
    template_name = 'novels/book_form.html'

    def get(self, request, ck):
        pic = get_object_or_404(Chapter, id=ck, owner=self.request.user)
        form = CreateChapterForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, ck):
        pic = get_object_or_404(Chapter, id=ck, owner=self.request.user)
        form = CreateChapterForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()
        success_url = reverse_lazy('novels:book_detail', kwargs={'pk': pic.book.id})
        return redirect(success_url)


class ChapterDeleteView(OwnerDeleteView):
    model = Chapter
    template_name = 'novels/chapter_confirm_delete.html'

    def get_success_url(self):
        return reverse("novels:book_detail", args=[self.object.book.id])


def stream_file(request, pk):
    pic = get_object_or_404(Book, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.cover)
    response.write(pic.cover)
    return response


class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, pk) :
        f = get_object_or_404(Book, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, book=f)
        comment.save()
        return redirect(reverse('novels:book_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "novels/comment_delete.html"
    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id

    def get_success_url(self):
        book = self.object.book
        return reverse('novels:book_detail', args=[book.id])


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Book, id=pk)
        fav = Fav(user=request.user, book=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Delete PK", pk)
        t = get_object_or_404(Book, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, book=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()