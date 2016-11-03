from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^member/$',MemberView.as_view(), name="member"),
    url(r'^CV/$',SectionMainView.as_view(), name="main_section"),
    url(r'^CV/(?P<section_id>[0-9]+)/$',PerSectionView.as_view(), name="section_id"),
    url(r'^CV/delete/(?P<section_id>[0-9]+)/$',DeleteSectionView.as_view(), name="section_delete"),
    url(r'^CV/photo/(?P<section_id>[0-9]+)/$', UploadPhotoView.as_view(), name="photo"),
    url(r'^CV/photo/del/(?P<section_id>[0-9]+)/$', DeletePhotoView.as_view(), name="delphoto"),
    url(r'^CV/rename/(?P<section_id>[0-9]+)/$', RenameSectionView.as_view(), name="rename"),

    url(r'^CV/education/(?P<section_id>[0-9]+)/$', EducationPageView.as_view(), name="edupage"),
    url(r'^CV/education/load/(?P<section_id>[0-9]+)/$', EducationLoadView.as_view(), name="eduload"),
    url(r'^CV/education/del/(?P<edu_id>[0-9]+)/$', DeleteEducationView.as_view(), name="deledu"),

    url(r'^CV/work/(?P<section_id>[0-9]+)/$', WorkPageView.as_view(), name="workpage"),
    url(r'^CV/work/load/(?P<section_id>[0-9]+)/$', WorkLoadView.as_view(), name="workload"),
    url(r'^CV/work/del/(?P<work_id>[0-9]+)/$', DeleteWorkView.as_view(), name="delwork"),

    url(r'^CV/special_section/(?P<section_id>[0-9]+)/$', SpecialSectionView.as_view(), name="special_section"),
    url(r'^CV/special_section/del/(?P<sp_id>[0-9]+)/$', DeleteSpecialSectionView.as_view(), name="delspecial_section"),
    url(r'^CV/special_section/edit/(?P<sp_id>[0-9]+)/$', EditSpecialSectionView.as_view(), name="edit_section"),

    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^$', IndexView.as_view(), name="index"),
    ]