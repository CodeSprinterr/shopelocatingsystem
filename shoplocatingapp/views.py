from .models import Area, Shopdata,Item
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render ,redirect
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.core.files.storage import FileSystemStorage
from shoplocatingsystem.settings import EMAIL_HOST_USER
from django.core.mail import send_mail



# Create your views here.
def searchbyarea(request):
    if request.COOKIES.get('state') and request.COOKIES.get('city') and request.COOKIES.get('district'): 
        if  'state' in request.GET: 
            statename = request.GET.get('state')
            districtname = request.GET.get('district')
            cityname = request.GET.get('city1')
            areaname = request.GET.get('area')
            qs = Shopdata.objects.filter(shoparea =areaname,shopstate=statename,shopcity=cityname,shopdistrict=districtname).values_list('sid','shopname','shopaddress')
            datalist =list()
            for dt in qs:

                datalist.append(dt)

            return render(request,'searchbyarea.html',{'listdata': datalist,'nameisthere' : "yes" })
        else:
            return render(request,'searchbyarea.html',{'nameisthere' : "no" })
    
    else :
        return render(request,'prepage.html')

def state(request):
    if request.COOKIES.get('state') and request.COOKIES.get('city') and request.COOKIES.get('district'): 
        if 'term' in request.GET:
            qs = Area.objects.filter(state__istartswith=request.GET.get('term')).values_list('state', flat=True).distinct()
            state = list()
            for st in qs:
                state.append(st)

            return JsonResponse(state, safe=False)
        return HttpResponse()
    else :
        return render(request,'prepage.html')

@csrf_exempt
def district(request):
    if request.COOKIES.get('state') and request.COOKIES.get('city') and request.COOKIES.get('district'): 
        if request.method == 'POST':
            statename = request.POST['statename']
            qs = Area.objects.filter(state=statename).values_list('district', flat=True).distinct()
            district = list()
            for dt in qs:
                district.append(dt)

            return  JsonResponse(district, safe=False)
    else :
        return render(request,'prepage.html')
    
    
def citylist(request):
    if 'term' in request.GET:        
        qs = Area.objects.filter(city__istartswith=request.GET.get('term'),state =request.GET.get('statedata'),district =request.GET.get('districtdata') ).values_list('city', flat=True).distinct()
        citylist = list()
        for dt in qs:
            citylist.append(dt)
        return JsonResponse(citylist, safe=False)

def arealist(request):
    if 'term' in request.GET:        
        qs = Area.objects.filter(area__istartswith=request.GET.get('term'),state =request.GET.get('statedata'),district =
                                 request.GET.get('districtdata'),city = request.GET.get('citydata') ).values_list('area', flat=True).distinct()
        arealistdata = list()
        for dt in qs:
            arealistdata.append(dt)
        return JsonResponse(arealistdata, safe=False)
    
def displayshop(request):
    if request.COOKIES.get('state') and request.COOKIES.get('city') and request.COOKIES.get('district'): 
        
        if 'id' in request.GET: 
            id1 = request.GET.get("id")
            shopfulldata = Shopdata.objects.filter(sid = id1 ).values_list('shopname','shopimage','shopdesc','shopcontact','shopemail',
                            'shopaddress','shoparea','shopcity','shopdistrict','shopstate','holiday','type').distinct()
            shopda =list(shopfulldata[0])
            itemdata = Item.objects.filter(shopid =id1).values_list('itemname','itemcategory')
            itemlistdata =list()
            for dt in itemdata:
                itemlistdata.append(dt)
            

            return render(request,'displayshop.html',{'data':shopda,'itemlistdata':itemlistdata})
        else :
            return redirect("/")
    else :
        return render(request,'prepage.html')
    
def index(request):
    if request.COOKIES.get('state') and request.COOKIES.get('city') and request.COOKIES.get('district'):
        return render(request,'index.html')
    else :
        return render(request,'prepage.html')


def getlocation(request):
    if 'term' in request.GET:
        qs = Area.objects.filter(city__istartswith=request.GET.get('term')).values_list('city','district','state').distinct()
        city = list()
        for ct,dt,st in qs:
            city.append({"label": ct,"dist":dt,"state":st,"value":ct}) 
        return JsonResponse(city, safe=False)
    return HttpResponse()
def itemlist(request):
    # in development
    if 'term' in request.GET:
        qs = Shopdata.objects.filter(shopcity=request.GET.get('ct'), shopdistrict = request.GET.get('dt'),shopstate =request.GET.get('st') ).values_list('sid',flat = True).distinct()
        id = list()
        for i in qs:
            id.append(i) 
        print(id)
        listitem = Item.objects.filter(itemname__istartswith = request.GET.get('term') ,shopid__in= id).values_list('itemname',flat = True) .distinct()
        it = list()
        for i in listitem:
            it.append(i) 
           
            
        return JsonResponse(it, safe=False)
    return HttpResponse()

