from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from projectv2.main import parsesingle, parselist
from xlwt import Workbook

# the purpose of this file is to set the view of the web page
# the methods are the controller of the web page


# the purpose of this method is to deal with the input from input box one
# the method get the input and send to the infobox crawler
def search_post(request):
    ctx = {}
    # get the request and send to the parse method
    if request.POST:
        query = request.POST['q']
        message = parsesingle(query)
    else:
        message = ''
    ctx['dict'] = message
    # return the web page
    return render(request, "index.html", ctx)


# the purpose of this method is to deal with the input from input box two
# the method get the input, retrieve the input in the database and yield an file with all the information
def download(request):
    if request.GET:
        query = request.GET['l']
        workbook = parselist(query)
    else:
        workbook = " "
    # check whether the workbook is null
    if isinstance(workbook,Workbook):
        filename = "file.xls"
        response = HttpResponse(content_type='application/vnd.ms-excel')
        # yield the response
        response['Content-Disposition'] = 'attachment; filename=' + filename
        workbook.save(response)
        return response
    else:
        return render_to_response('notfound.html')

