from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import io
import copy
from django.http.response import HttpResponse
import datetime, pytz, calendar, string, logging



from .models import Test
from xlsxwriter.workbook import Workbook



# Main Page
def index(request):
    
    # test_list = Test.objects.order_by('name').distinct('name')
    test_list = Test.objects.values('projname','pid').distinct()
    template = loader.get_template('xlsx/listView.html')
    context = {
        'test_list': test_list,
        'year_range' : range(2017,2019),
        'month_range' : range(1,13)
    }
    return HttpResponse(template.render(context, request))


alphabet = list(string.ascii_uppercase)
days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    

# Extract EXCEL
def xlsxbymonth(request):
    # For column
    output = io.BytesIO()
    
    # Get Data with POST
    year = int(request.POST.get('year'))
    month = int(request.POST.get('month'))
    pid = int(request.POST.get('pid'))
    
    # Check Month's End date
    month_end = calendar.monthrange(year, month)[1]
    
    # Create New Excel File
    workbook = Workbook(output, {'in_memory': True})
    
    # by date range
    test_list = Test.objects.filter(pid = pid, cdate__range = [datetime.date( year, month , 1), datetime.date( year, month ,month_end)]).order_by('name')
    test_list_temp = Test.objects.filter(pid = pid)
    # Sorting Employees through eliminating duplicated employee ( In django, distinct query is not affordable for mysql DB )
    employees = test_list.values('name','epid', 'level').distinct()
    
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
        'num_format': '[h]:mm;-0;;@'
    })
    
      
    # 
    # Create daily SHEET
    #
    daily_sheet(workbook, year, month, month_end, test_list, employees, common_cell, common_cell_time, test_list_temp)
    #
    # Create Summary SHEET
    #
    # summary_sheet(workbook, year, month, month_end, test_list, employees, common_cell, common_cell_time, test_list_temp)
    #
    # Create Monthly Summary SHEET
    #
    # monthly_summary_sheet(workbook, year, month, month_end, test_list, employees, common_cell, common_cell_time, test_list_temp)
        
        
    workbook.close()
    output.seek(0)
    
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename={}.xlsx".format(datetime.datetime.now())
    
    
    return response
    
    
# for calculate Lunch Or Dinner Hour
def minute_interval(start, end):
    reverse = False
    
    if start > end:
        start, end = end, start
        reverse = True
    
    delta = (end.hour - start.hour)*3600 + (end.minute - start.minute)*60 + end.second - start.second
    
    if reverse:
        delta = 24*3600 - delta
    # return type is int and seconds
    return delta
    
