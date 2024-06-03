from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError

from articles.models import Category, Posts, Comment


# Форма добавления новой статьи
class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label="Категория не выбрана",
                                 label="Категории")

    class Meta:
        model = Posts
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels ={'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError("Длина заголовка превышает 100 символов")
        return title


# Загрузка изображений
class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")


# Форма обратной связи с CAPTCHA
class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 10}))
    captcha = CaptchaField()


# Форма добавления нового комментария к статье
class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-input',
                                          'cols': 200, 'rows': 1}),
        }
        labels = {'body': 'Новый комментарий'}

