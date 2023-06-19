from django.shortcuts import render , get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import *
from .decorators import *
from django.contrib.auth.models import User , Group
from django.contrib import messages
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse
import json
from datetime import datetime ,date , time
from .filters import ProductFilter
from django.db.models import Q


def IS_discount(x):
    if x == 0 or x == '' or x == '0':
        return False
    else:
        return True
def setDate(x):
    date = datetime.strptime(x, '%Y-%m-%d')
    return date
def setTime(x):
    hour1 , minute1  = x.split(':')
    time1 = time(int(hour1), int(minute1))
    return time1
def checkDateTime(x,y):
    if x and y:
        return True
    else: return False
def getDateTime(x,y):
    session = None
    if checkDateTime(x , y):
        x1 = setTime(x)
        y1 = setDate(y)
        session = datetime.combine(y1 , x1)
    return session
def start_session_List(x , y , z , i , j):
    list = [x , y , z , i , j]
    return list
def end_session_List(x , y , z , i , j):
    list = [x , y , z , i , j]
    return list
def save_sessin(doctor , list1 , list2 , duration):
    for i , j in zip(list1 , list2):
        if i and j :
            session1 = session.objects.create(doctor = doctor , startsession = i , endsession = j ,duration =  duration)
        else:
            list1.remove(i)
            list2.remove(j)


# Create your views here.


@authandicated
def Doctor_signUP(request):
    form = RegForm()
    msg = ''
    phone= request.POST.get('number')
    name = request.POST.get('name')
    email= request.POST.get('email')
    vent_phone = request.POST.get('vent_number')
    vent_add = request.POST.get('business-add')
    about = request.POST.get('about')
    profile_pic =request.FILES.get('profile_pic') 
    vent_pic =request.FILES.getlist('vent_pic')
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            prof = form.save()
            user = auth.authenticate(request,username = request.POST.get('username'),password = request.POST.get('password1'))
            if user is not None:
                device = request.COOKIES.get('device')
                pro_get = Profile.objects.filter(device = device)
                if pro_get:
                    pro_get = Profile.objects.get(device = device)
                    pro_get.user = user 
                    pro_get.phone = phone
                    pro_get.email = email
                    pro_get.address = vent_add
                    pro_get.save()
                profileU = Profile(user = user , phone = phone , email = email , device = device)
                profileU.save()
                doctor_prof = DoctorVent(user = user,name = name , email = email , phone = phone , vent_phone= vent_phone 
                                    , address = vent_add , about = about , profile_pic = profile_pic)
                doctor_prof.save()
                doctor_profile = Profile.objects.create(user = user , email = email , phone = phone , address = vent_add)
                group = Group.objects.get(name = 'doctor')
                prof.groups.add(group)
                for img in vent_pic:
                    photo = Vent_Photo.objects.create(
                    DoctorVent = doctor_prof ,
                    vent_img=img,
                )
                auth.login(request , user)
                next_url = request.GET.get('next')
                if next_url == '' or next_url == None:
                    next_url = 'home'
                return redirect(next_url)
            else:
                msg = messages.error('please cheak username or pass')
    context = {'form':form , 'msg': msg}
    return render(request , 'doctor-sign.html',context)
@login_required(login_url = 'login')
@only_Doctor
def vetDash(request):
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor1 = user.groups.filter(name='doctor').exists()
    doctor = DoctorVent.objects.get(user = user)
    session_booked = Bookedsession.objects.filter(doctor = doctor)
    if request.method == 'POST':
        date1 = request.POST.get('date1')
        startsessionT1 = request.POST.get('startsession1')
        endsessionT1 = request.POST.get('endsessin1')
        
        date2 = request.POST.get('date2')
        startsessionT2 = request.POST.get('startsession2')
        endsessionT2 = request.POST.get('endsessin2')
        
        date3 = request.POST.get('date3')
        startsessionT3 = request.POST.get('startsession3')
        endsessionT3 = request.POST.get('endsessin3')
        
        date4 = request.POST.get('date4')
        startsessionT4 = request.POST.get('startsession4')
        endsessionT4 = request.POST.get('endsessin4')
        
        date5 = request.POST.get('date5')
        startsessionT5 = request.POST.get('startsession5')
        endsessionT5 = request.POST.get('endsessin5')
        
        duration = request.POST.get('duration1')
        
        startsession = getDateTime(startsessionT1 , date1)
        startsession1 = getDateTime(startsessionT2 , date2)
        startsession2 = getDateTime(startsessionT3 , date3)
        startsession3 = getDateTime(startsessionT4 , date4)
        startsession4 = getDateTime(startsessionT5 , date5)
        startList = start_session_List(startsession , startsession1 , startsession2 , startsession3 , startsession4 )
        
        endsession = getDateTime(endsessionT1 , date1)
        endsession1 = getDateTime(endsessionT2 , date2)
        endsession2 = getDateTime(endsessionT3 , date3)
        endsession3 = getDateTime(endsessionT4 , date4)
        endsession4 = getDateTime(endsessionT5 , date5)
        endList = end_session_List(endsession ,endsession1 , endsession2 , endsession3 , endsession4)
        
        save_sessin(doctor , startList , endList , duration)
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request , 'vetDash.html' , {'customer':custom,'aa':myFilter, 'user1': doctor , 'doctor':doctor1 , 'session':session_booked})

