from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import io

from django.http.response import HttpResponse
import datetime, calendar, string



from .models import Test
from xlsxwriter.workbook import Workbook



# Main Page
def index(request):
    
    # test_list = Test.objects.order_by('name').distinct('name')
    test_list = Test.objects.values('name','epid').distinct()
    template = loader.get_template('xlsx/listView.html')
    context = {
        'test_list': test_list,
        'year_range' : range(2014,2019),
        'month_range' : range(1,13)
    }
    return HttpResponse(template.render(context, request))


alphabet = list(string.ascii_uppercase)
days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    


def xlsxbymonth(request):
    # For column
    output = io.BytesIO()
    
    # Get Data with POST
    year = int(request.POST.get('year'))
    month = int(request.POST.get('month'))
    
    # Check Month's End date
    month_end = calendar.monthrange(year, month)[1]
    
    # Create New Excel File
    workbook = Workbook(output, {'in_memory': True})
    
    # First Pick by date range
    test_list = Test.objects.filter(date__range = [datetime.date( year, month , 1), datetime.date( year, month ,month_end)]).order_by('name')
    # Sorting Employees through eliminating duplicated employee ( In django, distinct query is not affordable for mysql DB )
    employees = test_list.values('name','epid').distinct()
    
    # Style for usuall Cell
    common_cell = workbook.add_format({
        'valign':'vcenter',
        'align':'center',
        'right':1,
        'top':1,
        'left':1,
      })
      # Style for usuall Cell with Time format
    common_cell_time = workbook.add_format({
        'valign':'vcenter',
        'align':'center',
        'right':1,
        'top':1,
        'left':1,
        'num_format': 'h:mm;@'
    })
      
      
    # Create daily SHEET
    # Create daily SHEET
    daily_sheet(workbook, year, month, month_end, test_list, employees, common_cell, common_cell_time)
    summary_sheet(workbook, year, month, employees, common_cell, common_cell_time)
        
        
    workbook.close()
    output.seek(0)
    
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename={}.xlsx".format(datetime.datetime.now())
    
    
    return response
    
    

def minute_interval(start, end):
    reverse = False
    if start > end:
        start, end = end, start
        reverse = True
    
    delta = (end.hour - start.hour)*60 + end.minute - start.minute + (end.second - start.second)/60.0
    if reverse:
        delta = 24*60 - delta
    
    return delta
    
