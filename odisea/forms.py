# your_app/forms.py
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "category", "content"]
        labels = {
            'title': '',
            'content': '',
            'category': '',
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10, "cols": 25, "placeholder": "Article content.."}),
        }

        def __init__(self, *args, **kwargs):
            super(Article, self).__init__(*args, **kwargs)
            self.fields["category"].empty_label = "Category"
            # following line needed to refresh widget copy of choice list
            self.fields["category"].widget.choices = self.fields["category"].choices