def searchbyitem(request):
    if request.COOKIES.get('state') and request.COOKIES.get('city') and request.COOKIES.get('district'):
        if 'itname'and 'state' in request.GET:
            itemname = request.GET.get("itname")
            state = request.GET.get("state")
            district = request.GET.get("district")
            city = request.GET.get("city")
            print(itemname)
            print(state)
            print(district)
            print(city)        
            #qs = Shopdata.objects.filter(shopstate=state,shopcity=city,shopdistrict=district).values_list('sid',flat = True)
            cursor = connection.cursor()
            cursor.execute('''SELECT sid,shopname,shopaddress FROM shopdata sd  INNER JOIN item it  on sd.shopcity= "'''+city+'''" AND sd.shopdistrict = "'''+district+'''"AND sd.shopstate = "'''+state+'''" and it.shopid= sd.sid and it.itemname="'''+itemname+'''"''')
            data = cursor.fetchall()
            listofid =list()

            for i in data: 
                listofid.append(i)  
                
            print(listofid)          

            return render(request,'searchbyitems.html',{'listdata': listofid})


        return render(request,'searchbyitems.html')
    else :
        return render(request,'prepage.html')

def searchbyshop(request):
    if request.COOKIES.get('state') and request.COOKIES.get('city') and request.COOKIES.get('district'):
        if 'shopname' in request.GET:
            sname = request.GET.get('shopname')
            state = request.COOKIES.get('state')
            district = request.COOKIES.get("district")
            city = request.COOKIES.get("city")
            qs = Shopdata.objects.filter(shopname = sname,shopstate = state,shopcity = city,shopdistrict = district).values_list('sid','shopname','shopaddress').distinct()
            listofshop =list()
            for i in qs: 
                listofshop.append(i)  

            return render(request,'searchbyshop.html',{'listdata': listofshop})
        else:
            return render(request,'searchbyshop.html')
    else :
        return render(request,'prepage.html')


def getshopname(request):
    if 'term' in request.GET:
        qs = Shopdata.objects.filter(shopname__istartswith=request.GET.get('term'),shopstate = request.COOKIES.get('state'),shopcity = request.COOKIES.get('city'),shopdistrict = request.COOKIES.get('district') ).values_list('shopname', flat=True)[:30]
        sname = list()
        for dt in qs:
            sname.append(dt)
        
        return  JsonResponse(sname, safe=False)
    return HttpResponse();


    
def about(request):
    if request.COOKIES.get('state') and request.COOKIES.get('city') and request.COOKIES.get('district'):
        return render(request,'about.html')
    else :
        return render(request,'prepage.html')

def contactus(request):
    if request.COOKIES.get('state') and request.COOKIES.get('city') and request.COOKIES.get('district'):
        return render(request,'contactus.html')
    else :
        return render(request,'prepage.html')
    
    
    
    







@csrf_exempt  
def additem(request):
    if 'id'in request.session:
        if request.method == 'POST':
            if Item.objects.filter(shopid = request.POST.get('hiddenid'),itemname =request.POST.get('iname'),itemcategory=request.POST.get('icategory')).exists():
                print("abcd")
                return render(request,'additem.html',{"alertdata":'a'})
            else:
                itemdata = Item(shopid = request.POST.get('hiddenid'),itemname =request.POST.get('iname'),itemcategory=request.POST.get('icategory'))
                itemdata.save()


        
        id = request.session['id']  
        listofitems=list()
        itemdata=Item.objects.filter(shopid=id).values_list('itemname','itemcategory').distinct()
        for i in itemdata:
            listofitems.append(i)

        return render(request,'additem.html',{"id":id,"listofitems":listofitems})
    else:
        return redirect('login')
    
    
def itemdelete(request):
    if 'id'in request.session:
        if 'iname' in request.GET:
            id=request.GET.get('id')
            iname= request.GET.get('iname')
            print(iname)
            qs=Item.objects.filter(itemname =iname,shopid=id).delete()



        id = request.session['id']
        listofitems=list()
        itemdata=Item.objects.filter(shopid=id).values_list('itemname','itemcategory').distinct()
        for i in itemdata:
            listofitems.append(i)

        return render(request,'itemdelete.html',{"id":id,"listofitems":listofitems})
    else:
        return redirect('login')

