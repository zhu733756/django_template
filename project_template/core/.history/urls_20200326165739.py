from django.conf.urls import url
from django.urls import include
from .auth import obtain_expiring_auth_token
from .views import *

urlpatterns = [
    url(r'user/auth', obtain_expiring_auth_token),
    url(r'post/to/crawl/file', postToCrawlFile, name="postToCrawlFile"),
    url(r'post/to/crawl/link',
        postToCrawlSingleLink,
        name="postToCrawlSingleLink"),
    url(r'task/list', getTaskList, name="getTaskList"),
    url(r'delete/task', delete_task, name="delete_task"),
    url(r'getXmlList', getXmlList, name="getXmlList"),
    url(r'online/xmlDetails', showXmlDetails, name="showXmlDetails"),
    url(r'video/callback', video_callback, name="video_callback"),
]
