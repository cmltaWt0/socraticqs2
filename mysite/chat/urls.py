import injections
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter

from .views import ChatInitialView
from .api import MessagesView
from .services import SequenceHandler, FsmHandler


inj = injections.Container()
inj['next_handler'] = SequenceHandler()
# Injects appropriate ProgressHandler
MessagesView = inj.inject(MessagesView)
ChatInitialView = inj.inject(ChatInitialView)

router = SimpleRouter()
router.register(r'messages', MessagesView, base_name='messages')

urlpatterns = patterns(
    '',
    url(r'^enrollcode/(?P<enroll_key>[a-zA-Z0-9]+)/$', ChatInitialView.as_view(), name='chat_enroll'),
    url(r'^', include(router.urls)),
)
