from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import io

from django.http.response import HttpResponse




from .models import Test
from xlsxwriter.workbook import Workbook

# Create your views here.
def index(request):
    
    # test_list = Test.objects.order_by('name').distinct('name')
    test_list = Test.objects.values('name','epid').distinct()
    template = loader.get_template('xlsx/listView.html')
    context = {
        'test_list': test_list,
        'year_range' : range(2010,2019),
        'month_range' : range(1,13)
    }
    return HttpResponse(template.render(context, request))

def test(request, epid, test):
    return HttpResponse("Hello, epid : " + epid + " test : " + test)

def downXlsx(request, epid):
    output = io.BytesIO()

    
    
    workbook = Workbook(output, {'in_memory': True})
    test_list = Test.objects.filter(epid = epid).order_by('date')
    
    for test in test_list : 
        worksheet = workbook.add_worksheet(test.date.strftime('%m%d%Y'))
        worksheet.write(0,0,'name')
        worksheet.write(1,0,test.name)
        worksheet.write(0,1,'startDay')
        worksheet.write(1,1,str(test.startday))
        worksheet.write(0,2,'endDay')
        worksheet.write(1,2,str(test.endday))
        worksheet.write(0,3,'startLunch')
        worksheet.write(1,3,str(test.startlunch))
        worksheet.write(0,4,'endLunch')
        worksheet.write(1,4,str(test.endlunch))
        
    workbook.close()
    output.seek(0)
    
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=test.xlsx"
    
    
    # template = loader.get_template('xlsx/downXlsx.html')
    # context = {
    #     'test_list': test_list,
    # }
    return response
    # return HttpResponse(template.render(context, request))


def xlsxbydate(request):
    output = io.BytesIO()

    
    
    workbook = Workbook(output, {'in_memory': True})
    test_list = Test.objects.filter(epid = request.POST.get('epid')).order_by('date')
    
    for test in test_list : 
        worksheet = workbook.add_worksheet(test.date.strftime('%m%d%Y'))
        worksheet.write(0,0,'name')
        worksheet.write(1,0,test.name)
        worksheet.write(0,1,'startDay')
        worksheet.write(1,1,str(test.startday))
        worksheet.write(0,2,'endDay')
        worksheet.write(1,2,str(test.endday))
        worksheet.write(0,3,'startLunch')
        worksheet.write(1,3,str(test.startlunch))
        worksheet.write(0,4,'endLunch')
        worksheet.write(1,4,str(test.endlunch))
        
    workbook.close()
    output.seek(0)
    
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=test.xlsx"
    
    
    return response
    
def xlsxbymonth(request):
    output = io.BytesIO()

    
    
    workbook = Workbook(output, {'in_memory': True})
    test_list = Test.objects.filter(epid = request.POST.get('epid')).order_by('date')
    
    for test in test_list : 
        worksheet = workbook.add_worksheet(test.date.strftime('%m%d%Y'))
        
        merge_format = workbook.add_format({'align': 'center', 'bold': True})
        worksheet.merge_range('B1:W1', 'BTI Solutions : WorkingTime Card', merge_format)
        
        worksheet.merge_range('C8:C9', 'Date', merge_format)
        
        worksheet.merge_range('D8:D9', 'No.', merge_format)
        
        worksheet.merge_range('E8:E9', 'Level', merge_format)
        
        worksheet.merge_range('F8:F9', 'Name', merge_format)
        
        worksheet.merge_range('G8:J8', 'Office', merge_format)
        
        worksheet.write('G9','Clock In')
        
        worksheet.write('H9','Clock Out')
        
        worksheet.write('I9','Lunch')
        
        worksheet.write('K9','Dinner')
        
        worksheet.write(10,5,test.name)
        worksheet.write(10,6,str(test.startday))
        worksheet.write(10,7,str(test.endday))
        lunch_hour = test.startlunch - test.endlunch
        worksheet.write(10,8,str(lunch_hour.hours))
        
    workbook.close()
    output.seek(0)
    
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=test.xlsx"
    
    
    return response