#done
login_required(login_url = 'login')
@only_seller
def addPET(request):
    if request.user:
        user = request.user
        custom = user.groups.filter(name='customer').exists() 
        
    pet = 1
    product_name = request.POST.get('product-name')
    product_sortDes = request.POST.get('sort-des')
    description = request.POST.get('Detail')
    first_file_upload = request.FILES.get('first-file-upload')
    second_file_upload = request.FILES.get('second-file-upload')
    third_file_upload = request.FILES.get('third-file-upload')
    last_file_upload = request.FILES.get('last-file-upload')
    price = request.POST.get('price')
    product_discount_price = request.POST.get('discount-price')
    product_sell_price = request.POST.get('price')
    stock =request.POST.get('stock')
    pet_type = "none"
    categories = request.POST.get('categories')
    images = [first_file_upload , second_file_upload , third_file_upload , last_file_upload]
    discount = IS_discount(product_discount_price)
    product1 = Product(
        user = user,product_name = product_name,
        product_shot_des = product_sortDes , product_description = description,
        product_price = price, discount = discount ,
        product_discount_price = product_discount_price,
        product_Catecory = categories ,
        product_sell_price = product_sell_price ,
        product_stock= stock,product_type = pet_type,
        slug = product_name
    )
    if request.method == 'POST'and request.FILES:
        product1.save()
        prodct11 = Product.objects.get(product_name = product_name)
        prodct11.product_img = first_file_upload
        prodct11.save()
        
        for x in images:
            if x:
                pic = Photo.objects.create(
                    product= prodct11,
                    product_img = x
                )
            else:
                images.remove(x)
        return redirect('DashBoard')
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'add-product.html',{'customer':custom, "pet":pet ,'aa':myFilter})
# done
@authandicated
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(email = email)
        user1 = auth.authenticate(request, username = user.username , password = password)
        if user1 is not None:
            auth.login(request,user1)
            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'please check username or password')
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'login.html',{'aa':myFilter})
# done
@authandicated
def signup(request):
    form = RegForm()
    phone= request.POST.get('number')
    email= request.POST.get('email')
    message1 = ''
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            prof = form.save()
            user = auth.authenticate(request,username = request.POST.get('username'),password = request.POST.get('password1'))
            if user:
                device = request.COOKIES.get('device')
                pro_get = Profile.objects.filter(device = device)
                if pro_get:
                    pro_get = Profile.objects.get(device = device)
                    pro_get.user = user 
                    pro_get.phone = phone
                    pro_get.email = email
                    pro_get.save()
                profileU = Profile(user = user , phone = phone , email = email , device = device)
                profileU.save()
                group = Group.objects.get(name = 'customer')
                prof.groups.add(group)
                if user is not None:
                    auth.login(request,user)
                    next_url = request.GET.get('next')
                    if next_url == '' or next_url == None:
                        next_url = 'home'
                    return redirect(next_url)
            else:
                message1 =  'please check username or password'
        else:
                message1 =  'please check username or password'
    return render(request,'signup.html',{'form':form , 'msg':message1})
# done
def logoutUser(request):
    auth.logout(request)
    return redirect('login')
# Done

