from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class Department(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    approved = models.BooleanField(default=False)  

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=10)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    phone = models.CharField(max_length=150,default=True) 
    image = models.ImageField(upload_to='patients/',null=True)
    def __str__(self):
        return self.user.email




class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    disease = models.CharField(max_length=150)
    appointment_date = models.DateField()


    def __str__(self):
        return f'{self.patient.user.email} - {self.doctor.user.email} - {self.appointment_date}'



class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)