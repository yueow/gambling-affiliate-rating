from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from casinos import models


# admin.site.unregister(User)


class CasinoAdmin(SummernoteModelAdmin):
    summernote_fields = ('content','accepted_payments', 'bonus',)

    list_filter = ("dol", 'ca_license')
    search_fields = ['title', 'content', 'ca_license', 'dol']

    save_on_top = True


class BonusAdmin(admin.ModelAdmin):
    list_display = ('bonus_digit', 'two_word_desc', 'bonus_desc', 'dep_bool', 'dep')

    list_filter = ('bonus_digit', 'casino', 'dep_bool', 'dep')
    search_fields = ('bonus_digit', 'casino', 'dep_bool', 'dep')


admin.site.register(models.Casino, CasinoAdmin)
admin.site.register(models.Bonus, BonusAdmin)

admin.site.register(models.CasinoRating)
admin.site.register(models.Feature)
admin.site.register(models.Payment)
admin.site.register(models.Software)
admin.site.register(models.Game)
admin.site.register(models.TopCasino)