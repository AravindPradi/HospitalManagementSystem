from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import Department, Doctor, Appointment, Patient, Notification
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
import random
import string
from datetime import date

User = get_user_model()


def home(request):
    return render(request,'home.html')


def register(request):
    return render(request,'register_splash.html')





def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif hasattr(user, 'doctor'):
                return redirect('doctor_dashboard')
            elif hasattr(user, 'patient'):
                return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'login.html')









def doc_register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        department_id = request.POST.get('department')
        image = request.FILES.get('image')

        
        if User.objects.filter(username=uname, email=email).exists():
            messages.info(request, 'Data already exists, check username and email')
            return redirect('doc_register')
        else:

            user = User.objects.create(username=uname, email=email, first_name=fname, last_name=lname)

            department = Department.objects.get(id=department_id)

            doctor = Doctor.objects.create(user=user, department=department, image=image, approved=False)  

            subject = 'Account Registration'
            message = f'Your account registration is pending approval by the admin.\nUsername: {uname}'
            from_email = 'aravind.pradeep.0802@gmail.com'
            to_email = [email]
            send_mail(subject, message, from_email, to_email)

            messages.info(request, 'Registration request sent. Please wait for admin approval.')
            return redirect('doc_register')
    else:
        dept = Department.objects.all()
        context = {'dept': dept}
        return render(request, 'doc_register.html', context=context)



