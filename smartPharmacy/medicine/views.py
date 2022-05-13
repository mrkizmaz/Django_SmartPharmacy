from email import message
from django.shortcuts import render,redirect, get_object_or_404
from medicine.forms import *
from django.contrib import messages
from medicine.models import Medicine, Patient
from smartPharmacy import settings
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required

# Create your views here.
# anasayfa
def index(request):
    return render(request, 'index.html')

# dashboard
@login_required(login_url='user:login')
def dashboard(request):

    keyword = request.GET.get("keyword")
    if keyword:
        medicines = Patient.objects.filter(first_name__contains = keyword)
        return render (request, "dashboard.html", {"medicines":medicines})

    medicines = Patient.objects.all()
    context={
        "medicines":medicines
    }
    return render(request,"dashboard.html",context)

# hasta sayfası
@login_required(login_url='user:login')
def addpatient(request):
    form=PatientForm(request.POST or None)

    if form.is_valid():

        medicine=form.save(commit=False)
        medicine.first_name
        medicine.save()

        messages.success(request,"Hasta kaydı başarıyla oluşturuldu")
        return redirect("/medicines/dashboard/")

    return render(request,"addpatient.html",{"form":form})

@login_required(login_url='user:login')
def deletePatient(request, id):
    patient = get_object_or_404(Patient, id = id)
    patient.delete()
    messages.success(request, 'Hasta başarıyla silindi.')

    return redirect('medicine:dashboard')

@login_required(login_url='user:login')
def deleteRecete(request, id):
    recete = get_object_or_404(Recete, id = id)
    recete.delete()
    messages.success(request, 'Reçete başarıyla silindi.')

    return redirect('medicine:recetelistesi')

# recete sayfası
@login_required(login_url='user:login')
def receteolustur(request):
    form=ReceteForm()
    if request.method=="POST":
        form=ReceteForm(request.POST)

        if form.is_valid():
            form.save()
            form.save()
            messages.success(request,"Reçete başarıyla oluşturuldu")
            return redirect("medicine:dashboard")

    context={"form":form}
    return render(request,"receteolustur.html",context)

# ilac listesi
@login_required(login_url='user:login')
def ilacListesi(request):
    ilaclar=Medicine.objects.all()
    context={
        "ilaclar":ilaclar
    }
    return render(request,"ilaclistesi.html",context)

# recete listesi
@login_required(login_url='user:login')
def receteListesi(request):
    recete=Recete.objects.filter()

    context={
        "recete":recete,
        
    }
    return render(request,"recetelistesi.html",context)

# detay sayfası
@login_required(login_url='user:login')
def deTail(request,id):
    medicine= Recete.objects.filter(id=id).first()
    medicine = get_object_or_404(Recete, id = id)
    message= Recete.objects.filter(id=id)

    if request.method=="POST":
        mail= message.values_list('hasta__mail',flat=True).first()
        patient=message.values_list('hasta__first_name',flat=True).first()
        qr_code=message.values_list('qr_code',flat=True).first()
        total=message.values_list('toplam',flat=True).first()
        
        filename = "/home/ersel/Documents/GitHub/Django_SmartPharmacy/smartPharmacy/uploads/" + qr_code
        attachment = open(filename,'rb')
        subject='İlaçlarınızı eczane otomatından almayı unutmayınız.\nToplam Tutar: {} TL'.format(total)
        msg = EmailMultiAlternatives(
            "Sayın,"+ patient +" Reçeteniz ",
            subject,
            settings.EMAIL_HOST_USER,
            [mail],
            headers={'Message-ID': 'foo'},
        )
        if attachment:
            mime_image = MIMEImage(attachment.read())
            mime_image.add_header('Content-ID', '<attachment>')
            msg.attach(mime_image)
       
        msg.send()

        messages.success(request,"Mail başarıyla gönderildi")
        
        return redirect("medicine:dashboard")
    context={
        "medicine":medicine,
        }
        
    return render(request,"detail.html",context)
