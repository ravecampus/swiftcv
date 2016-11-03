from django.contrib import admin

# Register your models here.

from .models import (
    Account, 
    Section,  
    Work, 
    Education,
    SpecialSection,
    )


# class AccountAdmin(admin.ModelAdmin):
#     model = Account
#     list_display = ['email', 'email_cv', 'full_name', 'phone', 'website', 'address_l1', 'address_l2', 'address_l3']


class EducationAdmin(admin.ModelAdmin):
    model = Education
    list_display = ['course', 'institution', 'start', 'end', 'other_information']


# class QualificationAdmin(admin.ModelAdmin):
#     model = Qualification

class SectionAdmin(admin.ModelAdmin):
    model = Section
    list_display = ['name']

admin.site.register(Work)
admin.site.register(Section, SectionAdmin)
admin.site.register(Education, EducationAdmin)    
admin.site.register(Account)
admin.site.register(SpecialSection)
