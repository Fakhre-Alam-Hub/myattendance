from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=70)
    phone = models.CharField(max_length=10)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
            return self.name

class attendanceEntry(models.Model):
    name = models.CharField(max_length=100, unique_for_date='date')
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now=True)

    # class Meta:
    #     unique_together = (("name", "date"),)