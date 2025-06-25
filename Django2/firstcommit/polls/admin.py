from django.contrib import admin

# Register your models here.


from .models import Question,Choice
from .models import Author

# admin.site.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ["pub_date", "question_text"]


# admin.site.register(Question, QuestionAdmin)
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {"fields": ["question_text"]}),
#         ("Date information", {"fields": ["pub_date"]}),
#     ]

# SELECT * FROM products WHERE username = 'Admin' OR password == 1

# admin.site.register(Question, QuestionAdmin)

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]

    list_display = ["question_text", "pub_date", "was_published_recently"]


class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
    ]

admin.site.register(Author, AuthorAdmin)


admin.site.register(Question, QuestionAdmin)