from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.forms.widgets import ChoiceFieldRenderer, RendererMixin, Select
from ct.models import Course, Unit, Lesson, UnitLesson
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from ct.models import Course, CourseUnit, Unit, Lesson, UnitLesson
from ctms.models import Invite
from django.contrib.auth.models import User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'addedBy')
        widgets = {
            'addedBy': forms.HiddenInput
        }


class CreateUnitForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title',)


class EditUnitForm(forms.ModelForm):
    KIND_CHOICES = (
        (Lesson.EXPLANATION, 'Introduction'),
        (Lesson.ORCT_QUESTION, 'Question'),
    )
    unit_type = forms.ChoiceField(choices=KIND_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Lesson
        fields = ('title', 'text', 'unit_type')

    def save(self, commit=True):
        self.instance.kind = self.cleaned_data['unit_type']
        return super(EditUnitForm, self).save(commit)


class AddEditUnitForm(EditUnitForm):
    class Meta:
        model = Lesson
        fields = ('title', 'text', 'unit_type')


class AddEditUnitAnswerForm(forms.ModelForm):
    answer = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Lesson
        fields = ('answer', )

    def save(self, unit, user, ul, commit=True):
        self.instance.text = self.cleaned_data['answer']
        # if self.instance.id:
        self.instance.title = 'Answer'
        self.instance.addedBy = user
        self.instance.kind = Lesson.ANSWER
        self.instance.save_root()
        ul = UnitLesson.create_from_lesson(self.instance, unit, kind=UnitLesson.ANSWERS, parent=ul)
        lesson = super(AddEditUnitAnswerForm, self).save(commit)
        return lesson


class ErrorModelForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'text')

    def save(self, questionUL, user, commit=True):
        self.instance.addedBy = user
        return self.instance.save_as_error_model(questionUL.lesson.concept, questionUL)

ErrorModelFormSet = modelformset_factory(Lesson, form=ErrorModelForm, fields=('id', 'title', 'text'))


class CreateCourseletForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('title',)


class InviteForm(forms.ModelForm):
    def __init__(self, course=None, instructor=None, *args, **kwargs):
        self.course = course
        self.instructor = instructor
        super(InviteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Invite
        fields = ('email', 'type', 'course')
        widgets = {
            'type': forms.HiddenInput,
            'course': forms.HiddenInput,

        }

    def save(self, commit=True):
        invite = Invite.create_new(
            commit=False,
            instructor=self.instructor,
            course=self.course,
            email=self.cleaned_data['email'],
            invite_type=self.cleaned_data['type'],
        )
        self.instance = invite
        return super(InviteForm, self).save(commit=commit)
