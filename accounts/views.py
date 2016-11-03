from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import login, logout
from .forms import (
    SignUpForm, 
    LoginForm, 
    EducationForm, 
    AccountForm, 
    SectionForm_,
    SectionForm,
    UploadForm,
    WorkForm,
    SpecialSectionForm,
    SpecialSectionForm_,
    )
from .models import (
    Account,
    Section,
    Education,
    Work,
    SpecialSection,
    )
from braces.views import LoginRequiredMixin
from django.conf import settings

import json


class IndexView(TemplateView):

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            return  HttpResponseRedirect(reverse('main_section'))
        return render(self.request, 'index.html', {})


class MemberView(TemplateView):
    """ Sign Up View 
    """
    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            return  HttpResponseRedirect(reverse('main_section'))
        return render(self.request,'accounts/member.html', {})

    def post(self, *args, **kwargs):
        form_id = self.request.POST.get('form_id', False)
        if form_id == 'signup':
            form = SignUpForm(self.request.POST)
            if form.is_valid():
                instance = form.save()
                instance.backend = settings.AUTHENTICATION_BACKENDS[0]
                login(self.request,instance)
                return HttpResponse(status=201)
            else:
                error_ = {}
                for err in form.errors:
                    error = form.errors[err].as_text()
                    error_[err] = str(error)
                return HttpResponseBadRequest(json.dumps(error_))
        if form_id == 'login':
            form_login = LoginForm(self.request.POST)
            if form_login.is_valid():
                login(self.request, form_login.user_cache)
                return HttpResponse(status=200)
            else:
                return HttpResponseBadRequest(json.dumps({
                    'error':form_login.errors['__all__'].as_text()
                    }))


class SectionMainView(LoginRequiredMixin, TemplateView):
    """
    """
    def get(self, *args, **kwargs):
        # section = Section.objects.get(s)
        return render(self.request, 'accounts/main_section.html',{})

    def post(self, *args, **kwargs):
        user = Account.objects.get(email=self.request.user)
        form = SectionForm(self.request.POST)
        if form.is_valid():
            instance = form.save()
            user.section.add(instance)
            return HttpResponse(json.dumps(instance.id), status=200)
        else:
            error_ = {}
            for err in form.errors:
                error = form.errors[err].as_text()
                error_[err] = str(error)
            return HttpResponseBadRequest(json.dumps(error_))


class PerSectionView(LoginRequiredMixin, TemplateView):
    """ CV Dashboard View
    """

    def get(self, *args, **kwargs):
      
        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        try:
            form = SectionForm_(instance=section)

        except SectionForm_.DoesNotExist:
            form = SectionForm_()

        special = SpecialSection.objects.filter(section=section)

        return render(self.request, 'accounts/dashboard.html', {
            'section':section,
            'form':form,
            'special': special,
            })

    def post(self, *args, **kwargs):
        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        form = SectionForm_(self.request.POST, instance=section)

        edu_data = zip(
            self.request.POST.getlist('institution'), 
            self.request.POST.getlist('course'),
            self.request.POST.getlist('start_date'),
            self.request.POST.getlist('end_date'),
            self.request.POST.getlist('information'),
            )

        education_dicts = [{
        'institution': institution, 
        'course': course,
        'start': start_date,
        'end': end_date,
        'other_information': information, 
        } for (
            institution, 
            course, 
            start_date, 
            end_date, 
            information,
            ) in edu_data]

        work_data = zip(
            self.request.POST.getlist('job'),
            self.request.POST.getlist('company'),
            self.request.POST.getlist('start_date_work'),
            self.request.POST.getlist('end_date_work'),
            self.request.POST.getlist('other_information_work'),
            )

        work_dicts = [{
        'job': job,
        'company': company,
        'start_date_work': start_date_work,
        'end_date_work': end_date_work,
        'other_information_work': other_information_work, 
        } for (
            job, 
            company, 
            start_date_work, 
            end_date_work, 
            other_information_work,
            ) in work_data]

        if form.is_valid():
            sec = form.save()
            # saving list of education background
            educs = Education.objects.filter(section=sec)

            # saving list of work experience
            works = Work.objects.filter(section=sec)

            for data, ed in zip(education_dicts, educs):  

                form_e = EducationForm(data, instance=ed)
                f = form_e.save(commit=False)
                f.section = sec
                f.save()

            for data2, wrk in zip(work_dicts, works):

                form_w = WorkForm(data2, instance=wrk)
                w = form_w.save(commit=False)
                w.section = sec
                w.save()
                
            return HttpResponse(status=200)
        else:
            error_ = {}
            for err in form.errors:
                error = form.errors[err].as_text()
                error_[err] = str(error)
            return HttpResponseBadRequest(json.dumps(error_))