def admin_approve(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    doctor.approved = True

    password = ''.join(random.choices(string.digits, k=6))
    
    hashed_password = make_password(password)
    
    doctor.user.password = hashed_password
    
    doctor.save()
    doctor.user.save()

    subject = 'Account Registration Approved'
    message = f'Your account has been approved by the admin.\nUsername: {doctor.user.username}\nPassword: {password}'
    from_email = 'aravind.pradeep.0802@gmail.com'
    to_email = [doctor.user.email]
    send_mail(subject, message, from_email, to_email)

    messages.info(request, 'Doctor registration approved.')
    return redirect('admin_dashboard')




def admin_reject(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    user_email = doctor.user.email
    doctor.delete()

    subject = 'Account Registration Rejected'
    message = 'Your account registration has been rejected by the admin.'
    from_email = 'aravind.pradeep.0802@gmail.com'
    to_email = [user_email]
    send_mail(subject, message, from_email, to_email)

    messages.info(request, 'Doctor registration rejected.')
    return redirect('admin_dashboard')





        
    

def doctor_dashboard(request):
    return render(request,'doctor_dashboard.html')


def all_patient_details(request):
    patients = Patient.objects.all()
    return render(request, 'all_patient_details.html', {'patients': patients})







@login_required(login_url='custom_login')
def upcomings(request):
    doctor = request.user.doctor  
    today = date.today()
    upcoming_appointments = Appointment.objects.filter(doctor=doctor, appointment_date__gte=today)
    return render(request, 'upcomings.html', {'upcoming_appointments': upcoming_appointments})
    









@login_required(login_url='custom_login')
def profile(request):
    current_user = request.user

    try:
        doctor = Doctor.objects.get(user=current_user)
        department = doctor.department
        image_url = doctor.image.url if doctor.image else None
        phone1 = None
    except Doctor.DoesNotExist:
        doctor = None
        try:
            patient = Patient.objects.get(user=current_user)
            department = patient.department
            phone1 = patient.phone
            image_url = None  
        except Patient.DoesNotExist:
            department = None
            phone1 = None
            image_url = None

    context = {
        'doctor': doctor,
        'department': department,
        'phone': phone1,
        'image_url': image_url,
    }
    return render(request, 'profile.html', context=context)


@login_required(login_url='custom_login')
def update_profile(request):
    current_user = request.user
    try:
        doctor = Doctor.objects.get(user=current_user)
        if request.method == 'POST':
            current_user.first_name = request.POST.get('fname')
            current_user.last_name = request.POST.get('lname')
            current_user.email = request.POST.get('email')
            current_user.username = request.POST['uname']
            current_user.save()

            new_image = request.FILES.get('image')
            if new_image:  
                doctor.image = new_image
        
            department_id = request.POST.get('department')
            department = Department.objects.get(id=department_id)
            doctor.department = department
            doctor.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else: 
            dept = Department.objects.all()
            context = {'doctor': doctor, 'dept': dept}
            return render(request, 'update_profile.html', context=context)
    except Doctor.DoesNotExist:
        pass
    return render(request, 'update_profile.html')






def patient_register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')

        patient_id = str(random.randint(000, 9999)).zfill(4)
        password = ''.join(random.choices(string.digits, k=6))
        hashed_password = make_password(password)

        user = User.objects.create(email=email, password=hashed_password, first_name=fname, last_name=lname,username=uname)
        patient = Patient.objects.create(user=user, image=image, phone=phone, patient_id=patient_id)

        
        subject = 'Account Registration'
        message = f"Hello,\n\nThank you for registering!\n\nYour login credentials are:\nUsername: {uname}\nEmail: {email}\nPassword: {password}\nPatient ID: {patient.id}\n\nBest regards,\nBook The Doc"

        from_email = 'aravind.pradeep.0802@gmail.com'
        to_email = [email]
        send_mail(subject, message, from_email, to_email)

        messages.info(request, 'Check your email for credentials')
        return redirect('patient_register')

    else:
        dept = Department.objects.all()
        context = {'dept': dept}
        return render(request, 'patient_register.html', context=context)







@login_required(login_url='custom_login')
def patient_dashboard(request):
    return render(request,'patient_dashboard.html')









def p_appointment(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        dis = request.POST.get('dis')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        
        
        
        doctor = Doctor.objects.get(id=doctor_id)
        
        appointment_count = Appointment.objects.filter(doctor=doctor, appointment_date=date).count()
        if appointment_count >= 5:
            messages.error(request, 'Booking limit exceeded for the selected date. Please choose another date.')
            return redirect('p_appointment')
        
        try:
            patient_profile = request.user.patient
        except AttributeError:
            patient_profile = None
        
        if patient_profile:
            patient = patient_profile

            appointment = Appointment.objects.create(patient=patient, doctor=doctor, appointment_date=date)
            appointment.save()

            message = f'New appointment scheduled for {date} by {patient.user.first_name}'
            Notification.objects.create(recipient=doctor.user, message=message)

            print("Appointment created successfully!")
            messages.success(request, 'Appointment created successfully, we will contact you soon !')
        else:
            print("Error: Patient profile not found!")
            messages.error(request, 'Error: Patient profile not found!')
        
        return redirect('p_appointment')
    
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'p_appointment.html', {'departments': departments, 'doctors': doctors})




def notifications(request):
    return render(request,'notifications.html') 



def mark_notifications_as_read(request):
    request.user.notifications.filter(read=False).update(read=True)
    return redirect('doctor_dashboard')


def delete_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.delete()
    return redirect('notifications')








@login_required(login_url='custom_login')
def appointment_done(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, 'Appointment done successfully!')
    return redirect('upcomings')
    
    





@login_required(login_url='custom_login')
def patient_profile(request):
   
    try:
        patient = request.user.patient
        phone = patient.phone
        image_url = patient.image.url if patient.image else None
        context = {
            'user': request.user,
            'phone': phone,
            'image_url': image_url
        }
        return render(request, 'patient_profile.html', context=context)
    except Patient.DoesNotExist:
       
        return render(request, 'patient_profile.html')
    







@login_required(login_url='custom_login')
def reset_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old')
        new_password = request.POST.get('new')

        if request.user.check_password(old_password):
            request.user.password = make_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('custom_login') 
        else:
            messages.error(request, 'Old password is incorrect.')
    return render(request, 'reset_password.html')




def logout(request):
    auth.logout(request)
    return redirect('home')








# Admin panel views


@login_required(login_url='custom_login')
def admin_dashboard(request):
    
    return render(request, 'admin_dashboard.html')



@login_required(login_url='custom_login')
def add_dept(request):
    if request.method == 'POST':
        d_name = request.POST.get('dept_name')
        d_desc = request.POST.get('dept_desc')

        existing_dept = Department.objects.filter(name=d_name).exists()
        if not existing_dept:
            dept_data = Department.objects.create(name=d_name, desc=d_desc)
            dept_data.save()
            messages.success(request, 'Department added successfully')
        else:
            messages.error(request, 'Department already exists.')

        return redirect('add_dept')

    return render(request, 'add_dept.html')


def doc_details(request):
    doctors = Doctor.objects.all()
    
    context = {'doctors':doctors}
    return render(request,'doc_details.html',context=context)



@login_required(login_url='custom_login')
def doc_update(request,pk):
    data = get_object_or_404(Doctor,pk=pk)

    if request.method == 'POST':
        data.user.first_name = request.POST['fname']
        data.user.last_name = request.POST['lname']
        data.user.username = request.POST['uname']
        data.user.email = request.POST['email']
        select = request.POST['department']
        department = Department.objects.get(id=select)
        data.department = department


        new_image = request.FILES.get('image')
        if new_image:
            data.image = new_image


        data.user.save()
        data.save()
        return redirect('doc_details')
    dept = Department.objects.all()
    context = {'data':data,
               'dept':dept
               }
    return render(request,'doc_update_admin.html',context=context)




@login_required(login_url='custom_login')
def doc_delete(request,pk):
    data = get_object_or_404(Doctor,id=pk)

    if request.method == 'POST':
        user = data.user
        data.delete()
        user.delete()
        return redirect('doc_details')
    context = {'data':data}
    return render(request,'doc_delete.html',context=context)





@login_required(login_url='custom_login')
def all_appointments(request):
    data = Appointment.objects.all()
    
    return render(request,'all_appointments_admin.html',{'data':data})


def approvals(request):
    pending_doctors = Doctor.objects.filter(approved=False)
    context = {'pending_doctors': pending_doctors}
    return render(request,'approvals.html',context=context)



@login_required(login_url='custom_login')
def all_dept(request):
    data = Department.objects.all()
    context = {'data':data}
    return render(request,'all_dept.html',context=context)