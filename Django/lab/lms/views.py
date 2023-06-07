from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from datetime import date, datetime
from django.contrib.auth.decorators import login_required

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

from .models import *
from .forms import *
from .filters import *

from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Count

def about(request):
    return render(request, 'about.html')
#Chat
@login_required
def home(request):
    return render(request, 'home.html')
@login_required
def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })
@login_required
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)
@login_required
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')
@login_required
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


#test
class AnalysisCategoryChartDataView(View):
    def get(self, request, *args, **kwargs):
        chart_data = Journal.objects.values('analysis_cathegory__name') \
            .annotate(count=Count('analysis_cathegory')) \
            .order_by('-count')[:8]
        labels = [item['analysis_cathegory__name'] for item in chart_data]
        data = [item['count'] for item in chart_data]
        return JsonResponse(data={
            'labels': labels,
            'data': data
        })

# Journal PDF-----------------
def journal_report(request, journal_id):
    # Получить запись Journal
    journal = Journal.objects.get(id=journal_id)

    # Создание PDF-документа в буфере памяти
    

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('FreeSans', 'static/FreeSans.ttf'))
    # Настройка шрифтов и размеров
    pdf.setFont("FreeSans", 28)
    width, height = letter

    # Вывод данных из записи журнала на страницу PDF-документа
    pdf.drawImage("static/logo.jpg", 50, height - 25, width=75, height=75)
    pdf.drawString(180, height - 20,'Лаборатория МЕДСИ')
    pdf.line(0,height -28,600,height -28)
    pdf.setFont("FreeSans", 14)
    pdf.drawString(50, height - 50, f"Номер заявки: {journal.number}")
    pdf.line(145,height -55,300,height -55)
    pdf.drawString(50, height - 75, f"ФИО : {journal.client_name} {journal.client_surname}")
    pdf.line(95,height -80,300,height -80)
    pdf.drawString(50, height - 100, f"Пол: {journal.sex}")
    pdf.line(80,height -105,100,height -105)
    pdf.drawString(50, height - 125, f"Дата рождения: {journal.birth}")
    pdf.line(160,height -130,240,height -130)
    pdf.drawString(50, height - 150, f"Подразделение: {', '.join(str(c) for c in journal.analysis_cathegory.all())}")
    pdf.line(160,height -155,550,height -155)
    pdf.drawString(50, height - 175, f"Название анализа: {', '.join(str(a) for a in journal.analysis_name.all())}")
    pdf.line(175,height -180,550,height -180)
    pdf.drawString(50, height - 200, f"Норма результатов: {journal.norma}")
    pdf.line(180,height -205,550,height -205)
    pdf.drawString(50, height - 225, f"Результаты анализов: {journal.description}")
    pdf.line(195,height -230,550,height -230)
    pdf.setFont("FreeSans", 8)
    pdf.drawString(50, height - 275, "Әртүрлі әдістерді немесе жабдықтарды қолданып жасаған бірдей зерттеудің нәтижелері әртүрлі болуы мүмкін.")
    pdf.drawString(50, height - 285, "Алынған зертханалық талдаудың нәтижелері диагноз болып табылмайды және дәрігердің кеңесін талап етеді.")
    pdf.drawString(50, height - 305, "Результаты одних и тех же исследований , проведенных с применением разных методик или оборудования, могут различаться. ")
    pdf.drawString(50, height - 315, "Полученные результаты лабораторных исследований, не являются диагнозом и требуют консультации лечащего врача.")
    pdf.drawImage("static/footer.jpg", 0, height - 400, width=600)

    # Закрытие PDF-документа и возврат его в ответе
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
# Journal -----------------
@login_required
def dashboard(request):
    journals = Journal.objects.all()
    
    month = request.GET.get('month', None)
    if month:
        month_date = datetime.strptime(month, '%Y-%m').date()
    else:
        month_date = date.today().replace(day=1)
    
    journ = Journal.objects.filter(date_time__year=month_date.year, date_time__month=month_date.month)
    month_count = journ.count()

    today = date.today()
    jour = Journal.objects.filter(date_time__date=today)
    
    count = Journal.objects.filter(is_done='Не готов').aggregate(Count('id'))['id__count']

    current_month = datetime.now().month
    current_year = datetime.now().year

    orders_by_category = Journal.objects.filter(
        date_time__month=current_month,
        date_time__year=current_year
    ).values('analysis_cathegory__name').annotate(
        total_orders=Count('id')
    ).order_by('analysis_cathegory__name')

    categories = ['ГЕМАТОЛОГИЧЕСКИЕ', 'ОБЩЕКЛИНИЧЕСКИЕ', 'БИОХИМИЧЕСКИЕ', 'ИММУНОЛОГИЧЕСКИЕ',
                  'ОНКОМАРКЕРЫ', 'АЛЛЕРГОЛОГИЧЕСКИЕ', 'ПОЛОВЫЕ ИНФЕКЦИИ', 'ГОРМОНЫ']
    orders_by_category = orders_by_category.filter(analysis_cathegory__name__in=categories)

    today_count = jour.count()
    orders_count = journals.count()
    return render(request, 'dashboard.html', {
        'journals': journals,
        'orders_by_category': orders_by_category,
        'count': count,
        'orders_count': orders_count,
        'today_count': today_count,
        'month_count': month_count,
    })
