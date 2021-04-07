from django import forms
from novels.models import Book,Chapter
from django.core.files.uploadedfile import InMemoryUploadedFile
from novels.humanize import naturalsize
from django.core.exceptions import ValidationError
from django.core import validators

# Create the form class.
class CreateBookForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    cover = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Book
        fields = ['title','tags', 'description','cover']  # Picture is manual

        # Validate the size of the picture                                                                  def clean(self):
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:                                                                                         return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < " + self.max_upload_limit_text + " bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateBookForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.cover  # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance


class CreateChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['name','text']  # Picture is manual

class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)