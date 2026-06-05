from django.contrib import admin

# Register your models here.
class TasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'completed', 'user')
    list_filter = ('completed', 'user')
    search_fields = ('title', 'description')