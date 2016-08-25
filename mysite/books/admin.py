from django.contrib import admin
from models import Publisher, Book, Author
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'test',)
    search_fields = ('first_name', 'last_name', 'email', 'test',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'Publisher', 'publication_date',)
    list_filter = ('publication_date', 'title',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    # fields = ('title', 'authors', 'Publisher',)
    filter_horizontal = ('authors',)
    raw_id_fields = ('Publisher',)
        


admin.site.register(Publisher)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
