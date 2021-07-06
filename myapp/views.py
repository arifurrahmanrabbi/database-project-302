from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from myapp import db
import string
import random
import datetime
import sys

# Create your views here.


def index(request):
    return render(request, 'myapp/index.html', {})


def login(request):
    return render(request, 'myapp/login.html')


def signup(request):
    return render(request, 'myapp/signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("Email: {}, Password: {}".format(email, password))
        sql = f"""	select * from user_ 
					where user_email = '{email}' and user_password = '{password}'"""
        res = db.get_table(sql)
        if res:
            user = auth.authenticate(username=res[0][0], password=password)
            if user is not None:
                auth.login(request, user)
                print("Logging Successful!!!", file=sys.stderr)
                return redirect('/dashboard')
        else:
            print("Logging Failed!!!", file=sys.stderr)
            return render(request, 'myapp/login.html', {'login_failed': True})


def user_signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        dob = request.POST.get("dob")
        sql2 = "select for_user_id.nextval from dual"
        res = db.get_table(sql2)
        print(res[0][0])
        sql = f"""	insert into user_ 
					(user_id, user_name, user_email, user_password, user_dob) 
					values 
					('U'||'{res[0][0]}', '{name}', '{email}', '{password}',TO_DATE('{dob}','YYYY-MM-DD'))"""
        db.update_table(sql)
        print(res)
        user = User.objects.create_user(
            username='U'+f'{res[0][0]}', password=password, email=email, first_name=name)
        user.save()
        auth.login(request, user)
        return redirect('/dashboard')


def property_view(request):
    if request.method == "POST":
        property_type = request.POST.getlist('property_type')
        location = request.POST.getlist('location')
        purpose = request.POST.getlist('purpose')
        beds = request.POST.get("beds")
        size = request.POST.get("size")
        min_price = request.POST.get("min-price")
        max_price = request.POST.get("max-price")
        status = request.POST.getlist("status")
        sort = request.POST.getlist("sort")
        where = ""
        if property_type:
            where = where + \
                " where property_type in ( " + str(property_type)[1:-1]+" )"
        if location:
            if where:
                where = where+" and city in ( " + str(location)[1:-1]+" )"
            else:
                where = where+" where city in ( " + str(location)[1:-1]+" )"

        if purpose:
            if where:
                where = where+" and purpose in ( " + str(purpose)[1:-1]+" )"
            else:
                where = where+" where purpose in ( " + str(purpose)[1:-1]+" )"
        if beds:
            if where:
                where = where+f" and no_of_bedrooms = {beds}"
            else:
                where = where+f" where no_of_bedrooms = {beds}"
        if size:
            if where:
                where = where+f" and size_ <= {size}"
            else:
                where = where+f" where size_ <= {size}"
        if min_price or max_price:
            if not max_price:
                max_price = "100000000"
            if not min_price:
                min_price = "0"
            if where:
                where = where+f" and price between {min_price} and {max_price}"
            else:
                where = where + \
                    f" where price between {min_price} and {max_price}"
        if status:
            if where:
                where = where+f" and status in (" + str(status)[1:-1]+" )"
            else:
                where = where+f" where status  in (" + str(status)[1:-1]+" )"
        if sort:
            if len(sort) == 2:
                where = where+f" order by  " + sort[0]+" desc,"+sort[1]+" desc"
            else:
                where = where+f" order by  " + sort[0]+" desc "
        # else:
        # 	where=where+f" order by added_on desc,price desc"

        query = """	select *from property 
					left join appartment on property.property_id=appartment.property_id 
					left join land on property.property_id=land.property_id 
					left join building on property.property_id=building.property_id """+where

        print(query)
        sql = db.get_table(query)
        print(sql)
        # print(where)
        # print(property_type,location,purpose,beds,size,min_price,max_price,status,sort)

        return render(request, 'myapp/property_view.html', {'sql': sql})

    else:
        query = """	select *from property 
					left join appartment on property.property_id=appartment.property_id 
					left join land on property.property_id=land.property_id 
					left join building on property.property_id=building.property_id 
					order by property.added_on desc"""
        sql = db.get_table(query)
        # print(sql)
        return render(request, 'myapp/property_view.html', {'sql': sql})


def dashboard(request):
    return render(request, 'myapp/dashboard.html', {})


def history(request):
    query = f"select *from property left join appartment on property.property_id=appartment.property_id left join land on property.property_id=land.property_id left join building on property.property_id=building.property_id join manages on property.property_id=manages.property_id join user_ on manages.user_id=user_.user_id where user_.user_id = '{request.user.username}' order by property.added_on desc"
    sql = db.get_table(query)
    return render(request, 'myapp/dashboard.html', {'sql': sql, 'isProfile': False, 'isNewPost': False, 'isHistory': True})


def property_post(request):
    if request.method == "POST":
        status = request.POST.get("status")
        purpose = request.POST.get("purpose")
        size = request.POST.get("size")
        price = request.POST.get("price")
        description = request.POST.get("description")
        road = request.POST.get("road")
        zip = request.POST.get("zip")
        city = request.POST.get("city")
        city = request.POST.get("city")
        type = request.POST.get("type")
        posting_date = datetime.datetime.now().strftime('%Y-%m-%d')
        closing_date = posting_date
        sql = "select for_property_id.nextval from dual"
        res = db.get_table(sql)
        if closing_date:
            sql1 = f"""	insert into property 
						values ('P'||'{res[0][0]}', '{type}', '{description}','{status}','{purpose}',
						'{road}','{zip}','{city}', TO_DATE('{posting_date}','YYYY-MM-DD'),
						TO_DATE('{closing_date}','YYYY-MM-DD'),{price},{size})"""
            db.update_table(sql1)
        else:
            sql1 = f"""	insert into 
						property(property_id,property_type,property_description,status,purpose,road_no,zip_code,
						city,added_on,price,size_) values ('P'||'{res[0][0]}', '{type}', '{description}',
						'{status}','{purpose}','{road}','{zip}','{city}', TO_DATE('{posting_date}','YYYY-MM-DD'),
						{price},{size})"""
            db.update_table(sql1)
        sql2 = f"begin insert_manages('{request.user.username}','P'||'{res[0][0]}'); end;"
        db.exec_query(sql2)
        if type == "appartment":
            floor = request.POST.get("floor")
            beds = request.POST.get("beds")
            bath = request.POST.get("bath")
            sql = f"""	insert into 
						appartment(property_id,floor_no,no_of_bedrooms,no_of_bathrooms) 
						values ('P'||'{res[0][0]}', {floor}, {beds}, {bath})"""
            db.update_table(sql)

        elif type == "building":
            building_no = request.POST.get("building_no")
            building_name = request.POST.get("building_name")
            building_floor = request.POST.get("building_floor")
            units = request.POST.get("units")
            completion_date = request.POST.get("completion_date")
            sql = f"""	insert into 
						building(property_id,building_no, building_name,no_of_floors,no_of_units,
						completion_date) values ('P'||'{res[0][0]}','{building_no}','{building_name}',
						{building_floor},{units},TO_DATE('{completion_date}','YYYY-MM-DD'))"""
            db.update_table(sql)

        else:
            reg = request.POST.get("reg")
            ltype = request.POST.get("ltype")
            stype = request.POST.get("stype")
            tax = request.POST.get("tax")
            boundaries = request.POST.get("boundaries")
            road_size = request.POST.get("road_size")
            purchase_date = request.POST.get("purchase_date")
            certificates = request.POST.get("certificates")
            sql = f"""	insert into 
						land(property_id,land_reg_no,land_type,soil_type,tax,boundaries,road_size,
						purchase_date,certificate_id) values('P'||'{res[0][0]}','{reg}','{ltype}','{stype}',
						{tax},'{boundaries}','{road_size}',TO_DATE('{purchase_date}','YYYY-MM-DD'),
						'{certificates}')"""
            db.update_table(sql)
        return redirect('/dashboard/new_post')


def profile(request):
    if request.method == "POST":
        insert = ""
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        dob = request.POST.get("dob")
        phone = request.POST.get("phone")
        road = request.POST.get("road")
        zip = request.POST.get("zip")
        city = request.POST.get("city")
        phone1 = request.POST.get("phone1")
        phone2 = request.POST.get("phone2")
        sql = f"""	begin update user_ 
					set user_name = '{name}', user_email = '{email}', user_password = '{password}', 
					user_dob = TO_DATE('{dob}','YYYY-MM-DD'),  city = '{city}', road_no = '{road}', 
					zip_code = '{zip}' where user_id = '{request.user.username}'; end;"""
        db.update_table(sql)
        sql2 = f"""	begin update 
					phone set phone_no_1='{phone1}',phone_no_2='{phone2}' 
					where userid = '{request.user.username}'; end;"""
        db.update_table(sql2)
        user = User.objects.get(username=request.user.username)
        user.set_password(password)
        user.email = email
        user.first_name = name
        user.save()
        user = auth.authenticate(
            username=request.user.username, password=password)
        auth.login(request, user)

    sql = f"""	create or replace view profile_details  
				as   select user_.user_name,user_.user_email,user_.user_password,user_.user_dob,
				phone.phone_no_1,phone.phone_no_2,user_.road_no,user_.zip_code,user_.city 
				from user_ join phone on user_.user_id=phone.userid 
				where user_id = '{request.user.username}'"""
    db.exec_query(sql)
    sql2 = f"select * from profile_details"
    res = db.get_table(sql2)
    return render(request, 'myapp/dashboard.html', {'isProfile': True, 'isNewPost': False, 'isHistory': False, 'res': res})


def new_post(request):
    return render(request, 'myapp/dashboard.html', {'isProfile': False, 'isNewPost': True, 'isHistory': False})


def property_delete(request, p_id):
    delete1 = f"begin delete from property where property.property_id='{p_id}'; end;"
    db.update_table(delete1)
    return redirect('/dashboard/history')


def property_details(request, p_id):
    query = f"select *from property left join appartment on property.property_id=appartment.property_id left join land on property.property_id=land.property_id left join building on property.property_id=building.property_id join manages on property.property_id=manages.property_id join user_ on manages.user_id=user_.user_id where property.property_id = '{p_id}'"
    sql = db.get_table(query)
    query = f"select * from user_ where user_id = '{ request.user.username }'"
    user_ = db.get_table(query)
    return render(request, 'myapp/property_details.html', {'sql': sql, 'user_': user_})


def property_edit(request, p_id):
    query = f"""select *from property 
				left join appartment on property.property_id=appartment.property_id 
				left join land on property.property_id=land.property_id 
				left join building on property.property_id=building.property_id 
				join manages on property.property_id=manages.property_id join user_ 
				on manages.user_id=user_.user_id where property.property_id = '{p_id}'"""
    sql = db.get_table(query)
    if request.method == "POST":
        status = request.POST.get("status")
        purpose = request.POST.get("purpose")
        size = request.POST.get("size")
        price = request.POST.get("price")
        description = request.POST.get("description")
        road = request.POST.get("road")
        zip = request.POST.get("zip")
        city = request.POST.get("city")
        sql = f"""	update property set 
					city = '{city}', zip_code = '{zip}', road_no = '{road}', 
					property_description = '{description}', price = '{price}', status = '{status}', 
					purpose = '{purpose}', size_ = '{size}' where property_id = '{p_id}'"""
        db.update_table(sql)

        if type == "appartment":
            floor = request.POST.get("floor")
            beds = request.POST.get("beds")
            bath = request.POST.get("bath")
            sql = f"""	update appartment set 
						floor_no = '{floor}', no_of_bedrooms = '{beds}', no_of_bathrooms = '{bath}' 
						where property_id = '{p_id}'"""
            db.update_table(sql)

        elif type == "building":
            building_no = request.POST.get("building_no")
            building_name = request.POST.get("building_name")
            building_floor = request.POST.get("building_floor")
            units = request.POST.get("units")
            completion_date = request.POST.get("completion_date")
            sql = f"""	update building set 
						completion_date = TO_DATE('{completion_date}','YYYY-MM-DD'), no_of_units = '{units}', 
						no_of_floors = '{building_floor}', building_no = '{building_no}', 
						building_name = '{building_name}' where property_id = '{p_id}'"""
            db.update_table(sql)

        else:
            reg = request.POST.get("reg")
            ltype = request.POST.get("ltype")
            stype = request.POST.get("stype")
            tax = request.POST.get("tax")
            boundaries = request.POST.get("boundaries")
            road_size = request.POST.get("road_size")
            purchase_date = request.POST.get("purchase_date")
            certificates = request.POST.get("certificates")
            sql = f"""	update land set 
						certificate_id = '{certificates}', purchase_date = 
						TO_DATE('{purchase_date}','YYYY-MM-DD'), road_size = '{road_size}', 
						boundaries = '{boundaries}', tax = '{tax}', soil_type = '{stype}', 
						land_type = '{ltype}', land_reg_no = '{reg}' where property_id = '{p_id}'"""
            db.update_table(sql)

        return redirect(f'/property_view/details/{p_id}')
    return render(request, 'myapp/property_edit.html', {'row': sql})
