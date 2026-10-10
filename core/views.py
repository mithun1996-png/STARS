# Logic and Processing 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher, MessPG
import os
from django.db.models import F 
from openpyxl import Workbook, load_workbook
from django.db.models import Case, When, Value, IntegerField
import razorpay
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Home page view 
def home(request):
    teachers = Teacher.objects.all()
    subject = request.GET.get('subject')
    district = request.GET.get('district')
    classes = request.GET.get('classes')
    #Filter based on search 
    if subject:
        teachers = teachers.filter(subject = subject)
    if district:
        teachers = teachers.filter(location__icontains=district)
    if classes:
        teachers = teachers.filter(classes = classes)

    return render(request, 'home.html', {'teachers': teachers})

def information(request):
    return render(request, 'information.html')
def reviews(request):
    return render(request, 'reviews.html')  # or return render(request, 'home.html') temporarily
# DEDICATED TEACHERS LIST VIEW 
# views.py
from django.shortcuts import render
from .models import Teacher

def teacher_list(request):
    teachers = Teacher.objects.annotate(
        # Assign numeric weights so Premium (3) > Pro (2) > Free (1)
        tier_weight=Case(
            When(membership_tier='premium', then=Value(3)),
            When(membership_tier='pro', then=Value(2)),
            When(membership_tier='free', then=Value(1)),
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by(
        '-is_featured',   # 1st: Featured profiles first (True before False)
        '-tier_weight',   # 2nd: Premium (3) -> Pro (2) -> Free (1)
        '-rating',        # 3rd: Highest rated tutors first
        '-id'             # 4th: Newer profiles first
    )

    return render(request, 'teacher_list.html', {'teachers': teachers})

# Add teacher 
def add_teacher(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        classes = request.POST.get('classes')
        qualification = request.POST.get('qualification')
        location = request.POST.get('location')
        fees = request.POST.get('fees')
        phone = request.POST.get('phone')

        Teacher.objects.create(name=name,
                               subject = subject,
                               classes = classes,
                               qualification = qualification,
                               location = location,
                               fees = fees,
                               phone = phone)
        # Excel file path sync with database 
        file_path = "teachers.xlsx"
        # If file exists load, else create 
        if os.path.exists(file_path):
            wb = load_workbook(file_path)
            sheet = wb.active
        else:
            wb = Workbook()
            sheet = wb.active
            sheet.append(["Name", "Subject", "Class", "Qualification", "Location", "Fess", "Phone"])
        # Add new row 
        sheet.append([name, subject, classes, qualification, location, fees, phone])
        # save file 
        wb.save(file_path)
        return redirect('/')
    return render(request, 'add_teacher.html')


# Teacher profile page 
def teacher_detail(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    return render(request, 'teacher_detail.html', {'teacher': teacher})


# Delete Teacher 
def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id = id)
    if request.method == 'POST':
        entered_phone = request.POST.get('phone')
        # Check ownership 
        if entered_phone == teacher.phone:
            teacher.delete() 
            return redirect('/')
        else:
            return render(request, 'delete_confirm.html',{
                'teacher' : teacher,
                'error' : 'Incorrect phone number!'

            })
    return render(request, 'delete_confirm.html', {'teacher':teacher})

# Edit Teacher details 
def edit_teacher(request, id ):
    teacher = get_object_or_404(Teacher, id = id )
    if request.method == 'POST':
        # Check ownership (Same as delete)
        entered_phone = request.POST.get('phone') or request.POST.get('phone_check') or request.POST.get('phone_number')
        if entered_phone != teacher.phone:
            return render(request, 'edit_teacher.html', { 
            'teacher':teacher,
            'error': 'Incorrect phone number!'
            })
        # Update Profiles 
        teacher.name = request.POST.get('name')
        teacher.subject = request.POST.get('subject')
        teacher.classes = request.POST.get('classes')
        teacher.qualification = request.POST.get('qualification')
        teacher.location = request.POST.get('location')
        teacher.fees = request.POST.get('fees')

        teacher.save()
        return redirect('/')
    return render(request, 'edit_teacher.html', {'teacher': teacher})


# Mess/PG List
def messpg_list(request):
    messes = MessPG.objects.all() # Select all records 
    return render(request, 'messpg_list.html', {'messes':messes})


# Add PGregistrartion
def add_messpg(request):
    if request.method == 'POST':
        MessPG.objects.create(
            name=request.POST.get('name'),
            owner_name=request.POST.get('owner_name'),
            location=request.POST.get('location'),
            district=request.POST.get('district'),
            rent=request.POST.get('rent'),
            food_available=request.POST.get('food_available'),
            phone=request.POST.get('phone'),
            description=request.POST.get('description')
        )
        return redirect('/messpg/')
    return render(request, 'add_messpg.html')

# PG/Mess detsils page 

def mess_details(request, id):
    """
    This function runs when a user visits a PG/Mess details page.
    request : Information about the visitor 
    id : Unique identifier for the PG/Mess 
    """
    # Serch for a MeesPG 
    mess = get_object_or_404(MessPG, id =id)
    # Increse the views count directly in the database.
    MessPG.objects.filter(pk = mess.pk).update(views = F('views') +1)
    mess.refresh_from_db()
    # sent the data to the HTML page 

    return render(request, 'mess_detail.html', {'mess':mess})

# This make render dynamically with database content 
def learning_python(request):
    return render(request, 'python.html')

def learning_html(request):
    return render(request, 'html.html')

def learning_matlab(request):
    return render(request, 'matlab.html')

def learning_latex(request):
    return render(request, 'latex.html')


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def initiate_upi_payment(request):
    # Amount in paise (₹299 = 29900 paise)
    amount = 29900 
    
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    }
    
    order = client.order.create(data=order_data)
    
    context = {
        'order_id': order['id'],
        'amount': amount,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'user_name': request.user.get_full_name() if request.user.is_authenticated else "Student",
    }
    return render(request, 'upi_payment.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        try:
            # Verify signature to prevent tampering
            client.utility.verify_payment_signature({
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature')
            })
            
            # TODO: Update your Teacher / Subscription model status to "ACTIVE" here
            
            return JsonResponse({'status': 'Payment Successful'})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'Payment Verification Failed'}, status=400)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Teacher

def submit_upi_utr(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == "POST":
        utr_number = request.POST.get("utr_number", "").strip()
        selected_plan = request.POST.get("membership_tier", "pro")

        # Validate UTR length (12 digits for Indian UPI transactions)
        if len(utr_number) == 12 and utr_number.isdigit():
            teacher.utr_number = utr_number
            teacher.membership_tier = selected_plan
            teacher.payment_status = 'pending'  # Awaits admin verification
            teacher.save()

            messages.success(request, "Your payment UTR was submitted successfully! Profile will be activated after quick verification.")
            return redirect('teacher_detail', pk=teacher.id)
        else:
            messages.error(request, "Please enter a valid 12-digit UPI Transaction/UTR reference number.")
            
    return render(request, "submit_utr.html", {"teacher": teacher})

def python_page(request):
    return render(request, 'python.html')

def html_page(request):
    return render(request, 'html.html')

def matlab_page(request):
    return render(request, 'matlab.html')

def latex_page(request):
    return render(request, 'latex.html')