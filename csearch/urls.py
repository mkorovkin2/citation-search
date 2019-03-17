from django.conf.urls import url
from django.views.generic import TemplateView, FormView
from csearch import views

urlpatterns = [
   url(r'^author/',TemplateView.as_view(template_name='presubmit.html')),
   url(r'^publication/',TemplateView.as_view(template_name='presubmit_pub.html')),
   url(r'^submit_request/', views.search_submit_request, name='submit_request'),
   url(r'^search_author/', views.search, name='searchg'),
   url(r'^search_author_updated/', views.search, name='searchg2'),
   url(r'^search_publication/', views.search_pub, name='searchp'),
   url(r'^list_view/', views.display_list, name='display_list'),
   url(r'^updated/', views.update_list, name='update_list'),
   url(r'^select_papers/', views.select_papers, name='select_papers'),
   url(r'^search_publication_specified/', views.search_pub_specified_paper, name='searchp_specified'),
   url(r'^submitted_filtered/', views.submitted_filtered, name='submitted_filtered')

]