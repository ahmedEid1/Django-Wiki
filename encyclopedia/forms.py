from django import forms


class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


class EditForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)
