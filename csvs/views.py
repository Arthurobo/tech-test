from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import TeacherCsvModelForm
from .models import TeacherCsv, Teacher
from account.models import Account
import csv

@login_required
def add_teacher(request):
    form = TeacherCsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = TeacherCsvModelForm()

        obj = TeacherCsv.objects.get(activated=False)
        with open(obj.filez.path, 'r') as f:
            # reader = csv.reader(f)
            reader = csv.reader(f, delimiter=',',)

            for i, row in enumerate(reader):
                # if i==0:
                #     pass
                # else:
                password = "1234"
                if row:    
                    first_name = row[0]
                    last_name =  row[1]
                    profile_image = row[2]
                    email = row[3]
                    phone_number = row[4]
                    room_number = row[5]
                    subjects_taught = row[6]
                    
                    Account.objects.create(
                        first_name = first_name,
                        last_name = last_name,
                        # profile_image = profile_image,
                        email = email,
                        phone_number = phone_number,
                        room_number = room_number,
                        subjects_taught = subjects_taught,
                        password = password,
                    )
            obj.activated = True
            obj.save()

    return render(request, 'csv/upload.html', {'form': form})