# done
@login_required(login_url = 'login')
@only_seller
def addProduct(request):
    if request.user:
        user = request.user
        custom = user.groups.filter(name='customer').exists() 
    product_name = request.POST.get('product-name')
    product_sortDes = request.POST.get('sort-des')
    description = request.POST.get('Detail')
    first_file_upload = request.FILES.get('first-file-upload')
    second_file_upload = request.FILES.get('second-file-upload')
    third_file_upload = request.FILES.get('third-file-upload')
    last_file_upload = request.FILES.get('last-file-upload')
    price = request.POST.get('price')
    product_discount_price = request.POST.get('discount-price')
    product_sell_price = request.POST.get('sell-price')
    stock =request.POST.get('stock')
    pet_type = request.POST.get('pet-Type')
    categories = request.POST.get('categories')
    images = [first_file_upload , second_file_upload , third_file_upload , last_file_upload]
    discount = IS_discount(product_discount_price)
    product1 = Product(
        user = user,product_name = product_name,
        product_shot_des = product_sortDes , product_description = description,
        product_price = price, discount = discount ,
        product_discount_price = product_discount_price,
        product_Catecory = categories ,
        product_sell_price = product_sell_price ,
        product_stock= stock,product_type = pet_type,
        slug = product_name
    )
    if request.method == 'POST'and request.FILES:
        product1.save()
        prodct11 = Product.objects.get(product_name = product_name)
        prodct11.product_img = first_file_upload
        prodct11.save()
        
        for x in images:
            if x:
                pic = Photo.objects.create(
                    product= prodct11,
                    product_img = x
                )
            else:
                images.remove(x)
        return redirect('DashBoard')
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'add-product.html',{'customer':custom , 'aa':myFilter})
# done
@login_required(login_url = 'login')
def seller(request):
    business_name = request.POST.get('business-name')
    business_add = request.POST.get('business-add')
    about = request.POST.get('about')
    business_phone = request.POST.get('phone')
    user = request.user
    profile_user = Profile.objects.get(user = user)
    profile_user.business_name = business_name
    profile_user.address = business_add
    profile_user.about = about
    profile_user.business_phone = business_phone
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    if request.method == 'POST':
        group = Group.objects.get(name = 'seller')
        groupCus = Group.objects.get(name = 'customer')
        user.groups.add(group)
        user.groups.remove(groupCus)
        profile_user.save()
        return redirect('DashBoard')
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'seller.html',{'customer':custom , 'aa':myFilter})
# done
def product(request):
    products = Product.objects.all()
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter , 'doctor':doctor})
# Done
def home(request):
    discountProduct  =Product.objects.filter(discount = True)
    Dogs = Product.objects.filter(product_type = 'Dog',product_Catecory = 'none')
    Cats = Product.objects.filter(product_type = 'Cat',product_Catecory = 'Food')
    user = request.user
    custom = user.groups.filter(name='customer').exists()
    doctor = user.groups.filter(name='doctor').exists()
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    context = {'customer':custom,'discoutProduct':discountProduct, 
            'Dogs':Dogs,'Cats':Cats, 'cartItem':cartItems,'items':items, 'order':order , 'aa':myFilter , 'doctor':doctor }
    return render(request,'index.html', context)

# Done
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    customer = Profile.objects.get(user = customer)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
# Done
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    device = request.COOKIES.get('device')  
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        customer = Profile.objects.get(user = customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer = Profile.objects.create(device=device)
        customer , order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
# Done-test
def productDetail(request):
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'product-detail.html',{'customer':custom, 'cartItem':cartItems , 'aa':myFilter , 'doctor':doctor})
# Done
def productDetailList(request,slug):
    product_data = Product.objects.get(slug = slug)
    prodctImgs = Photo.objects.filter(product = product_data)
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    
    product1  =Product.objects.filter(discount = True)
    product2 = Product.objects.filter(product_type = 'Dog',product_Catecory = 'none')
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'product-detail.html',{'data':product_data, 'customer':custom,
                                                 'discoutProduct':product1, 'Dogs':product2
                                                 ,'imgs':prodctImgs , 'cartItem':cartItems, 'aa':myFilter , 'doctor':doctor})
# Done
def card(request):
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    context = {'items':items, 'order':order, 'cartItems':cartItems ,'customer':custom,'aa':myFilter  ,'doctor':doctor}
    return render(request,'card.html',context)
# Done
@login_required(login_url = 'login')
def checkout(request):
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    context = {'items':items, 'order':order, 'cartItems':cartItems , 'customer':custom , 'aa':myFilter , 'doctor':doctor}
    return render(request,'checkout.html',context)
