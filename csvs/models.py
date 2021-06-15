from django.db import models



def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.email) + "_" + "_" + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
    return "assets/defaultProfileImage/default.jpg"


# Create your models here.
class TeacherCsv(models.Model):
    filez = models.FileField(upload_to='teacher/csv')
    date_created = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.CharField(max_length=255)
    
    # profile_picture = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, 
    #                                     null=True, blank=True, default='default.jpg')

    email_address = models.EmailField()
    phone_number = models.CharField(max_length=255)
    room_number = models.CharField(max_length=255)
    subjects_taught = models.CharField(max_length=255)
    

    # def __str__(self):
    #     return self.id