class LogoutView(LoginRequiredMixin, View):
    """ Logout View
    """
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('member'))


class DeleteSectionView(View):

    def get(self, *args, **kwargs):
        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        section.delete()
        return HttpResponse(status=204)


class DeletePhotoView(View):

    def post(self, *args, **kwargs):
        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        form = UploadForm(self.request.POST, instance=section)
        if form.is_valid():
            fremove = form.save(commit=False)
            fremove.photo = ''
            fremove.save()
            fremove.delete_photo()
            return HttpResponse(status=204)


class DeleteEducationView(View):

    def get(self, *args, **kwargs):
        education = get_object_or_404(Education, id=kwargs.get('edu_id'))
        education.delete()
        return HttpResponse(status=204)


class EducationPageView(View):

    def post(self, *args, **kwargs):

        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        form = EducationForm(self.request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.section = section
            instance.save()
            return  HttpResponse(status=200)


class EducationLoadView(View):

    def get(self, *args, **kwargs):
        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        educ = Education.objects.filter(section=section)
        return render(self.request, 'includes/education.html', {'educ':educ})


class WorkPageView(View):

    def post(self, *args, **kwargs):
        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        form = WorkForm(self.request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.section = section
            instance.save()
            return HttpResponse(status=200)


class WorkLoadView(View):

    def get(self, *args, **kwargs):

        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        works = Work.objects.filter(section=section)
        return render(self.request, 'includes/work.html',{'works':works})

class DeleteWorkView(View):

    def get(self, *args, **kwargs):
        work = get_object_or_404(Work, id=kwargs.get('work_id'))
        work.delete()
        return HttpResponse(status=204)


class RenameSectionView(View):
    def post(self, *args, **kwargs):
        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        form = SectionForm(self.request.POST, instance=section)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
        else:
            error_ = {}
            for err in form.errors:
                error = form.errors[err].as_text()
                error_[err] = str(error)
            return HttpResponseBadRequest(json.dumps(error_))


class UploadPhotoView(View):

    def post(self, *args, **kwargs):
        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        form = UploadForm(self.request.POST, self.request.FILES, instance=section)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
        else:
            error_ = {}
            for err in form.errors:
                error = form.errors[err].as_text()
                error_[err] = str(error)
            return HttpResponseBadRequest(json.dumps(error_))


class SpecialSectionView(View):

    def post(self, *args, **kwargs):

        section = get_object_or_404(Section, id=kwargs.get('section_id'))
        form = SpecialSectionForm(self.request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.section =  section
            instance.save()
        return HttpResponse(status=200)


class DeleteSpecialSectionView(View):

    def get(self, *args, **kwargs):
        sp = get_object_or_404(SpecialSection, id=kwargs.get('sp_id'))
        sp.delete()
        return HttpResponse(status=204)

class EditSpecialSectionView(View):

    def post(self, *args, **kwargs):
        special = SpecialSection.objects.get()
        form = SpecialSectionForm_(self.request.POST,instance=special)
        return HttpResponse(status=200)


