from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User, Booking
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.

def home_view(request):
    return render(request, 'core/home.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')

        # Validation
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if user_type not in ['doctor', 'patient']:
            messages.error(request, "Invalid user type")
            return redirect('register')

        # Create user (IMPORTANT: use your custom User model)
        user = User.objects.create_user(
            username=username,
            password=password1,
            user_type=user_type
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'core/register.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Role-based redirect
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def doctor_dashboard(request):
    if request.user.user_type != 'doctor':
        return redirect('home')

    bookings = Booking.objects.filter(doctor=request.user)

    return render(request, 'core/doctor_dashboard.html', {'bookings': bookings})

@login_required
def patient_dashboard(request):
    if request.user.user_type != 'patient':
        return redirect('home')

    bookings = Booking.objects.filter(patient=request.user)

    return render(request, 'core/patient_dashboard.html', {'bookings': bookings})

@login_required
def book_appointment(request):
    if request.user.user_type != 'patient':
        return redirect('home')

    doctors = User.objects.filter(user_type='doctor')

    if request.method == "POST":
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')

        doctor = User.objects.get(id=doctor_id)

        # prevent double booking
        if Booking.objects.filter(
            doctor=doctor,
            date=date,
            time_slot=time_slot
        ).exists():
            messages.error(request, "Slot already booked")
            return redirect('book')

        Booking.objects.create(
            patient=request.user,
            doctor=doctor,
            date=date,
            time_slot=time_slot
        )

        messages.success(request, "Appointment booked")
        return redirect('patient_dashboard')

    return render(request, 'core/book.html', {'doctors': doctors})
