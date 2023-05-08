import razorpay
import uuid
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from modules.accounts.models import User, Slot
from modules.payments.models import Payment
from modules.appointments.models import Appointment
from modules.recommender.choices import symptoms
from modules.recommender.service import predict_disease


@login_required
def recommender(request):
    if request.method == "POST":
        first_symptom = request.POST.get("first_symptom")
        second_symptom = request.POST.get("second_symptom")
        third_symptom = request.POST.get("third_symptom")

        disease = predict_disease([first_symptom, second_symptom, third_symptom])
        doctors = User.objects.filter(is_doctor=True, specializations__disease=disease)

        context = {
            "prediction": True,
            "disease": disease,
            "doctors": doctors,
            "symptoms": symptoms,
        }
        return render(request, "patients/recommender.html", context)

    context = {"symptoms": symptoms, "prediction": False}
    return render(request, "patients/recommender.html", context)


@login_required
def appointments_list(request):
    appointments = Appointment.objects.filter(
        patient=request.user, is_approved=True, payment__status=Payment.Status.SUCCESS
    ).select_related("doctor", "payment")
    context = {"appointments": appointments}
    return render(request, "patients/appointments/list.html", context)


@login_required
def appointments_create(request):
    doctor_id = request.GET.get("doctor_id")
    doctor = get_object_or_404(User, id=doctor_id, is_doctor=True)
    start_date = timezone.now()
    end_date = timezone.now() + timezone.timedelta(days=7)

    slots = Slot.objects.filter(
        user=doctor, date__range=(start_date, end_date)
    ).order_by("date")

    context = {"doctor": doctor, "slots": slots}
    return render(request, "patients/appointments/create.html", context)


@login_required
def appointments_checkout(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)
    doctor = slot.user
    _client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    amount = int(doctor.consulting_fees) * 100
    order = _client.order.create(
        {
            "amount": amount,
            "currency": "INR",
            "receipt": "receipt#1",
            "partial_payment": False,
        }
    )
    payment = Payment.objects.create(
        user=request.user, amount=amount, transaction_id=uuid.uuid4().hex
    )
    context = {
        "order": order,
        "slot": slot,
        "doctor": doctor,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "callback_url": "http://127.0.0.1:8000"
        + reverse("appointments-confirm", args=[slot.id])
        + "?transaction_id="
        + payment.transaction_id,
    }
    return render(request, "patients/appointments/checkout.html", context)


@csrf_exempt
@login_required
def appointments_confirm(request, slot_id):
    payment_id = request.POST.get("razorpay_payment_id")
    transaction_id = request.GET.get("transaction_id")

    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    slot = get_object_or_404(Slot, id=slot_id)

    payment.payment_id = payment_id
    payment.status = Payment.Status.SUCCESS
    payment.save()

    appointment = Appointment.objects.create(
        patient=request.user,
        doctor=slot.user,
        date=slot.date,
        start_time=slot.start_time,
        end_time=slot.end_time,
        is_approved=True,
        payment=payment,
    )

    context = {
        "appointment": appointment,
        "payment": payment,
        "slot": slot,
        "doctor": slot.user,
    }
    return render(request, "patients/appointments/confirm.html", context)
