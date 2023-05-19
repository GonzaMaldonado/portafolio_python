from django.urls import path
from .views import IndexView, CategoryDetailView, ListAllCategoriesView, ShowPostDetailView

app_name = 'posts'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('category/<slug:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/', ListAllCategoriesView.as_view(), name='all_categories'),
    path('article/<slug:slug>', ShowPostDetailView.as_view(), name='post'),
]