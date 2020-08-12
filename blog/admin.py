from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog import models as blogModels
from casinos import models as casinoModels

# Register your models here.


class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    summernote_fields = ('content',)

    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

# # class CasinoAdmin(admin.ModelAdmin):
# #     pass

# class CasinoAdmin(SummernoteModelAdmin):
#     summernote_fields = ('content','accepted_payments', 'bonus', 'pros_c', 'cons_c',  )

#     list_filter = ('rate', 'rate_soft', 'rate_design', 'rate_safe', 'rate_faith', "dol", 'ca_license')
#     search_fields = ['title', 'content', 'ca_license', 'dol']
#     prepopulated_fields = {'slug': ('title',)}


# class BonusAdmin(admin.ModelAdmin):
#     list_display = ('bonus_digit', 'two_word_desc', 'bonus_desc', 'dep_bool', 'dep')

#     list_filter = ('bonus_digit', 'casino', 'dep_bool', 'dep')
#     search_fields = ('bonus_digit', 'casino', 'dep_bool', 'dep')

# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'image', 'is_crypto')

#     list_filter = ('name', 'is_crypto', 'casino')
#     search_fields = ('name', 'is_crypto', 'casino')    


# admin.site.register(casinoModels.Casino, CasinoAdmin)

# admin.site.register(casinoModels.Payment, PaymentAdmin)
# admin.site.register(casinoModels.Bonus, BonusAdmin)
admin.site.register(blogModels.Post, PostAdmin)