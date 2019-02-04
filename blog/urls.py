from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blog/<int:pk>', views.blog_detail_view, name='blog-detail'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('myblogs/', views.UsersBlogListView.as_view(), name='my-blogs'),
    path('blog/create/', views.BlogCreate.as_view(), name='blog-create'),
    path('blog/<int:pk>/update/', views.BlogUpdate.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', views.BlogDelete.as_view(), name='blog-delete'),
    path('blog/<int:pk>/<int:com_pk>', views.delete_comment, name='comment-delete'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.update_profile, name='update-profile'),
    path('delete/', views.delete_profile, name='delete-profile'),
]