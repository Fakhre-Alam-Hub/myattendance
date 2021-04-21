from django.shortcuts import render
from datetime import datetime
from Home.models import Contact
from django.contrib import messages
from Accounts.models import User, Profile
from django.http.response import StreamingHttpResponse
from Home.camera import VideoCamera
import cv2
import numpy as np
import face_recognition
from numpy import save
from Home.models import attendanceEntry
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'Home/index.html')

def attendance(request):
    return render(request, 'Home/attendance.html')

def refresh_table(request):
    queryset = attendanceEntry.objects.all()
    return JsonResponse({"table":list(queryset.values())})


def about(request):
    return render(request, 'Home/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")

        contact = Contact(name=name, email=email, phone=phone,
                          desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'Home/contact.html')


# For extracting features from stored images in database
def extract_features(request):
    import os
    import cv2
    all_user = User.objects.all()
    all_profile = Profile.objects.all()

    known_face_names = []
    images = []
    for user in all_user:
        profile = all_profile.get(user_id=user.id)
        img_path = profile.image
        cur_img = cv2.imread(f"{'media'}/{img_path}")
        images.append(cur_img)
        known_face_names.append(user.username)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    known_face_encodings = findEncodings(images)
    # save image encodings to npy file
    # default_storage.save(known_face_encodings.npy, known_face_encodings)
    save("media/known_face_encodings.npy", known_face_encodings)
    # save name to npy file
    # default_storage.save(known_face_names.npy, known_face_names)
    save("media/known_face_names.npy", known_face_names)
    messages.success(request, 'Feature extraction has been done!')

    data = attendanceEntry.objects.all()
    context = {
        'all_data': data,
    }

    return render(request, 'Home/attendance.html', context)

# For video camera
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')