def time_format(time):
    time_format = '{}:{:02d}'.format(int(time//60), int(time%60))
    return time_format
    
        
def daily_sheet(workbook, year, month, month_end, test_list, employees, common_cell, common_cell_time):
    
    for day in range(1,month_end+1): 
        # Create sheet
        worksheet = workbook.add_worksheet('{}'.format(day))
        
        # Set column's width
        worksheet.set_column(0, 0, 3)
        worksheet.set_column(4, 4, 40)
        worksheet.set_column(5, 15, 9)
        
        # Cells' Style
        sheet_title = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'bottom' : 1
        })
        
        title_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'bg_color': 'yellow',
            'top': 1,
            'right': 1
        })
        
        title_format_border = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'bg_color': 'yellow',
            'right': 2,
            'top': 1
        })
        
        cell_bold_r = workbook.add_format({
            'align':'center',
            'top':1,
            'right':2,
            'left': 1,
            'bottom':1,
            'num_format': 'h:mm;@'
        })
        
        date_cell = workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'border': 1,
            'num_format': 'mm.dd.yy;@'
            })
        
        
        # Draw Basic Line
        for c in range(1, 20):
            for r in range(7, 24):
                worksheet.write(r, c, '', common_cell)
        # name                
        for i in range(7,24):
            worksheet.write(i, 4, '', cell_bold_r)
        # office dinner
        for i in range(7,24):
            worksheet.write(i, 8, '', cell_bold_r)
        # office dinner
        for i in range(7,24):
            worksheet.write(i, 12, '', cell_bold_r)
        # total hour
        for i in range(7,24):
            worksheet.write(i, 15, '', cell_bold_r)
                
        
        
        worksheet.merge_range('B2:V2', 'BTI Solutions : WorkingTime Card',sheet_title)
        
        worksheet.merge_range('B8:B9', 'Date', title_format)
        
        worksheet.merge_range('C8:C9', 'No.', title_format)
        
        worksheet.merge_range('D8:D9', 'Level', title_format)
        
        worksheet.merge_range('E8:E9', 'Name', title_format_border)
        
        worksheet.merge_range('F8:I8', 'Office', title_format_border)
        worksheet.merge_range('J8:M8', 'Business Trip', title_format_border)
        
        worksheet.merge_range('N8:N9', 'Office Hours', title_format)
        
        worksheet.merge_range('O8:O9', 'Biz Trip Hours', title_format)
        
        worksheet.merge_range('P8:P9', 'Total Hours', title_format_border)
        
        worksheet.merge_range('Q8:Q9', 'Model', title_format)
        
        worksheet.merge_range('R8:R9', 'Version', title_format)
        
        worksheet.merge_range('S8:S9', 'Test item', title_format)
        
        worksheet.merge_range('T8:T9', 'Note', title_format)
        
        
        worksheet.write('F9','Clock In', title_format)
        worksheet.write('J9','Clock In', title_format)

        worksheet.write('G9','Clock Out', title_format)
        worksheet.write('K9','Clock Out', title_format)
        
        worksheet.write('H9','Lunch', title_format)
        worksheet.write('L9','Lunch', title_format)
        
        worksheet.write('I9','Dinner', title_format_border)
        worksheet.write('M9','Dinner', title_format_border)
        
        # date
        worksheet.merge_range('B10:B24', '{}.{}.{}'.format(month,day,year), date_cell)
        
        # no.
        for i in range(10,25):
            worksheet.write(i-1, 2, str(i-9) , common_cell)
        
        tests = test_list.filter(date = datetime.date(year, month, day))
        for idx, employee in enumerate(employees):
            worksheet.write(9+idx, 4, employee.get('name'), cell_bold_r)
            
            # If there is a employee who worked
            if tests.filter(epid = employee.get('epid')) :
                worksheet.write(9+idx, 5, str(tests.get(epid = employee.get('epid')).startday), common_cell)
            
                worksheet.write(9+idx,6,str(tests.get(epid = employee.get('epid')).endday), common_cell)
            
                lunch_hour = minute_interval(tests.get(epid = employee.get('epid')).startlunch, tests.get(epid = employee.get('epid')).endlunch)
            
                day_hour = minute_interval(tests.get(epid = employee.get('epid')).startday, tests.get(epid = employee.get('epid')).endday)
            
            
                worksheet.write(9+idx,7,str(time_format(lunch_hour)),common_cell)
                # Write total office
                worksheet.write(9+idx,13, '=G{row}-F{row}-H{row}'.format(row = 10+idx),common_cell_time)
            
                worksheet.write_formula('P{}'.format(10+idx), '=N{}+O{}'.format(10+idx,10+idx), cell_bold_r)
            else:
                continue
        
        bold_border_r = workbook.add_format({
            'right': 2
        })
        bold_border_l = workbook.add_format({
            'left': 2
        })
        bold_border_t = workbook.add_format({
            'top': 2
        })
        bold_border_b = workbook.add_format({
            'bottom': 2
        })
        
        
        # right bold
        worksheet.conditional_format('A8:A24', {
            'type': 'no_errors', 
            'format': bold_border_r
        })
        # left bold 
        worksheet.conditional_format('U8:U24', {
            'type': 'no_errors', 
            'format': bold_border_l
        })
        # bottom bold
        worksheet.conditional_format('B7:T7', {
            'type': 'no_errors', 
            'format': bold_border_b
        })
        # top bold
        worksheet.conditional_format('B25:T25', {
            'type': 'no_errors', 
            'format': bold_border_t
        })
    
    
    