def time_format(seconds):
    # recieved time is seconds
    if seconds != 0:
        time_format = '{:02d}:{:02d}'.format(int(seconds//3600), int((seconds%3600)//60))
    else:
        time_format = ''
    return time_format
    

#Function Make Daily Sheet
def daily_sheet(workbook, year, month, month_end, test_list, employees, common_cell, common_cell_time, test_list_temp):
    
    # From month's start to end
    # for day in range(1,month_end+1):
    for day in range(1,5): 
        # Create sheet
        worksheet = workbook.add_worksheet('{}'.format(day))
        
        # Set column's width
        worksheet.set_column(0, 0, 3)
        worksheet.set_column(4, 4, 40)
        worksheet.set_column(5, 15, 9)
        
        # Cells' Styles
        
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
        
        # Write Title of sheet
        title = "BTI Solutions : WorkingTime Card"
        write_title(title, 2, workbook, worksheet, month, month_end, year, test_list, test_list_temp)
        
        
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
        
        
        for idx in range(0, 15):
            # Fill in No
            worksheet.write( 9+idx, 2, str(idx + 1) , common_cell)
            # Write total office
            worksheet.write(9+idx,13, '=G{row}-F{row}-H{row}-I{row}'.format(row = 10+idx),common_cell_time)
            # Write total business trip
            worksheet.write(9+idx,14, '=K{row}-J{row}-L{row}-M{row}'.format(row = 10+idx),common_cell_time)
            # Write Total Hours
            worksheet.write_formula('P{}'.format(10+idx), '=N{}+O{}'.format(10+idx,10+idx), common_cell_time)
        
        # Write per each Employee
        tests = test_list.filter(cdate = datetime.date(year, month, day))
        for idx, employee in enumerate(employees):
            
            logging.warning("in enumerate(employees) Day : "+ str(day) + " idx : " + str(idx))
            # write name
            worksheet.write(9+idx, 4, employee.get('name'), cell_bold_r)
            # write level
            worksheet.write(9+idx, 3, employee.get('level'), common_cell)
            
            # If there is a employee who worked
            # if tests.filter(epid = employee.get('epid')) :
            # If true then Employee worked Or False then Employee didn't work
            work = tests.filter(epid = employee.get('epid'))
            if work :
                
                startday = work.order_by('startday').first().startday
                endday = work.order_by('startday').first().endday
                lunch_hour = 0
                dinner_hour = 0
                
                for test in work.order_by('startday'):
                    logging.warning("in work.order_by('startday') test.epid : " + str(test.epid))
                    # emp = tests.filter(epid = employee.get('epid')).first()
                    startday = test.startday if test.startday < startday else startday
                    dinner_hour += (test.startday - endday).total_seconds() if test.startday > endday else 0
                    endday = test.endday
                    
                    lunch_hour += minute_interval(test.startlunch, test.endlunch) if test.startlunch else 0
                    dinner_hour += minute_interval(test.startdinner,test.enddinner) if test.startdinner else 0
    
                    # #
                    # #BUSINESS TRIP
                    # #
                    # # start day
                    # worksheet.write(9+idx, 9, emp.startday.time().strftime('%H:%M') if emp.startday.time() != datetime.time(0,0) else '', common_cell)
                    # # end day
                    # worksheet.write(9+idx, 10, emp.endday.time().strftime('%H:%M') if emp.endday.time() != datetime.time(0,0) else '' , common_cell)
                    # # caculate lunch hour
                    # lunch_hour = minute_interval( emp.startlunch, emp.endlunch)
                    # # Lunch hour
                    # worksheet.write(9+idx, 11, time_format(lunch_hour), common_cell)
                    # # caculate Dinner hour
                    # dinner_hour = minute_interval( emp.startdinner, emp.enddinner)
                    # # Dinner hour
                    # worksheet.write(9+idx, 12, time_format(dinner_hour), common_cell)
                
                # start day
                worksheet.write(9+idx, 5, startday.time().strftime('%H:%M'), common_cell)
                # end day
                worksheet.write(9+idx,6, endday.time().strftime('%H:%M'), common_cell)
                # Lunch hour
                worksheet.write(9+idx,7, time_format(lunch_hour), common_cell)
                
                # Dinner hour
                worksheet.write(9+idx,8, time_format(dinner_hour), common_cell)
                # Write model
                worksheet.write('Q{}'.format(10+idx), work.first().model, common_cell)
                # Write Version
                worksheet.write('R{}'.format(10+idx), work.first().version, common_cell)
                # Write testitem
                worksheet.write('S{}'.format(10+idx), work.first().testitem, common_cell)



    
    
    
def summary_sheet(workbook, year, month, month_end, test_list, employees, common_cell, common_cell_time, test_list_temp):
    
    worksheet = workbook.add_worksheet('Summary')
    
    #Set Column's Width
    worksheet.set_column(1, 1, 3)
    worksheet.set_column(5, 5, 30)
    
    # calendar with starting sunday 
    cal= calendar.Calendar(6).monthdayscalendar(year,month)
    
    total_unit_cell = workbook.add_format({
        'valign':'vcenter',
        'align':'center',
        'right':1,
        'top':1,
        'left':1,
    })
    total_unit_cell.set_num_format('0.00;-0;;@')
    
    write_title("BTI Solutions : WorkingTime Card", 2, workbook, worksheet, month, month_end, year, test_list, test_list_temp)
    
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
        
        # # each employee in a week
        # for idx, employee in enumerate(employees):
        #     # Write name
        #     worksheet.write(10 + idx + 20*week, 5, employee.get('name',''), common_cell)
        #     # Write level
        #     worksheet.write(10 + idx + 20*week, 4, '=IF(\'1\'!E{n}<>\"\",\'1\'!E{n},\"\")'.format(n=10+idx), common_cell_time)
            
            
        #     for i in range(0,7):
        #         # Daily Office Hour
        #         worksheet.write( 10+idx + 20*week, 6 + 2*i, "='{}'!N{}".format(cal[week][i], 10 + idx) if cal[week][i] != 0 else '', common_cell_time )
        #         # Daily Trevel Hour
        #         worksheet.write( 10+idx + 20*week, 7 + 2*i, "='{}'!O{}".format(cal[week][i], 10 + idx) if cal[week][i] != 0 else '', common_cell_time )
            
            
            
        #     # total office
        #     # worksheet.write(10 + 20*week, 20, "=G{n}+I{n}+K{n}+M{n}+O{n}+Q{n}+S{n}".format(n=11+20*week), common_cell_time)
            
        #     worksheet.write(10 + 20*week + idx, 20, "={alphabet[6]}{n}+{alphabet[8]}{n}+{alphabet[10]}{n}+{alphabet[12]}{n}+{alphabet[14]}{n}+{alphabet[16]}{n}+{alphabet[18]}{n}".format(n= 11 + 20*week + idx, alphabet = alphabet), common_cell_time)
        #     # Travel office
        #     worksheet.write(10 + 20*week + idx, 21, "={alphabet[7]}{n}+{alphabet[9]}{n}+{alphabet[11]}{n}+{alphabet[13]}{n}+{alphabet[15]}{n}+{alphabet[17]}{n}+{alphabet[19]}{n}".format(n= 11 + 20*week + idx, alphabet = alphabet), common_cell_time)
            
        #     # total office Unit
        #     worksheet.write(10 + 20*week + idx, 22, "=IF((U{n})*24<0,24+(U{n})*24,(U{n})*24)".format(n=11+20*week), common_cell_time)
        #     # total Travel Unit
        #     worksheet.write(10 + 20*week + idx, 23, "=IF((V{n})*24<0,24+(V{n})*24,(V{n})*24)".format(n=11+20*week), common_cell_time)
            
        
        for i in range(0,7):
            # write day
            worksheet.merge_range('{}{}:{}{}'.format(alphabet[6+2*i], 8+20*week, alphabet[7+2*i], 8+20*week), days[i], common_cell)
            # write date
            worksheet.merge_range('{}{}:{}{}'.format(alphabet[6+2*i], 9+20*week, alphabet[7+2*i], 9+20*week), '{:02d}.{:02d}'.format(month,cal[week][i]) if cal[week][i] != 0 else '', common_cell)
            
            worksheet.write( 9 + 20*week , 6 + 2*i, 'Office', common_cell)
            worksheet.write( 9 + 20*week , 7 + 2*i, 'Travel', common_cell)
            
            # total hours per week : office total
            worksheet.write( 25 + 20*week , 6 + 2*i, '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[6+2*i], st = 11 + 20*week, ed = 25 + 20*week), common_cell_time)
            # total hours per week : trevel total
            worksheet.write( 25 + 20*week , 7 + 2*i, '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[7+2*i], st = 11 + 20*week, ed = 25 + 20*week), common_cell_time)
            
            for j in range(0, 15):
                
                # Fill in No
                worksheet.write(10 + j + 20*week, 3, str(j+1), common_cell)
                # Fill level
                worksheet.write(10 + j + 20*week, 4, '=IF(\'1\'!D{n}<>\"\",\'1\'!D{n},\"\")'.format(n=10+j), common_cell)
                # Fill Name
                worksheet.write(10 + j + 20*week, 5, '=IF(\'1\'!E{n}<>\"\",\'1\'!E{n},\"\")'.format(n=10+j), common_cell)
                
                # write daily office hour
                worksheet.write( 10 + j + 20*week, 6 + 2*i, '=\'{}\'!N{}'.format(cal[week][i], 10+j) if cal[week][i] != 0 else '', common_cell_time)
                # write daily travel hour
                worksheet.write( 10 + j + 20*week, 7 + 2*i, '=\'{}\'!O{}'.format(cal[week][i], 10+j) if cal[week][i] != 0 else '', common_cell_time)
                # total office
                # worksheet.write(10 + 20*week, 20, "=G{n}+I{n}+K{n}+M{n}+O{n}+Q{n}+S{n}".format(n=11+20*week), common_cell_time)
                
                worksheet.write(10 + j + 20*week, 20, "={alphabet[6]}{n}+{alphabet[8]}{n}+{alphabet[10]}{n}+{alphabet[12]}{n}+{alphabet[14]}{n}+{alphabet[16]}{n}+{alphabet[18]}{n}".format(n= 11 + 20*week + j, alphabet = alphabet), common_cell_time)
                # Travel office
                worksheet.write(10 + j + 20*week, 21, "={alphabet[7]}{n}+{alphabet[9]}{n}+{alphabet[11]}{n}+{alphabet[13]}{n}+{alphabet[15]}{n}+{alphabet[17]}{n}+{alphabet[19]}{n}".format(n= 11 + 20*week + j, alphabet = alphabet), common_cell_time)
                
                # total office Unit
                worksheet.write(10 + j + 20*week, 22, "=IF((U{n})*24<0,24+(U{n})*24,(U{n})*24)".format(n=11+20*week + j), total_unit_cell)
                # total Travel Unit
                worksheet.write(10 + j + 20*week, 23, "=IF((V{n})*24<0,24+(V{n})*24,(V{n})*24)".format(n=11+20*week + j), total_unit_cell)
                
        
        worksheet.write( 9 + 20*week , 20, 'Office', common_cell)
        worksheet.write( 9 + 20*week , 21, 'Travel', common_cell)
        worksheet.write( 9 + 20*week , 22, 'Office Unit', common_cell)
        worksheet.write( 9 + 20*week , 23, 'Travel Unit', common_cell)
        
        # total Office
        worksheet.write( 25 + 20*week , 20 , '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[20], st = 11 + 20*week, ed = 25 + 20*week), common_cell_time)
        # total Travel
        worksheet.write( 25 + 20*week , 21 , '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[21], st = 11 + 20*week, ed = 25 + 20*week), common_cell_time)
        # total offce unit's total
        worksheet.write( 25 + 20*week , 22 , '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[22], st = 11 + 20*week, ed = 25 + 20*week), common_cell)
        # total travel unit's total
        worksheet.write( 25 + 20*week , 23 , '=SUM({alp}{st}:{alp}{ed})'.format(alp = alphabet[23], st = 11 + 20*week, ed = 25 + 20*week), common_cell)
        

       
def monthly_summary_sheet(workbook, year, month, month_end, test_list, employees, common_cell, common_cell_time, test_list_temp):
    total_unit_cell = workbook.add_format({
        'valign':'vcenter',
        'align':'center',
        'right':1,
        'top':1,
        'left':1,
    })
    total_unit_cell.set_num_format('0.00;-0;;@')
    
    worksheet = workbook.add_worksheet('Monthly Analysis')
    
    #Set Column's Width
    worksheet.set_column(0, 0, 3)
    
    write_title("BTI Solutions: Monthly Working Time Card", 1, workbook, worksheet, month, month_end, year, test_list, test_list_temp)
    
    worksheet.merge_range('B8:B9','Level')
    worksheet.merge_range('C8:C9', 'Name')
        
    for i in range(0, 6):
        worksheet.merge_range('{alphabet1}8:{alphabet2}8'.format(alphabet1 = alphabet[3+2*i], alphabet2 = alphabet[4+2*i]), 'WK{}'.format(i+1))
        worksheet.write( 8, 3 + 2*i, 'Office' )
        worksheet.write( 8, 4 + 2*i, 'Travel' )
    
    worksheet.merge_range('P8:R8','TOTAL')
    worksheet.write( 'P9', 'Office' )
    worksheet.write( 'Q9', 'Travel' )
    worksheet.write( 'R9', 'Total' )
    
    for row in range(0, 15):
        # write level
        worksheet.write( 9 + row, 1, '=Summary!E{}'.format(11 + row), common_cell)
        # write name
        worksheet.write( 9 + row, 2, '=Summary!F{}'.format(11 + row), common_cell)
        for wk in range(0,6):
            # write WK Office Time
            worksheet.write( 9 + row, 3 + 2*wk, '=Summary!W{}'.format(11 + 20*wk + row), total_unit_cell)
            # write WK Travel Time
            worksheet.write( 9 + row, 4 + 2*wk, '=Summary!X{}'.format(11 + 20*wk + row), total_unit_cell)
            
        # Total Office    
        worksheet.write( 9 + row, 15, '=D{n}+F{n}+H{n}+J{n}+L{n}+N{n}'.format(n = 10 + row), total_unit_cell)
        # Total Travel    
        worksheet.write( 9 + row, 16, '=E{n}+G{n}+I{n}+K{n}+M{n}+O{n}'.format(n = 10 + row), total_unit_cell)
        # Total
        worksheet.write( 9 + row, 17, '=P{n}+Q{n}'.format(n = 10 + row), total_unit_cell)
    
    summary_cell = workbook.add_format({
        'valign':'vcenter',
        'align':'center',
        'border' : 1
    })
    summary_cell.set_num_format('_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)')
    
    
    worksheet.write( 'S8', '')
    worksheet.write( 'T8', 'Office',summary_cell)
    worksheet.write( 'U8', 'Travel',summary_cell)
    worksheet.write( 'V8', 'Total',summary_cell)
    worksheet.write( 'S9', 'Manager',summary_cell)
    worksheet.write( 'T9', '=SUMIF(B10:B173,"Mg",P10:P173)',summary_cell)
    worksheet.write( 'U9', '=SUMIF(B10:B173,"Mg",Q10:Q173)',summary_cell)
    worksheet.write( 'V9', '=SUMIF(B10:B173,"Mg",R10:R173)',summary_cell)
    worksheet.write( 'S10', 'Senior',summary_cell)
    worksheet.write( 'T10', '=SUMIF(B10:B173,"Sr",P10:P173)',summary_cell)
    worksheet.write( 'U10', '=SUMIF(B10:B173,"Sr",Q10:Q173)',summary_cell)
    worksheet.write( 'V10', '=SUMIF(B10:B173,"Sr",R10:R173)',summary_cell)
    worksheet.write( 'S11', 'Engineer',summary_cell)
    worksheet.write( 'T11', '=SUMIF(B10:B173,"Jr",P10:P173)',summary_cell)
    worksheet.write( 'U11', '=SUMIF(B10:B173,"Jr",Q10:Q173)',summary_cell)
    worksheet.write( 'V11', '=SUMIF(B10:B173,"Jr",R10:R173)',summary_cell)
    worksheet.write( 'S12', 'Driver',summary_cell)
    worksheet.write( 'T12', '=SUMIF(B10:B173,"Dr",P10:P173)',summary_cell)
    worksheet.write( 'U12', '=SUMIF(B10:B173,"Dr",Q10:Q173)',summary_cell)
    worksheet.write( 'V12', '=SUMIF(B10:B173,"Dr",R10:R173)',summary_cell)
    worksheet.write( 'S13', 'Total',summary_cell)
    worksheet.write( 'T13', '=SUM(T9:T12)',summary_cell)
    worksheet.write( 'U13', '=SUM(U9:U12)',summary_cell)
    worksheet.write( 'V13', '=SUM(V9:V12)',summary_cell)
    
    
    
    
    
    
def write_title(title, line, workbook, worksheet, month, month_end, year, test_list, test_list_temp):
    # Write Title of sheet
    
    sheet_title = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'bold': True,
        'border' : 1
    })
    
    worksheet.merge_range('B2:V2', title, sheet_title)
    #
    # Title of First Line
    #
    # Write Title Month
    worksheet.merge_range('B3:D3', 'Month',sheet_title)
    worksheet.merge_range('B4:D4', '{month}-1-{year} ~ {month}-{month_end}-{year}'.format(month = month, month_end = month_end, year = year), sheet_title)
    
    # Write Title Project Team
    worksheet.merge_range('E3:G3', 'Project Team', sheet_title)
    worksheet.merge_range('E4:G4', test_list_temp.first().projname , sheet_title)
    
    # Write Title Samsung Manager
    worksheet.merge_range('H3:L3', 'Samsung Manager(P/L)', sheet_title)
    worksheet.merge_range('H4:L4', '' , sheet_title)
    
    # Write Title Location Main Manager
    worksheet.merge_range('M3:Q3', 'Location Main Manager(P/L)', sheet_title)
    worksheet.merge_range('M4:Q4', '' , sheet_title)
    
    # Write Title Location Sub Manager
    worksheet.merge_range('R3:T3', 'Location Sub Manager', sheet_title)
    worksheet.merge_range('R4:T4', '' , sheet_title)
    
    
    if line == 2:
        #
        # Title of Second Line
        #
        # Write Title Month
        worksheet.merge_range('B5:D5', 'BTI Solutions [Leader]',sheet_title)
        worksheet.merge_range('B6:D6', test_list_temp.first().pmname, sheet_title)
        
        # Write Title Project Team
        worksheet.merge_range('E5:G5', 'Location', sheet_title)
        worksheet.merge_range('E6:G6', test_list_temp.first().loname , sheet_title)
        
        # Write Title Samsung Manager
        worksheet.merge_range('H5:L5', 'E-mail / Phone Number', sheet_title)
        worksheet.merge_range('H6:L6', '' , sheet_title)
        
        # Write Title Location Main Manager
        worksheet.merge_range('M5:Q5', 'E-mail / Phone Number', sheet_title)
        worksheet.merge_range('M6:Q6', '' , sheet_title)
        
        # Write Title Location Sub Manager
        worksheet.merge_range('R5:T5', 'E-mail / Phone Number', sheet_title)
        worksheet.merge_range('R6:T6', '' , sheet_title)
    
    

    