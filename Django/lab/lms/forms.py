from django import forms 
from .models import *


class JournalForm(forms.ModelForm):
  class Meta:
    model = Journal
    fields = ['number','client_name','client_surname','client_phone', 'birth', 'sex', 'analysis_name', 'analysis_cathegory']
    labels = {
      'number':'Номер заявки ',
      'client_name':'Имя ',
      'client_surname':'Фамилия ',
      'client_phone':'Телефон ',
      'birth':'Дата рождения ',
      'sex':'Пол ',
      'analysis_name':'Анализ ', 
      'analysis_cathegory':'Подразделение ', 
      
    }
    widgets = {
      'number': forms.NumberInput(attrs={'class': 'form-control'}), 
      'client_name': forms.TextInput(attrs={'class': 'form-control'}),
      'client_surname': forms.TextInput(attrs={'class': 'form-control'}),
      'client_phone': forms.NumberInput(attrs={'class': 'form-control'}), 
      'birth':forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
      'sex':forms.Select(attrs={'class': 'form-control'}),
      'analysis_name': forms.SelectMultiple(attrs={'class': 'form-control select-multiple', 'size': len(Price.objects.all()),}), 
      'analysis_cathegory': forms.SelectMultiple(attrs={'class': 'form-control', 'size': len(Structure.objects.all()),}), 
      
    }
    
class JournalFor(forms.ModelForm):
  class Meta:
    model = Journal
    fields = [ 'is_done', 'description', 'norma'] 
    labels = {
      
      'is_done':'Статус', 
      'description':'Результат', 
      'norma':'Нормы',
    }
    widgets = {
      
      'is_done': forms.Select(attrs={'class': 'form-control'}),
      'description':forms.Textarea(attrs={'class': 'form-control'}), 
      'norma': forms.Select(attrs={'class': 'form-control'}),
    }

class PriceForm(forms.ModelForm):
  class Meta:
    model = Price
    fields = ['name','bio', 'day', 'price', 'norma'] 
    labels = {
      'name':'Название',
      'day':'Срок готовности',
      'bio':'Биоматериал',
      'price':'Цена',
      'norma':'Нормы',
    }
    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control'}),
      'day': forms.TextInput(attrs={'class': 'form-control'}),
      'bio': forms.TextInput(attrs={'class': 'form-control'}),
      'price': forms.NumberInput(attrs={'class': 'form-control'}),            
      'norma': forms.Select(attrs={'class': 'form-control'}),
    }