def summary_sheet(workbook, year, month, employees, common_cell, common_cell_time):
    
    worksheet = workbook.add_worksheet('Summary')
    
    #Set Column's Width
    worksheet.set_column(1, 1, 3)
    worksheet.set_column(5, 5, 30)
    
    # calendar with starting sunday 
    cal= calendar.Calendar(6).monthdayscalendar(year,month)
    
    for week in range(0,5):
        # Drawing Border
        for co in range(0, 23):
            for ro in range(0, 19):
                worksheet.write(7+ro+(week*20), 1+co, '', common_cell)
        
        worksheet.merge_range('B{}:C{}'.format(8+20*week, 10+20*week), 'Week #',common_cell)
        worksheet.merge_range('D{}:D{}'.format(8+20*week, 10+20*week), 'No.',common_cell)
        worksheet.merge_range('E{}:E{}'.format(8+20*week, 10+20*week), 'Level',common_cell)
        worksheet.merge_range('F{}:F{}'.format(8+20*week, 10+20*week), 'Name',common_cell)
        worksheet.merge_range('U{}:X{}'.format(8+20*week, 9+20*week), 'Total',common_cell)
        
        worksheet.merge_range('B{}:C{}'.format( 11+ 20*week, 25+20*week), 'Week #{}'.format(week+1), common_cell)
        worksheet.merge_range('B{}:E{}'.format( 26+ 20*week, 26+20*week), '', common_cell)
        worksheet.write(25+20*week,5,'Total Hours per Week',common_cell)
        
        # each employee in a week
        for idx, employee in enumerate(employees):
            worksheet.write(10 + idx + 20*week, 5, employee.get('name',''), common_cell)
            
            for i in range(0,7):
                # Daily Office Hour
                worksheet.write( 10+idx + 20*week, 6 + 2*i, "='{}'!N{}".format(cal[week][i], 10 + idx) if cal[week][i] != 0 else '', common_cell_time )
                # Daily Trevel Hour
                worksheet.write( 10+idx + 20*week, 7 + 2*i, "='{}'!O{}".format(cal[week][i], 10 + idx) if cal[week][i] != 0 else '', common_cell_time )
            
            # total office
            worksheet.write(10 + 20*week, 20, "=G{n}+I{n}+K{n}+M{n}+O{n}+Q{n}+S{n}".format(n=11+20*week), common_cell)
            # Travel office
            worksheet.write(10 + 20*week, 21, "=H{n}+J{n}+L{n}+N{n}+P{n}+R{n}+T{n}".format(n=11+20*week), common_cell)
            
            # total office Unit
            worksheet.write(10 + 20*week, 22, "=IF((U{n})*24<0,24+(U{n})*24,(U{n})*24)".format(n=11+20*week), common_cell)
            # total Travel Unit
            worksheet.write(10 + 20*week, 22, "=IF((V{n})*24<0,24+(V{n})*24,(V{n})*24)".format(n=11+20*week), common_cell)
            
        
        for i in range(0,7):
            # write day
            worksheet.merge_range('{}{}:{}{}'.format(alphabet[6+2*i], 8+20*week, alphabet[7+2*i], 8+20*week), days[i], common_cell)
            # write date
            worksheet.merge_range('{}{}:{}{}'.format(alphabet[6+2*i], 9+20*week, alphabet[7+2*i], 9+20*week), '{:02d}.{:02d}'.format(month,cal[week][i]) if cal[week][i] != 0 else '', common_cell)
            
            worksheet.write( 9 + 20*week , 6 + 2*i, 'Office', common_cell)
            worksheet.write( 9 + 20*week , 7 + 2*i, 'Travel', common_cell)
            
            # total office total
            worksheet.write( 25 + 20*week , 6 + 2*i, '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[6+2*i], st = 11 + 20*week, ed = 25 + 20*week), common_cell_time)
            # total trevel total
            worksheet.write( 25 + 20*week , 7 + 2*i, '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[7+2*i], st = 11 + 20*week, ed = 25 + 20*week), common_cell_time)
            
        
        worksheet.write( 9 + 20*week , 20, 'Office', common_cell)
        worksheet.write( 9 + 20*week , 21, 'Travel', common_cell)
        worksheet.write( 9 + 20*week , 22, 'Office Unit', common_cell)
        worksheet.write( 9 + 20*week , 23, 'Travel Unit', common_cell)
        
        worksheet.write( 25 + 20*week , 20 , '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[20], st = 11 + 20*week, ed = 25 + 20*week), common_cell)
        worksheet.write( 25 + 20*week , 21 , '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[21], st = 11 + 20*week, ed = 25 + 20*week), common_cell)
        # total offce unit total
        worksheet.write( 25 + 20*week , 22 , '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[22], st = 11 + 20*week, ed = 25 + 20*week), common_cell)
        # total travel unit total
        worksheet.write( 25 + 20*week , 23 , '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[23], st = 11 + 20*week, ed = 25 + 20*week), common_cell)
        
        # Fill in No
        for n in range(1, 16):
            worksheet.write( n + 9 + 20*week, 3, n, common_cell)
    


    