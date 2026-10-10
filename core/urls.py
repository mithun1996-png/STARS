from django.urls import path
from . import views

urlpatterns = [
    # --- HOME & INFORMATION ---
    path('', views.home, name='home'),
    path('information/', views.information, name='information'),
    path('reviews/', views.reviews, name='reviews'),  # Fixed: Resolves NoReverseMatch for 'reviews'

    # --- TEACHERS SECTION ---
    path('teachers/', views.teacher_list, name='teachers'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('teacher/<int:id>/', views.teacher_detail, name='teacher_detail'),
    path('edit_teacher/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('delete_teacher/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('teacher/<int:teacher_id>/submit-upi/', views.submit_upi_utr, name='submit_upi_utr'),

    # --- MESS & PG SECTION ---
    path('messpg/', views.messpg_list, name='messpg_list'),
    path('add_messpg/', views.add_messpg, name='add_messpg'),
    path('mess/<int:id>/', views.mess_details, name='mess_details'),

    # --- LEARNING & ASTROPHYSICS PORTAL ---
    path('learning/python/', views.learning_python, name='learning_python'),
    path('learning/html/', views.learning_html, name='learning_html'),
    path('learning/matlab/', views.learning_matlab, name='learning_matlab'),
    path('learning/latex/', views.learning_latex, name='learning_latex'),

]