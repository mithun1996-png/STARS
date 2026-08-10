# Databse Stracturefor tEacher and PG/Mess 
from django.db import models
from django.core.validators import FileExtensionValidator

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    classes = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    fees = models.IntegerField()
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100, blank=True)
    demo_video = models.FileField(upload_to='videos/', blank=True, null=True)
    photo = models.ImageField(upload_to = "teacher_photos/", blank= True, null = True) 
    experience = models.IntegerField(default=0, 
                                     help_text = "Year of teaching experience")
    rating = models.FloatField(default = 0.0)
    views = models.IntegerField(default=0)
    varified = models.BooleanField(default = False)
    demo_video = models.FileField(
    upload_to='videos/',
    validators=[
        FileExtensionValidator(
            allowed_extensions=['mp4', 'mov', 'avi']
        )
    ],
    blank=True,
    null=True
)
    


    def __str__(self):
        return self.name
    

# Class for Mess/PG data base 
class MessPG(models.Model):
    name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)

    location = models.CharField(max_length=200)
    district = models.CharField(max_length=100)

    rent = models.IntegerField()

    food_available = models.CharField(max_length=50)
    wifi = models.BooleanField(default=False)

    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(
        max_length=15,
        blank=True
    )

    description = models.TextField()

    image = models.ImageField(upload_to='mess_images/', null=True, blank=True)
    # Gender choice 
    GENDER_CHOICES = [
        ('Boys', 'Boys'),
        ('Girls', 'Girls'),
        ('Co-ed', 'Co-ed'),
    ]
    gender_type = models.CharField(max_length=20, 
                                   choices=GENDER_CHOICES,
                                   default='Boys')
    # Single / Double / Triple Sharing
    Room_chices = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple Sharing', 'Triple Sharing'),
        ('Four', 'Four Sharing'),
    ]
    room_type = models.CharField(
        max_length=50,
        choices=Room_chices,
        blank=True,
        null=True
    )
    google_map_link = models.URLField(blank= True,
                                      help_text="Open Google Maps, click Share, and Paste the link here.")
    
    rating = models.FloatField(default=0.0)
    views = models.IntegerField(
        default=0
    )
    verified = models.BooleanField(
        default=False
    )
    featured = models.BooleanField(
        default=False
    )





    def __str__(self):
        return self.name