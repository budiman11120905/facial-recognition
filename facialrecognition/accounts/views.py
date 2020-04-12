from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import StreamingHttpResponse
from accounts.forms import RegistrationForm
from .models import UserProfile
import face_recognition
import requests
import cv2
import numpy as numpy
from PIL import Image as img, ImageDraw
import fnmatch
import os

# Used for finding dir paths
#rootDir = '../facialrecognition'

IMAGES_DIR = 'facialrecognition/media/images'
VERIF_DIR = 'facialrecognition/media/verif'

user_photo = []
user_photo_name = []

def home(request):
    numbers = [1, 2, 3, 4, 5]
    name = 'Aaron Moran'

    args = {'myName': name, 'numbers': numbers}
    return render(request, 'accounts/home.html', args)

# Fully working adding users and images


def register(request):
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("images")
            obj = UserProfile.objects.create(
                title=name,
                img=img
            )
            obj.save()
            print(obj)

            return render(request, 'accounts/verify.html', context)
          
    else:
        form = RegistrationForm()
    context['form'] = form
    return render(request, 'accounts/register.html', context)

def verifyPhoto(request):
    context = {}
    #DEBUG CODE TO FIND DIRECTORY TREES
    # for dirName, subdirList, fileList in os.walk(rootDir):
    #     print('Found directory: %s' % dirName)
    #     for fname in fileList:
    #         print('\t%s' % fname)

    '''Loop over images in directory, add to lists
    TODO: use the encoded images to verify user
    '''
    print("Loading registered faces database!")
    for file in os.listdir(IMAGES_DIR):
        if file.endswith(('.jpeg', '.png')):
            image = face_recognition.load_image_file(f"{IMAGES_DIR}/{file}")
            # encodes all found faces
            encoding = face_recognition.face_encodings(image)[0]
            user_photo.append(encoding)
            user_photo_name.append(file)

            print(user_photo)
            print(user_photo_name)

    if takePhoto() is True:
        form = RegistrationForm()
        context['form'] = form
        return redirect('/login')
    else:
        form = RegistrationForm()
        context['form'] = form
        return redirect('/register')


def takePhoto():
    context = {}
    # Get user to take image
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        cv2.imshow("Take Verification picture", frame)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.imwrite(f"{VERIF_DIR}/photo.png", frame)
            cv2.destroyAllWindows()
            break

    ver_photo = face_recognition.load_image_file(f"{VERIF_DIR}/photo.png")
    ver_photo_enc = face_recognition.face_encodings(ver_photo)[0]

    print(f"VERIFICATION PHOTO: {ver_photo}")
    print(f"VERIFICATION PHOTO ENC: {ver_photo_enc}")

    ver_locs = face_recognition.face_locations(ver_photo)
    ver_photo_enc = face_recognition.face_encodings(ver_photo, ver_locs)

    pil_image = img.fromarray(ver_photo)
    draw = ImageDraw.Draw(pil_image)

    for(top, right, bottom, left), ver_photo_enc in zip(ver_locs, ver_photo_enc):
        matches = face_recognition.compare_faces(user_photo, ver_photo_enc)

    if True in matches:
        print("Thank you for registering")
        return True
    else:
        print("FAILED")    
        return False
