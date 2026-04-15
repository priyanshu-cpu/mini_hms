from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    
    user_type = models.CharField(max_length=10, choices=ROLE_CHOICES)


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.doctor.username} - {self.date} - {self.time_slot}"


class Booking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_bookings')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_bookings')
    date = models.DateField()
    time_slot = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} booked {self.doctor.username}"