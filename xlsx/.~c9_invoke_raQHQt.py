from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import io

from django.http.response import HttpResponse
import datetime, calendar, string



from .models import Test
from xlsxwriter.workbook import Workbook

# Create your views here.
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

    year = request.POST.get('year')
    month = request.POST.get('month')
    month_range = calendar.monthrange(int(year), int(month))
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    workbook = Workbook(output, {'in_memory': True})
    test_list = Test.objects.filter(epid = request.POST.get('epid'), date__range=[startdate, enddate]).order_by('date')
    
    for day in range(month_range[0],month_range[1]+1): 
        worksheet = workbook.add_worksheet('{}'.format(day))
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
    alphabet = list(string.ascii_uppercase)
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    output = io.BytesIO()

    year = int(request.POST.get('year'))
    month = int(request.POST.get('month'))
    month_end = calendar.monthrange(year, month)[1]
    
    workbook = Workbook(output, {'in_memory': True})
    test_list = Test.objects.filter(date__range = [datetime.date( year, month , 1), datetime.date( year, month ,month_end)]).order_by('name')
    employees = test_list.values('name','epid').distinct()

    common_cell = workbook.add_format({
        'valign':'vcenter',
        'align':'center',
        'right':1,
        'top':1,
        'left':1,
        'num_format': '[h]:mm;-0;;@'
      })
    
    common_cell_num = workbook.add_format({
        'valign':'vcenter',
        'align':'center',
        'right':1,
        'top':1,
        'left':1
      })
      
    for day in range(1,month_end+1): 
        worksheet = workbook.add_worksheet('{}'.format(day))
        worksheet.set_column(0, 0, 3)
        worksheet.set_column(4, 4, 40)
        worksheet.set_column(5, 15, 9)
        
        title = workbook.add_format({
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
        
        border = workbook.add_format({
            'border': 1
        })
        
        cell_bold_r = workbook.add_format({
            'top':1,
            'right':2,
            'left': 1,
            'bottom':1
        })
        date_cell = workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'border': 1
            })
            
        bold_cell = workbook.add_format({
            'align':'center',
            'right':2,
            'top':1,
            'left':1,
            'num_format': '[h]:mm;-0;;@'
        })
          
        bold_time_cell = workbook.add_format({
            'align':'center',
            'right':2,
            'top':1,
            'left':1,
            'num_format': '[h]:mm;-0;;@'
        })
        
        common_time_cell = workbook.add_format({
            'align':'center',
            'right':1,
            'top':1,
            'left':1,
            'num_format': '[h]:mm;-0;;@'
        })
        
        for c in range(1, 20):
            for r in range(7, 24):
                worksheet.write(r, c, '', border)
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
                
        
        
        worksheet.merge_range('B2:V2', 'BTI Solutions : WorkingTime Card',title)
        
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
            worksheet.write(9+idx, 4, employee.get('name'), bold_cell)
            
            if tests.filter(epid = employee.get('epid')) :
                worksheet.write(9+idx, 5, str(tests.get(epid = employee.get('epid')).startday), common_time_cell)
            
                worksheet.write(9+idx,6,str(tests.get(epid = employee.get('epid')).endday), common_time_cell)
            
                lunch_hour = minute_interval(tests.get(epid = employee.get('epid')).startlunch, tests.get(epid = employee.get('epid')).endlunch)
            
                day_hour = minute_interval(tests.get(epid = employee.get('epid')).startday, tests.get(epid = employee.get('epid')).endday)
            
            
                worksheet.write(9+idx,7,str(time_format(lunch_hour)),common_time_cell)
                worksheet.write(9+idx,13,str(time_format(day_hour-lunch_hour)),common_time_cell)
            
                worksheet.write_formula('P{}'.format(10+idx), '=N{}+O{}'.format(10+idx,10+idx), bold_time_cell)
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
        
        
        # worksheet.conditional_format('B8:T24', {
        #     'type': 'no_errors', 
        #     'format': border
        # })
        
        # worksheet.conditional_format('A8:A24,E8:E24,I8:I24,M8:M24,P8:P24,T8:T24', {
        #     'type': 'no_errors', 
        #     'format': bold_border_r
        # })
        
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
        # worksheet.conditional_format('E8:E24', {
        #     'type': 'no_errors', 
        #     'format': bold_border_r
        # })
        # worksheet.conditional_format('I9:I24', {
        #     'type': 'no_errors', 
        #     'format': bold_border_r
        # })
        # worksheet.conditional_format('M10:M24', {
        #     'type': 'no_errors', 
        #     'format': bold_border_r
        # })
        # worksheet.conditional_format('T10:E24', {
        #     'type': 'no_errors', 
        #     'format': bold_border_r
        # })
        # worksheet.conditional_format('B7:T7', {
        #     'type': 'no_errors', 
        #     'format': bold_border_b
        # })
        # worksheet.write_blank ('B8', '', bold_border_lr)
        # worksheet.conditional_format('A8:A24,E8:E24,I8:I24,M8:M24,P8:P24T8:T24', {
        #     'type': 'no_errors', 
        #     'format': bold_border_r
        # })
        # worksheet.conditional_format('A8:A24,E8:E24,I8:I24,M8:M24,P8:P24T8:T24', {
        #     'type': 'no_errors', 
        #     'format': bold_border_r
        # })
        
    
    
    worksheet = workbook.add_worksheet('Summary')
    
    worksheet.set_column(1, 1, 3)
    # Name Collumn Width
    worksheet.set_column(5, 5, 30)

    

    
    # calendar with starting sunday 
    cal= calendar.Calendar(6).monthdayscalendar(year,month)
    
    # lunch_hour = minute_interval(test.startlunch, test.endlunch)
    # day_hour = minute_interval(test.startday, test.endday)
    # worksheet.write(9+idx,7,str(time_format(lunch_hour)),common_time_cell)
    # worksheet.write(9+idx,13,str(time_format(day_hour-lunch_hour)),common_time_cell)

    
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
        
        
        for idx, employee in enumerate(employees):
            worksheet.write(10 + idx + 20*week, 5, employee.get('name',''), common_cell)
            
            for i in range(0,7):
                # Daily Office Hour
                worksheet.write( 10+idx + 20*week, 6 + 2*i, "='{}'!N{}".format(cal[week][i], 10 + idx) if cal[week][i] != 0 else '', common_cell )
                # Daily Trevel Hour
                worksheet.write( 10+idx + 20*week, 7 + 2*i, "='{}'!O{}".format(cal[week][i], 10 + idx) if cal[week][i] != 0 else '', common_cell )
            
            # total office
            worksheet.write(10 + 20*week, 20, "=G{n}+I{n}+K{n}+M{n}+O{n}+Q{n}+S{n}".format(n=11+20*week), common_cell)
            # Travel office
            worksheet.write(10 + 20*week, 21, "=H{n}+J{n}+L{n}+N{n}+P{n}+R{n}+T{n}".format(n=11+20*week), common_cell)
            
            # total office Unit
            worksheet.write(10 + 20*week, 22, "=IF((U{n})*24<0,24+(U{n})*24,(U{n})*24)".format(n=11+20*week), common_cell)
            # total Travel Unit
            worksheet.write(10 + 20*week, 22, "=IF((V{n})*24<0,24+(V{n})*24,(V{n})*24)".format(n=11+20*week), common_cell)
            
        
        for i in range(0,7):
            worksheet.merge_range('{}{}:{}{}'.format(alphabet[6+2*i], 8+20*week, alphabet[7+2*i], 8+20*week), days[i], common_cell)
            worksheet.merge_range('{}{}:{}{}'.format(alphabet[6+2*i], 9+20*week, alphabet[7+2*i], 9+20*week), '{:02d}.{:02d}'.format(month,cal[week][i]) if cal[week][i] != 0 else '', common_cell)
            
            worksheet.write( 9 + 20*week , 6 + 2*i, 'Office', common_cell)
            worksheet.write( 9 + 20*week , 7 + 2*i, 'Travel', common_cell)
            
            # total office total
            worksheet.write( 25 + 20*week , 6 + 2*i, '=SUM({alp}11:{alp}25)'.format(alp = alphabet[6+2*i]), common_cell)
            # total trevel total
            worksheet.write( 25 + 20*week , 7 + 2*i, '=SUM({alp}11:{alp}25)'.format(alp = alphabet[7+2*i]), common_cell)

            

            # worksheet.write( 10+20*week, 10, '='3'!N10')        
            # worksheet.write( 10+20*week, 12, '='4'!N10')        
            # worksheet.write( 10+20*week, 14, '='5'!N10')        
            # worksheet.write( 10+20*week, 16, '='6'!N10')        
            # worksheet.write( 10+20*week, 1, '='7'!N10')        
            
        
        worksheet.write( 9 + 20*week , 20, 'Office', common_cell)
        worksheet.write( 9 + 20*week , 21, 'Travel', common_cell)
        worksheet.write( 9 + 20*week , 22, 'Office Unit', common_cell)
        worksheet.write( 9 + 20*week , 23, 'Travel Unit', common_cell)
        
        worksheet.write( 25 + 20*week , 20 + 2*i, '=SUM({alp}11:{alp}25)'.format(alp = alphabet[20]), common_cell)
        worksheet.write( 25 + 20*week , 21 + 2*i, '=SUM({alp}11:{alp}25)'.format(alp = alphabet[21]), common_cell)
        # total offce unit total
        worksheet.write( 25 + 20*week , 22 + 2*i, '=SUM({alp}11:{alp}25)'.format(alp = alphabet[22]), common_cell)
        # total travel unit total
        worksheet.write( 25 + 20*week , 23 + 2*i, '=SUM({alp}11:{alp}25)'.format(alp = alphabet[23]), common_cell)
        
        # Fill in No
        for n in range(1, 16):
            worksheet.write( n + 9 + 20*week, 3, n, common_cell_num)
        
        
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
    time_format = '{:02d}:{:02d}'.format(int(time//60), int(time%60))
    return time_format
    
def add_to_format(existing_format, dict_of_properties, workbook):
    # """Give a format you want to extend and a dict of the properties you want to
    # extend it with, and you get them returned in a single format"""
    new_dict={}
    for key, value in existing_format.__dict__.iteritems():
        if (value != 0) and (value != {}) and (value != None):
            new_dict[key]=value
    del new_dict['escapes']

    return(workbook.add_format(dict(new_dict.items() + dict_of_properties.items())))
    
    
def box(workbook, sheet_name, row_start, col_start, row_stop, col_stop):
    """Makes an RxC box. Use integers, not the 'A1' format"""

    rows = row_stop - row_start + 1
    cols = col_stop - col_start + 1

    for x in range((rows) * (cols)): # Total number of cells in the rectangle

        box_form = workbook.add_format()   # The format resets each loop
        row = row_start + (x // cols)
        column = col_start + (x % cols)

        if x < (cols):                     # If it's on the top row
            box_form = add_to_format(box_form, {'top':2}, workbook)
        if x >= ((rows * cols) - cols):    # If it's on the bottom row
            box_form = add_to_format(box_form, {'bottom':2}, workbook)
        if x % cols == 0:                  # If it's on the left column
            box_form = add_to_format(box_form, {'left':2}, workbook)
        if x % cols == (cols - 1):         # If it's on the right column
            box_form = add_to_format(box_form, {'right':2}, workbook)

        sheet_name.write(row, column, "", box_form)