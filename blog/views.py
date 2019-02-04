from django.shortcuts import render
from django.views import generic
from .models import Blogger, Blog, Comment
from .forms import CommentModelForm, UserForm, BloggerForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

def index(request):
    num_blogs = Blog.objects.all().count()
    num_bloggers = Blogger.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={
            'num_blogs': num_blogs,
            'num_bloggers': num_bloggers,
            'num_visits': num_visits,
        }
    )

class BlogListView(generic.ListView):
    model = Blog
    context_object_name = 'blog_list'
    template_name = 'blog/blog_list.html'
    paginate_by = 5

class BloggerListView(generic.ListView):
    model = Blogger
    context_object_name = 'blogger_list'
    template_name = 'blog/blogger_list.html'
    paginate_by = 5

class BloggerDetailView(generic.DetailView):
    model = Blogger

def blog_detail_view(request, pk):
    blog=get_object_or_404(Blog, pk=pk)
    comment_list = blog.comment_set.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(comment_list, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    if request.user.is_active:
        if request.method == 'POST':
            form = CommentModelForm(request.POST)
            if form.is_valid():
                comment = Comment(
                    blog=blog,
                    author=Blogger.objects.get(user=request.user),
                    date=datetime.datetime.now(),
                    description=form.cleaned_data['description']
                )
                comment.save()
                return HttpResponseRedirect(reverse('blog-detail', args=[str(blog.pk)]))
        else:
            form = CommentModelForm()
            return render(
                request,
                'blog/blog_detail.html',
                context={'blog': blog, 'form' : form, 'comment_pages':comments}
            )
    else:
        return render(
            request,
            'blog/blog_detail.html',
            context={'blog': blog, 'comment_pages':comments}
        )

class UsersBlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'blog/users_blog_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.filter(author=Blogger.objects.get(user=self.request.user))

class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['name', 'description']

    def form_valid(self, form):
        author = get_object_or_404(Blogger, pk=self.request.user.pk)
        date = datetime.datetime.now()
        form.instance.author = author
        form.instance.date = date
        return super().form_valid(form)

class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['name', 'description']

    def form_valid(self, form):
        date = datetime.datetime.now()
        form.instance.date = date
        return super().form_valid(form)

class BlogDelete(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('my-blogs')

def delete_comment(request, pk, com_pk):
    comment = get_object_or_404(Comment, pk=com_pk)
    comment.delete()
    return HttpResponseRedirect(reverse('blog-detail', args=[str(pk)]))

def signup(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.blogger.bio = form.cleaned_data.get('bio')
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            form = SignUpForm()
        return render(request, 'blog/signup.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('index'))

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        blogger_form = BloggerForm(request.POST, instance=request.user.blogger)
        if user_form.is_valid() and blogger_form.is_valid():
            user_form.save()
            blogger_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        blogger_form = BloggerForm(instance=request.user.blogger)
    return render(request, 'blog/profile.html', {
        'user_form': user_form,
        'blogger_form': blogger_form
    })

@login_required
@transaction.atomic
def delete_profile(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        user.delete()
        return HttpResponseRedirect(reverse('logout'))
    else:
        return render(request, 'blog/profile_delete.html',)