def itemdeletelist(request):
    if 'term' in request.GET:
        qs=Item.objects.filter(itemname__istartswith=request.GET.get('term'),shopid=request.GET.get('id')).values_list('itemname',flat=True).distinct()
        itemdata=list()
        for i in qs:
            itemdata.append(i)
        return JsonResponse(itemdata,safe=False)

def header(request):
    
    return render(request,'header.html')

def footer(request):

    return render(request,'footer.html')

def itemupdate(request):
    if 'id'in request.session:
        if request.method == 'POST':
            id1=request.POST.get('hiddenid')
            previousname=request.POST.get('iname')
            iname=request.POST.get('updateitem')
            icategory=request.POST.get('iucategory')
            print(id1,iname,icategory)
            Item.objects.filter(shopid=id1,itemname=previousname).update(itemname=iname,itemcategory=icategory)



        
        id = request.session['id']
        listofitems=list()
        itemdata=Item.objects.filter(shopid=id).values_list('itemname','itemcategory').distinct()
        for i in itemdata:
            listofitems.append(i)

        return render(request,'itemupdate.html',{"id":id,"listofitems":listofitems})
    else:
        return redirect('login')
    
def itemupdatelist(request):
    if 'id'in request.session:
        if 'term' in request.GET:
            qs=Item.objects.filter(itemname__istartswith=request.GET.get('term'),shopid=request.GET.get('id')).values_list('itemname','itemcategory').distinct()
            itemdata=list()
            for i,j in qs:
                itemdata.append({"label":i,"itcategory":j,"value":i})
            return JsonResponse(itemdata,safe=False)
    else:
        return redirect('login')


def profileupdate(request):
    if 'id'in request.session:
    
        id = request.session['id']  

        if request.method == 'POST':
            a=request.POST.get('sname')
            b=request.POST.get('hideimg')
            c=request.POST.get('sdesc')
            d=request.POST.get('scontact')
            o=request.POST.get('smail')
            e=request.POST.get('saddress')
            f=request.POST.get('area')
            g=request.POST.get('city1')
            h=request.POST.get('district')
            i=request.POST.get('state')
            j=request.POST.get('sholiday')
            k=request.POST.get('stype')
            m=request.POST.get('spass')


            if a.strip()== ""  or c.strip()=="" or d.strip()=="" or e.strip()=="" or f.strip()=="" or g.strip()=="" or h.strip()=="" or i.strip()=="" or j.strip()=="" or k.strip()==""or o.strip()=="":
                    return render(request,'registration.html',{"alertdata":'b'})

            simage = request.FILES.get('simage',False)
            if simage:
                fs = FileSystemStorage()
                filename = fs.save(simage.name, simage)
                print(filename)
                b=filename
                fs.delete(request.POST.get('hideimg'))

            if Area.objects.filter(area=f,city=g,district=h,state=i).exists():
                    pass
            else:
                return render(request,'registration.html',{"alertdata":'c'})

            if m.strip()=="":
                Shopdata.objects.filter(sid = id).update(shopname=a,shopimage=b,shopdesc=c,shopcontact=d,shopemail=o,shopaddress=e,shoparea=f,shopcity=g,shopdistrict=h,shopstate=i,holiday=j,type=k)
            else:
                Shopdata.objects.filter(sid = id).update(shopname=a,shopimage=b,shopdesc=c,shopcontact=d,shopemail=o,shopaddress=e,shoparea=f,shopcity=g,shopdistrict=h,shopstate=i,holiday=j,type=k,password=m)
            return render(request,'profileupdate.html',{"alertdata":'d'})



        else:
            qs=Shopdata.objects.filter(sid=id).values_list('shopname','shopimage','shopdesc','shopcontact','shopemail','shopaddress','shopstate','shopdistrict','shopcity','shoparea','holiday','type','username')
            listofshopdata = list()
            for i in qs:
                listofshopdata.append(i)
            listofshopdata = list(listofshopdata[0])
            print(listofshopdata)
            return render(request,'profileupdate.html',{"listofshopdata":listofshopdata})
    else:
        return redirect('login')
    
    
    
    
    

