from django.contrib import admin
from .models import BookModel, ReviewModel, CategoryModel
# Register your models here.


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']


admin.site.register(BookModel)
admin.site.register(ReviewModel)
admin.site.register(CategoryModel, CategoryModelAdmin)