#Done
login_required(login_url = 'login')
@only_seller
def deleteProduct(request,slug):
    product1 = Product.objects.get(slug = slug)
    product1.delete()
    return redirect('DashBoard')
#Done
login_required(login_url = 'login')
@only_seller
def editProduct(request,slug):
    if request.user:
        user = request.user
        custom = user.groups.filter(name='customer').exists() 
    product1 = Product.objects.get(slug = slug)    
    product_name = request.POST.get('product-name')
    product_sortDes = request.POST.get('sort-des')
    description = request.POST.get('Detail')
    first_file_upload = request.FILES.get('first-file-upload')
    second_file_upload = request.FILES.get('second-file-upload')
    third_file_upload = request.FILES.get('third-file-upload')
    last_file_upload = request.FILES.get('last-file-upload')
    price = request.POST.get('price')
    product_discount_price = request.POST.get('discount-price')
    product_sell_price = request.POST.get('price')
    stock =request.POST.get('stock')
    pet_type = request.POST.get('pet-Type')
    categories = request.POST.get('categories')
    images = [first_file_upload , second_file_upload , third_file_upload , last_file_upload]
    discount = IS_discount(product_discount_price)
    product = Product.objects.get(slug = slug)
    product.product_name = product_name
    product.product_shot_des = product_sortDes
    product.product_description = description
    product.product_sell_price = product_sell_price
    product.product_price = price
    product.product_discount_price = product_discount_price
    product.product_stock = stock
    product.product_type = pet_type
    product.product_Catecory = categories
    product.discount = discount
    if first_file_upload:
        product.product_img = first_file_upload
        for x in images:
            if x :
                pic = Photo.objects.create(
                    product= product,
                    product_img = x
                )
            else:
                images.remove(x)
    if request.method == 'POST'or request.FILES:
        product.save()
        return redirect('DashBoard')
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'edit-product.html',{'product':product1,'customer':custom , 'aa':myFilter})
#done
@login_required(login_url = 'login')
@only_seller
def dashBoard(request):
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    Product1 = Product.objects.filter(user = user)
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'sellerDash.html',{'product':Product1,'customer':custom,'aa':myFilter})
#done
def product_types(request,types):
    products = Product.objects.filter(product_type = types)
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'product.html',{'products':products,'customer':custom,'cartItem':cartItems,'types':types ,'aa':myFilter, 'doctor':doctor})
#done
def product_catigory(request,catigory):
    products = Product.objects.filter(product_Catecory = catigory)
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter is not None  :
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request,'product.html',{'products':products,'customer':custom,'cartItem':cartItems,'types':catigory ,'aa':myFilter, 'doctor':doctor})

#DONE
def doctorcards(request):
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    docdata = DoctorVent.objects.all()
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    return render(request, 'doctorcards.html', {'aa': myFilter, 'docdata': docdata , 'customer':custom , 'doctor':doctor})
#DONE
def doctor_details(request, slug):
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    doctor1 = get_object_or_404(DoctorVent, slug=slug)
    sessions = session.objects.all()
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    vent_photos = Vent_Photo.objects.all()
    context = {'doctor': doctor, 'sessions': sessions,'aa': myFilter,'vent_photos': vent_photos , 'doctordata':doctor1}
    return render(request, 'doctor_details.html', context)
#DONE
def book_session(request, session_id , slug):
    user = request.user
    custom = user.groups.filter(name='customer').exists() 
    doctor = user.groups.filter(name='doctor').exists()
    zz = 1
    session1 = get_object_or_404(session, id=session_id)
    doctor1 = get_object_or_404(DoctorVent, slug=slug)
    sessions = session.objects.all()
    petiant = Profile.objects.get(user = user)
    thisSession = session.objects.get(id = session_id)
    sessiondata =thisSession.startsession
    if request.method == 'POST':
        booked = Bookedsession.objects.create(patient = petiant ,doctor =doctor1 , sessionData = sessiondata)
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    product_name_filter = request.GET.get('product_name')
    if product_name_filter != '' and product_name_filter is not None:
        products = myFilter.qs
        return render(request,'product.html',{'products':products,'customer':custom , 'cartItem':cartItems , 'aa':myFilter})
    vent_photos = Vent_Photo.objects.all()    
    context = {'doctor': doctor, 'sessions': sessions,'aa': myFilter,'vent_photos': vent_photos , 'doctordata':doctor1 , 'zz':zz}
    return render(request,'doctor_details.html' , context)










