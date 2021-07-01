from django.contrib import admin
from vehicles.models import UKLicensedVehicles

#class RVLicensedAdmin(admin.ModelAdmin):
#    #list_display = ['rvtype', 'rvmake', 'rvmodel', 'rvvariant', 'number_licensed', 'year_licensed']
#    #ordering = ('rvmake', 'rvmodel', 'rvvariant', 'year_licensed',)
#    #list_filter = ['year_licensed', 'rvtype', 'rvmake', 'rvmodel', 'rvvariant' ]

#admin.site.register(RVLicensed, RVLicensedAdmin)