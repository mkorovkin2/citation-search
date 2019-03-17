from django import forms
import unidecode

# Form used for searching publications
class PubSearchForm(forms.Form):
   username = forms.CharField(max_length=200)
   choosepaper = forms.BooleanField(initial=False, required=False)

   def clean_user(self):
      username = self.cleaned_data.get('username')
      return username

   def clean_choosepaper(self):
      choosepaper = self.cleaned_data.get('choosepaper')
      return choosepaper

   def clean(self):
      data = self.cleaned_data

      username = data.get('username')
      choosepaper = data.get('choosepaper')
      data['username'] = unidecode.unidecode(username)
      data['choosepaper'] = choosepaper

      return data

# Form used for searching general data
class SearchForm(forms.Form):
   username = forms.CharField(max_length=200)

   def clean_user(self):
      # super(SearchForm, self).clean()
      username = self.cleaned_data.get('username')
      return username

   def clean(self):
      data = self.cleaned_data

      username = data.get('username')
      data['username'] = unidecode.unidecode(username)

      return data

# Form used for searching author with the goal of pulling previously-existing data
class AuthorRepullSearchForm(forms.Form):
   username = forms.CharField(max_length=200)
   includedkey = forms.CharField(max_length=400, required=False)
   excludedkey = forms.CharField(max_length=400, required=False)
   filter = forms.BooleanField(initial=False, required=False)
   repull = forms.BooleanField(initial=False, required=False)

   def clean_user(self):
      # super(SearchForm, self).clean()
      username = self.cleaned_data.get('username')
      return username

   def clean_includedkey(self):
      includedkey = self.cleaned_data.get('includedkey')
      return includedkey

   def clean_excludedkey(self):
      excludedkey = self.cleaned_data.get('excludedkey')
      return excludedkey

   def clean_filter(self):
      filter = self.cleaned_data.get('filter')
      return filter

   def clean_repull(self):
      repull = self.cleaned_data.get('repull')
      return repull

   def clean(self):
      data = self.cleaned_data

      username = data.get('username')
      i_key = data.get('includedkey')
      e_key = data.get('excludedkey')
      data['username'] = username

      filter = data.get('filter')
      if filter == None:
         data['filter'] = False
      else:
         data['filter'] = filter

      repull = data.get('repull')
      if repull == None:
         data['repull'] = False
      else:
         data['repull'] = repull

      data['includedkey'] = i_key
      data['excludedkey'] = e_key

      return data

# Form used for searching author data
class AuthorSearchForm(forms.Form):
   username = forms.CharField(max_length=200)
   includedkey = forms.CharField(max_length=400, required=False)
   excludedkey = forms.CharField(max_length=400, required=False)
   filter = forms.BooleanField(initial=False, required=False)

   def clean_user(self):
      # super(SearchForm, self).clean()
      username = self.cleaned_data.get('username')
      return username

   def clean_includedkey(self):
      includedkey = self.cleaned_data.get('includedkey')
      return includedkey

   def clean_excludedkey(self):
      excludedkey = self.cleaned_data.get('excludedkey')
      return excludedkey

   def clean_filter(self):
      filter = self.cleaned_data.get('filter')
      return filter

   def clean(self):
      data = self.cleaned_data

      username = data.get('username')
      i_key = data.get('includedkey')
      e_key = data.get('excludedkey')
      data['username'] = username

      filter = data.get('filter')
      if filter == None:
         data['filter'] = False
      else:
         data['filter'] = filter

      data['includedkey'] = i_key
      data['excludedkey'] = e_key

      return data