from django.conf.urls import url
from basic_app import views


app_name = 'basic_app'

urlpatterns=[
    #path('register',views.register,name='register'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^my_messages/$', views.my_messages, name='my_messages'),
    url(r'^my_unread_messages/$', views.my_unread_messages, name='my_unread_messages'),
    url(r'^message_page/(?P<message_id>[0-9]+)/$', views.message_page, name='message_page'),
    url(r'^delete_message/(?P<message_id>[0-9]+)/$', views.delete_message, name='delete_message'),


]
