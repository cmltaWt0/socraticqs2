import injections
from django.utils import timezone
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, mixins, views, generics
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Message, Chat, UnitError
from .serializers import MessageSerializer, ChatHistorySerializer, ChatProgressSerializer
from .services import ProgressHandler, SequenceHandler
from .permissions import IsOwner
from ct.models import Response as StudentResponse


inj_alternative = injections.Container()
inj_alternative['next_handler'] = SequenceHandler()
MessageSerializer = inj_alternative.inject(MessageSerializer)


def get_additional_messages(chat):
    print 'additional lessons'
    course_unit = chat.enroll_code.courseUnit
    unit = course_unit.unit
    addition_tasks = [(ul, 'selfeval')
                      for ul in unit.get_selfeval_uls(chat.user)]
    addition_tasks += [(ul, 'classify')
                       for ul in unit.get_serrorless_uls(chat.user)]
    addition_tasks += [(ul, 'resolve')
                       for ul in unit.get_unresolved_uls(chat.user)]
    # map(lambda (ul, task): Message.objects.get_or_create(contenttype='unitlesson',
    #                                                      content_id=ul.id,
    #                                                      chat=chat,
    #                                                      owner=chat.user,
    #                                                      is_additional=True),
    #     addition_tasks)
    lesson_ids = chat.enroll_code.courseUnit.unit.unitlesson_set.filter(order__isnull=False).values_list('id', flat=True)
    print lesson_ids
    for (ul, task) in addition_tasks:
        if ul not in lesson_ids:
            m, cr = Message.objects.get_or_create(contenttype='unitlesson',
                                                  content_id=ul.id,
                                                  chat=chat,
                                                  owner=chat.user,
                                                  is_additional = True)


@injections.has
class MessagesView(generics.RetrieveUpdateAPIView, viewsets.GenericViewSet):

    parser_classes = (JSONParser,)

    next_handler = injections.depends(ProgressHandler)

    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner)

    def retrieve(self, request, *args, **kwargs):
        message = self.get_object()
        chat = Chat.objects.filter(user=self.request.user).first()
        next_point = chat.next_point

        if (message.contenttype in ['response', 'uniterror'] and
            message.content_id and
            next_point == message):
            chat.next_point = self.next_handler.next_point(
                current=message.content, chat=chat, message=message, request=request
            )
            chat.save()
            serializer = self.get_serializer(message)
            return Response(serializer.data)


        if not message.chat or message.chat != chat or message.timestamp:
            print('FAULT')
            serializer = self.get_serializer(message)
            return Response(serializer.data)


        if (
            message.input_type == 'text' or
            message.input_type == 'options' or
            message.contenttype == 'uniterror'
            ):
            serializer = self.get_serializer(message)
            return Response(serializer.data)

        if message:
            # if message.input_type == 'finish':
            # Set next message for user
            if not message.timestamp:
                message.timestamp = timezone.now()
            message.save()
            chat.next_point = self.next_handler.next_point(
                current=message.content, chat=chat, message=message, request=request
            )
            chat.save()
            message.chat = chat


        serializer = self.get_serializer(message)
        return Response(serializer.data)

    def perform_update(self, serializer):
        message = self.get_object()
        chat = Chat.objects.filter(user=self.request.user).first()

        # Check if message is not in current chat
        if not message.chat or message.chat != chat:
            return
        if message.input_type == 'text':
            message.chat = chat
            text = self.request.data.get('text')
            if not message.content_id:
                resp = StudentResponse(text=text)
                resp.lesson = message.lesson_to_answer.lesson
                resp.unitLesson = message.lesson_to_answer
                resp.course = message.chat.enroll_code.courseUnit.course
                resp.author = self.request.user
            else:
                resp = message.content
                resp.text = text
            resp.save()
            if not message.timestamp:
                message.content_id = resp.id
                chat.next_point = message
                # chat.next_point = self.next_handler.next_point(
                #     current=message.content, chat=chat, message=message, request=self.request
                #     )
                chat.save()
                serializer.save(content_id=resp.id, timestamp=timezone.now(), chat=chat)
            else:
                serializer.save()
        if message.input_type == 'options':
            if (
                message.contenttype == 'uniterror' and
                'selected' in self.request.data
            ):
                get_additional_messages(chat)
                message.chat = chat
                # message.timestamp = timezone.now()
                selected = self.request.data.get('selected')[str(message.id)]['errorModel']
                uniterror = message.content
                uniterror.save_response(user=self.request.user, response_list=selected)

                # chat.next_point = message

                chat.next_point = self.next_handler.next_point(
                    current=message.content, chat=chat, message=message, request=self.request
                )
                chat.save()
                serializer.save(chat=chat)
            else:
                message.chat = chat
                # message.timestamp = timezone.now()
                selfeval = self.request.data.get('option')
                resp = message.content
                resp.selfeval = selfeval
                resp.save()
                chat.next_point = message

                # chat.next_point = self.next_handler.next_point(
                #     current=message.content, chat=chat, message=message, request=self.request
                # )
                chat.save()
                # serializer.save(content_id=resp.id, timestamp=timezone.now(), chat=chat)
                serializer.save(content_id=resp.id, chat=chat)



class HistoryView(generics.RetrieveAPIView):
    """
    List all messages in chat w/ additional info.
    """
    def get(self, request, *args, **kwargs):
        chat = Chat.objects.all().first()
        serializer = ChatHistorySerializer(chat)
        return Response(serializer.data)


class ProgressView(generics.RetrieveAPIView):
    """
    Return progress for chat.
    """
    def get(self, request, *args, **kwargs):
        chat = Chat.objects.all().first()
        serializer = ChatProgressSerializer(chat)
        return Response(serializer.data)