@login_required
def index(request):
    journals = Journal.objects.all()
    journals = Journal.objects.order_by('-id')

    filter = JournalFilter(request.GET, queryset=journals)
    journals = filter.qs
    return render(request, 'index.html', {
        'journals': journals,
        'filter': filter,
        
    })
@login_required
def view_journal(request, id):
    journal = Journal.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))
@login_required
def add(request):
  if request.method == 'POST':
    form = JournalForm(request.POST)
    if form.is_valid():
      new_number= form.cleaned_data['number']
      new_client_name = form.cleaned_data['client_name']
      new_client_surname = form.cleaned_data['client_surname']
      new_client_phone = form.cleaned_data['client_phone']
      new_sex = form.cleaned_data['date_time']
      new_birth = form.cleaned_data['date_time']
      new_analysis_name = form.cleaned_data['analysis_name']
      new_analysis_cathegory = form.cleaned_data['analysis_cathegory']
      new_date_time = form.cleaned_data['date_time']
      new_is_done = form.cleaned_data['is_done']
      new_description = form.cleaned_data['description']
      new_norma = form.cleaned_data['norma']

      new_journal = Journal(
        number=new_number,
        client_name=new_client_name,
        client_surname=new_client_surname,
        client_phone=new_client_phone, 
        birth=new_birth,
        sex=new_sex,
        date_time=new_date_time, 
        is_done=new_is_done, 
        description=new_description, 
        norma=new_norma
      )
      new_journal.save()
      new_journal.analysis_name.set(new_analysis_name)
      new_journal.analysis_cathegory.set(new_analysis_cathegory)
      return render(request, 'add.html', {
        'form': JournalForm(),
        'success': True
      })
  else:
    form = JournalForm()
  return render(request, 'add.html', {
    'form': JournalForm()
  })
@login_required  
def edit(request, id):
    journal = Journal.objects.get(pk=id)
    if request.method == 'POST':
        
        form = JournalFor(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return render(request, 'edit.html', {
                'form': form,
                'success': True
            })
    else:
        form = JournalFor(instance=journal)
    return render(request, 'edit.html', {
        'form': form
    })
@login_required
def delete(request, id):
  if request.method == 'POST':
    journal = Journal.objects.get(pk=id)
    journal.delete()
  return HttpResponseRedirect(reverse('index'))


#Price  -------------
@login_required
def index_price(request):
    return render(request, 'price.html', {
        'price': Price.objects.order_by('name')

    }) 
@login_required
def delete_price(request, id):
  if request.method == 'POST':
    price = Price.objects.get(pk=id)
    price.delete()
  return HttpResponseRedirect(reverse('price'))
@login_required
def add_price(request):
  if request.method == 'POST':
    form = PriceForm(request.POST)
    if form.is_valid():
      new_name= form.cleaned_data['name']
      new_day = form.cleaned_data['day']
      new_bio = form.cleaned_data['bio']
      new_price = form.cleaned_data['price']
      new_norma = form.cleaned_data['norma']
      

      new_price = Price(
        name=new_name,
        day=new_day,
        bio=new_bio,
        price=new_price,
        norma=new_norma,
        
      )
      new_price.save()
      return render(request, 'add_price.html', {
        'form': PriceForm(),
        'success': True
      })
  else:
    form = PriceForm()
  return render(request, 'add_price.html', {
    'form': PriceForm()
  })
@login_required  
def edit_price(request, id):
    if request.method == 'POST':
        price = Price.objects.get(pk=id)
        form = PriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return render(request, 'edit_price.html', {
                'form': form,
                'success': True
            })
    else:
        price = Price.objects.get(pk=id)
        form = PriceForm(instance=price)
    return render(request, 'edit_price.html', {
        'form': form
    })
