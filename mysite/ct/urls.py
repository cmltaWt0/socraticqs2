from django.conf.urls import patterns, include, url
from ct.views import *

urlpatterns = patterns('',
    url(r'^$', main_page, name='home'),
    url(r'^about/$', about, name='about'),
    url(r'^people/(?P<user_id>\d+)/$', person_profile, name='person_profile'),
    # instructor UI
    # course tabs
    url(r'^teach/courses/(?P<course_id>\d+)/$', course_view, name='course'),
    url(r'^teach/courses/(?P<course_id>\d+)/edit/$',
        edit_course, name='edit_course'),
    # courselet tabs
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/$',
        unit_tasks, name='unit_tasks'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/$',
        unit_concepts, name='unit_concepts'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/$',
        unit_lessons, name='unit_lessons'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/resources/$',
        unit_resources, name='unit_resources'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/edit/$',
        edit_unit, name='edit_unit'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/wikipedia/(?P<source_id>[^/]+)/$',
        wikipedia_concept, name='wikipedia_concept'),
    # lesson tabs
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/$',
        ul_teach, name='ul_teach'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/tasks/$',
        ul_tasks, name='ul_tasks'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/concepts/$',
        ul_concepts, name='ul_concepts'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/errors/$',
        ul_errors, name='ul_errors'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/faq/$',
        ul_faq_student, name='ul_faq'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/faq/(?P<resp_id>\d+)/$',
        ul_thread_student, name='ul_thread'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/edit/$',
        edit_lesson, name='edit_lesson'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/live/$',
        live_question, name='live_question'),
    # concept tabs
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/$',
        ul_teach, name='concept_teach'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/tasks/$',
        ul_tasks, name='concept_tasks'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/concepts/$',
        concept_concepts, name='concept_concepts'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/lessons/$',
        concept_lessons, name='concept_lessons'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/errors/$',
        concept_errors, name='concept_errors'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/faq/$',
        ul_faq_student, name='concept_faq'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/faq/(?P<resp_id>\d+)/$',
        ul_thread_student, name='concept_thread'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/edit/$',
        edit_lesson, name='edit_concept'),
    # error tabs
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/errors/(?P<ul_id>\d+)/$',
        resolutions, name='resolutions'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/errors/(?P<ul_id>\d+)/resources/$',
        error_resources, name='error_resources'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/errors/(?P<ul_id>\d+)/faq/$',
        ul_faq_student, name='error_faq'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/errors/(?P<ul_id>\d+)/faq/(?P<resp_id>\d+)/$',
        ul_thread_student, name='error_thread'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/errors/(?P<ul_id>\d+)/edit/$',
        edit_lesson, name='edit_error'),
    # responses
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/responses/(?P<resp_id>\d+)/assess/$',
        assess, name='assess_teach'),
    url(r'^teach/courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/responses/(?P<resp_id>\d+)/errors/$',
        assess_errors, name='assess_errors_teach'),

    # student UI
    # course tabs
    url(r'^courses/(?P<course_id>\d+)/$', course_view, name='course_student'),
    # unit tabs
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/$',
        study_unit, name='study_unit'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/slideshow/$',
        slideshow, name='slideshow'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/tasks/$',
        unit_tasks_student, name='unit_tasks_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/$',
        unit_lessons_student, name='unit_lessons_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/$',
        unit_concepts_student, name='unit_concepts_student'),
    # lesson tabs
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/tasks/$',
        ul_tasks_student, name='ul_tasks_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/concepts/$',
        ul_concepts, name='ul_concepts_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/errors/$',
        ul_errors_student, name='ul_errors_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/faq/$',
        ul_faq_student, name='ul_faq_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/faq/(?P<resp_id>\d+)/$',
        ul_thread_student, name='ul_thread_student'),
    # concept tabs
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/$',
        study_concept, name='study_concept'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/tasks/$',
        ul_tasks_student, name='concept_tasks_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/lessons/$',
        concept_lessons_student, name='concept_lessons_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/faq/$',
        ul_faq_student, name='concept_faq_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<ul_id>\d+)/faq/(?P<resp_id>\d+)/$',
        ul_thread_student, name='concept_thread_student'),
    # error tabs
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/errors/(?P<ul_id>\d+)/$',
        resolutions_student, name='resolutions_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/errors/(?P<ul_id>\d+)/resources/$',
        error_resources, name='error_resources_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/errors/(?P<ul_id>\d+)/faq/$',
        ul_faq_student, name='error_faq_student'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/errors/(?P<ul_id>\d+)/faq/(?P<resp_id>\d+)/$',
        ul_thread_student, name='error_thread_student'),
    # study pages
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/$',
        lesson, name='lesson'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/ask/$',
        ul_respond, name='ul_respond'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/responses/(?P<resp_id>\d+)/assess/$',
        assess, name='assess'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/responses/(?P<resp_id>\d+)/errors/$',
        assess_errors, name='assess_errors'),
    # Public couses page for anonymous users
    url(r'^courses/$', courses, name='courses'),
    # Subscribe to course with particular id
    url(r'^courses/(?P<course_id>\d+)/subscribe/$', courses_subscribe, name='subscribe'),

    # FSM node pages
    url(r'^nodes/(?P<node_id>\d+)/$', fsm_node, name='fsm_node'),
    url(r'^nodes/$', fsm_status, name='fsm_status'),

)