def registration(request):  
    
    if request.method == 'POST' and request.FILES['simage']:
        simage = request.FILES['simage']
        if Shopdata.objects.filter(username =request.POST.get('susername')).exists():
            print("abcd")

            return render(request,'registration.html',{"alertdata":'a'})
        else:
           
            fs = FileSystemStorage()
            filename = fs.save(simage.name, simage)
            print(filename)
            a=request.POST.get('sname')
            b=filename
            c=request.POST.get('sdesc')
            d=request.POST.get('scontact')
            o=request.POST.get('smail')
            e=request.POST.get('saddress')
            f=request.POST.get('area')
            g=request.POST.get('city1')
            h=request.POST.get('district')
            i=request.POST.get('state')
            j=request.POST.get('sholiday')
            k=request.POST.get('stype')
            l=request.POST.get('susername')
            m=request.POST.get('spass')
            if a.strip()== "" or b.strip()=="" or c.strip()=="" or d.strip()=="" or e.strip()=="" or f.strip()=="" or g.strip()=="" or h.strip()=="" or i.strip()=="" or j.strip()=="" or k.strip()=="" or l.strip()=="" or m.strip()=="" or o.strip()=="":
                return render(request,'registration.html',{"alertdata":'b'})
            if Area.objects.filter(area=f,city=g,district=h,state=i).exists():
                pass
            else:
                return render(request,'registration.html',{"alertdata":'c'})
            shopnam = Shopdata(shopname=a,shopimage=b,shopdesc=c,shopcontact=d,shopemail=o,shopaddress=e,shoparea=f,shopcity=g,shopdistrict=h,shopstate=i,holiday=j,type=k,username=l,password=m)

            shopnam.save()
            return render(request,'registration.html',{"id":id,"alertdata":'d'})  
    else:
        
        return render(request,'registration.html',{"id":id})  
        
    


def checkmail(request):
    '''
    subject = 'Welcome to apkidukan'
    message = 'Hope you are enjoying this semester'
    recepient = "dhanupharande.4@gmail.com"
    send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    '''
    return HttpResponse()

def login(request):
    if 'id'in request.session:
        del request.session['id']
    if request.method=='POST':
        user1=request.POST['usern']
        pass1=request.POST['passw']
        user=Shopdata.objects.filter(username=user1,password=pass1).exists()

        if user:
            iddata= Shopdata.objects.filter(username=user1,password=pass1).values_list('sid', flat=True)
            
            request.session['id'] =  iddata[0]
            
            return redirect('home')
        else:
            
            return render(request,'login.html',{'a':'a'})
    else:
        return render(request,'login.html')

def forgotpassword(request):
     
    if request.method == 'POST':
        uname=request.POST.get('uname')

        if(Shopdata.objects.filter(username=uname).exists()):
            print("a")
            pass1 = Shopdata.objects.filter(username=uname).values_list('shopemail','password')
            subject = str('Your Password to Login')
            message = str('your password is  : '+ pass1[0][1]) 
            recepient = str(pass1[0][0])
            send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            return render(request, 'forgotpassword.html',{'a':'b'})
        else:

            return render(request, 'forgotpassword.html',{'a':'a'})
    else:
        return render(request, 'forgotpassword.html')
    

def operatorlogin(request):
    return render(request,'operatorlogin.html')

def addlocation(request):
    if request.method=='POST':
        if request.POST.get('login'):
            login=request.POST.get('login')
            password=request.POST.get('password')
                
            if login=="admin" and password=="adminaa":
                return render(request,'addlocation.html')
            else:
                return render(request,'operatorlogin.html',{'a':4})
        if request.POST.get('state'):
            statedata=request.POST.get('state')
            districtdata=request.POST.get('district')
            citydata=request.POST.get('city1')
            areadata=request.POST.get('area')
            if Area.objects.filter(state=statedata,district=districtdata,city=citydata,area=areadata).exists():
                return render(request,'addlocation.html',{'a':1})
            elif statedata=="" and districtdata=="" and citydata=="" and areadata=="":
                return render(request,'addlocation.html',{'a':3})
            else:
                area=Area(state=statedata,district=districtdata,city=citydata,area=areadata)
                area.save()
                listdata= (statedata,districtdata,citydata)
                return render(request,'addlocation.html',{'a':2,'listdata':listdata})
    else:
        return redirect('operatorlogin')

                

def home(request):
    if 'id'in request.session:
   
        id1 = request.session['id']  
        shopfulldata = Shopdata.objects.filter(sid = id1 ).values_list('shopname','shopimage','shopdesc','shopcontact','shopemail',
                        'shopaddress','shoparea','shopcity','shopdistrict','shopstate','holiday','type').distinct()
        shopda =list(shopfulldata[0])
        itemdata = Item.objects.filter(shopid =id1).values_list('itemname','itemcategory')
        itemlistdata =list()
        for dt in itemdata:
            itemlistdata.append(dt)
        return render(request,'home.html',{'data':shopda,'itemlistdata':itemlistdata})
    else:
        return redirect('login')
    

def header1(request):
    
    return render(request,'header1.html')

def forget(request):
    return render(request,'forget.html')