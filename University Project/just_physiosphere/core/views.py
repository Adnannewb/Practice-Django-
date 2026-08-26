from datetime import datetime, time, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db import transaction
from django.contrib import messages  # Django messages framework

from .models import (
    User,
    Therapist,
    Service,
    Appointment,
    MedicalCard,
    Visit,
    Message,
    Payment,
)
from .forms import (
    RegistrationForm,
    LoginForm,
    AppointmentForm,
    ContactForm,
    TherapistProfileForm,
    TherapistUnavailableForm,
    VisitForm,
)
from .utils import (
    is_therapist_available,
    calculate_price_for_appointment,
    create_payment,
    simulate_online_payment,
    handle_offline_payment,
    refund_payment,
    send_notification_email,
    log_action,
    can_modify_appointment,
)


# ------------------------- Public pages ------------------------- #

def home(request):
    services = Service.objects.all()[:3]
    return render(request, "home.html", {"services": services})


def services_view(request):
    services = Service.objects.all().order_by("name")
    therapists = (
        Therapist.objects.select_related("user")
        .filter(user__is_active=True)
        .order_by("user__first_name")
    )
    return render(
        request,
        "services.html",
        {
            "services": services,
            "therapists": therapists,
        },
    )


def about_view(request):
    return render(request, "about.html")


def faq_view(request):
    return render(request, "faq.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            log_action(
                None,
                f"Contact message created: {msg.subject}",
                "messages",
                msg.id,
            )
            messages.success(request, "Thank you! Your message has been received.")
            return render(
                request, "contact.html", {"form": ContactForm(), "success": True}
            )
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


# ------------------------- Auth ------------------------- #

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_redirect")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            MedicalCard.objects.get_or_create(patient=user)
            log_action(user, "User registered", "users", user.id)
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("dashboard_redirect")
    else:
        form = RegistrationForm()
    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_redirect")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            log_action(user, "User logged in", "users", user.id)
            messages.success(request, "Login successful.")
            return redirect("dashboard_redirect")
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    log_action(
        request.user,
        "User logged out",
        "users",
        request.user.id if request.user.is_authenticated else None,
    )
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


# ------------------------- Dashboard routing ------------------------- #

@login_required
def dashboard_redirect(request):
    if request.user.role == "therapist" and hasattr(request.user, "therapist_profile"):
        return redirect("therapist_dashboard")
    elif request.user.role == "admin" or request.user.is_staff or request.user.is_superuser:
        return redirect("admin_dashboard")
    else:
        return redirect("user_dashboard")


# ------------------------- Patient dashboard ------------------------- #

@login_required
def user_dashboard(request):
    patient = request.user

    upcoming = (
        Appointment.objects.filter(
            patient=patient,
            start_time__gte=timezone.now(),
            status__in=[
                "pending_offline_verification",
                "confirmed",
                "pending_online_payment",
            ],
        )
        .select_related("therapist__user", "service")
        .order_by("start_time")
    )

    past = (
        Appointment.objects.filter(
            patient=patient,
            start_time__lt=timezone.now(),
            status__in=["completed", "refunded", "cancelled"],
        )
        .select_related("therapist__user", "service")
        .order_by("-start_time")[:10]
    )

    medical_card, _ = MedicalCard.objects.get_or_create(patient=patient)
    visits = (
        Visit.objects.filter(appointment__patient=patient)
        .select_related("appointment__therapist__user", "appointment__service")
        .order_by("-appointment__start_time")
    )

    if request.method == "POST" and "create_appointment" in request.POST:
        form = AppointmentForm(request.POST, user=patient)
        if form.is_valid():
            with transaction.atomic():
                therapist = form.cleaned_data["therapist"]
                service = form.cleaned_data["service"]
                start_time = form.cleaned_data["start_time"]
                duration = timedelta(minutes=service.duration_minutes)
                end_time = start_time + duration

                ok, msg = is_therapist_available(therapist, start_time, end_time)
                if not ok:
                    # therapist unavailable, daily limit exceeded, or overlap
                    form.add_error(None, msg)
                    messages.error(request, msg)
                else:
                    appointment = Appointment.objects.create(
                        patient=patient,
                        therapist=therapist,
                        service=service,
                        start_time=start_time,
                        end_time=end_time,
                        payment_method=form.cleaned_data["payment_method"],
                    )

                    amount = calculate_price_for_appointment(patient, patient.is_student)
                    payment = create_payment(
                        appointment, amount, form.cleaned_data["payment_method"]
                    )

                    if form.cleaned_data["payment_method"] == "online":
                        simulate_online_payment(payment)
                    else:
                        handle_offline_payment(appointment, payment)

                    log_action(
                        patient, "Appointment created", "appointments", appointment.id
                    )
                    send_notification_email(
                        "Appointment Request Received",
                        f"Dear {patient.first_name}, your appointment request has been received.",
                        [patient.email],
                    )
                    messages.success(
                        request,
                        "Your appointment request has been submitted successfully.",
                    )
                    return redirect("user_dashboard")
    else:
        form = AppointmentForm(user=patient)

    return render(
        request,
        "dashboards/user_dashboard.html",
        {
            "upcoming_appointments": upcoming,
            "past_appointments": past,
            "medical_card": medical_card,
            "visits": visits,
            "appointment_form": form,
        },
    )


@login_required
def user_cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if not can_modify_appointment(appointment):
        return HttpResponseForbidden(
            "Cannot cancel within 24 hours of appointment."
        )

    refund_payment(appointment, reason="User cancelled")
    appointment.status = "cancelled"
    appointment.save()

    send_notification_email(
        "Appointment Cancelled",
        f"Your appointment on {appointment.start_time} has been cancelled and refunded if applicable.",
        [request.user.email],
    )
    log_action(request.user, "User cancelled appointment", "appointments", appointment.id)
    messages.success(request, "Your appointment has been cancelled.")
    return redirect("user_dashboard")


@login_required
def user_reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if not can_modify_appointment(appointment):
        return HttpResponseForbidden(
            "Cannot reschedule within 24 hours of appointment."
        )

    if request.method == "POST":
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            therapist = form.cleaned_data["therapist"]
            service = form.cleaned_data["service"]
            start_time = form.cleaned_data["start_time"]
            duration = timedelta(minutes=service.duration_minutes)
            end_time = start_time + duration

            ok, msg = is_therapist_available(therapist, start_time, end_time)
            if not ok:
                form.add_error(None, msg)
                messages.error(request, msg)
            else:
                appointment.therapist = therapist
                appointment.service = service
                appointment.start_time = start_time
                appointment.end_time = end_time
                appointment.status = "confirmed"
                appointment.save()

                log_action(
                    request.user,
                    "User rescheduled appointment",
                    "appointments",
                    appointment.id,
                )
                send_notification_email(
                    "Appointment Rescheduled",
                    f"Your appointment has been rescheduled to {appointment.start_time}.",
                    [request.user.email],
                )
                messages.success(request, "Your appointment has been rescheduled.")
                return redirect("user_dashboard")
    else:
        form = AppointmentForm(
            user=request.user,
            initial={
                "therapist": appointment.therapist,
                "service": appointment.service,
                "start_time": appointment.start_time,
            },
        )

    # For simplicity reuse user_dashboard template to show form
    return render(
        request,
        "dashboards/user_dashboard.html",
        {
            "reschedule_form": form,
            "rescheduling": appointment,
        },
    )


# ------------------------- Therapist dashboard ------------------------- #

def therapist_required(view_func):
    return login_required(
        user_passes_test(
            lambda u: u.role == "therapist" and hasattr(u, "therapist_profile")
        )(view_func)
    )


@therapist_required
def therapist_dashboard(request):
    therapist = request.user.therapist_profile

    # Compute explicit local-day range for "today"
    today_date = timezone.localdate()
    tz = timezone.get_current_timezone()
    day_start = timezone.make_aware(datetime.combine(today_date, time.min), tz)
    day_end = day_start + timedelta(days=1)

    def get_todays():
        return (
            Appointment.objects.filter(
                therapist=therapist,
                start_time__gte=day_start,
                start_time__lt=day_end,
            )
            .select_related("patient", "service")
            .order_by("start_time")
        )

    def get_upcoming():
        return (
            Appointment.objects.filter(
                therapist=therapist,
                start_time__gte=timezone.now(),
                status__in=[
                    "pending_offline_verification",
                    "confirmed",
                    "pending_online_payment",
                ],
            )
            .select_related("patient", "service")
            .order_by("start_time")
        )

    def get_offline():
        return (
            Appointment.objects.filter(
                therapist=therapist,
                status="pending_offline_verification",
            )
            .select_related("patient", "service")
            .order_by("start_time")
        )

    # Default forms
    profile_form = TherapistProfileForm(instance=therapist)
    unavailable_form = TherapistUnavailableForm(instance=therapist)

    todays_appointments = get_todays()
    upcoming_appointments = get_upcoming()
    offline_appointments = get_offline()

    if request.method == "POST":
        # Update profile
        if "update_profile" in request.POST:
            profile_form = TherapistProfileForm(request.POST, request.FILES, instance=therapist)
            if profile_form.is_valid():
                profile_form.save()
                log_action(
                    request.user,
                    "Therapist profile updated",
                    "therapists",
                    therapist.id,
                )
                messages.success(request, "Profile updated successfully.")

        # Update unavailable dates
        elif "update_unavailable" in request.POST:
            unavailable_form = TherapistUnavailableForm(
                request.POST, instance=therapist
            )
            if unavailable_form.is_valid():
                unavailable_form.save()
                log_action(
                    request.user,
                    "Therapist unavailable dates updated",
                    "therapists",
                    therapist.id,
                )
                messages.success(request, "Unavailable dates updated.")

        # Mark session completed (attendance)
        elif "mark_completed" in request.POST:
            appt_id = request.POST.get("appointment_id")
            appointment = get_object_or_404(
                Appointment, id=appt_id, therapist=therapist
            )
            appointment.attended = True
            appointment.status = "completed"
            appointment.save()

            # Create a visit entry if not present
            visit, created = Visit.objects.get_or_create(appointment=appointment)
            if created:
                visit.notes = ""
                visit.signed = False
                visit.save()

            # Update medical card summary with a simple log line
            mc, _ = MedicalCard.objects.get_or_create(patient=appointment.patient)
            line = (
                f"{timezone.localdate().isoformat()}: "
                f"{appointment.service.name} session completed with "
                f"{therapist.user.get_full_name()}."
            )
            if mc.summary:
                mc.summary += f"\n{line}"
            else:
                mc.summary = line
            mc.save()

            log_action(
                request.user,
                "Appointment marked completed",
                "appointments",
                appointment.id,
            )
            messages.success(request, "Session marked as completed.")

        # Cancel with refund
        elif "cancel_with_refund" in request.POST:
            appt_id = request.POST.get("appointment_id")
            appointment = get_object_or_404(
                Appointment, id=appt_id, therapist=therapist
            )
            refund_payment(appointment, reason="Cancelled by therapist")
            appointment.status = "cancelled"
            appointment.save()
            send_notification_email(
                "Appointment Cancelled by Therapist",
                f"Your appointment on {appointment.start_time} has been cancelled by the therapist.",
                [appointment.patient.email],
            )
            log_action(
                request.user,
                "Therapist cancelled appointment",
                "appointments",
                appointment.id,
            )
            messages.success(request, "Appointment cancelled and refund processed.")

        # Confirm cash (offline) payment
        elif "confirm_cash" in request.POST:
            appt_id = request.POST.get("appointment_id")
            appointment = get_object_or_404(
                Appointment, id=appt_id, therapist=therapist
            )
            payment = getattr(appointment, "payment", None)
            if payment and payment.method == "cash":
                payment.status = "success"
                payment.gateway_response = (payment.gateway_response or "") + (
                    "\nCash payment verified at clinic."
                )
                payment.save()
                appointment.status = "confirmed"
                appointment.save()
                log_action(
                    request.user,
                    "Offline cash payment verified",
                    "payments",
                    payment.id,
                )
                messages.success(request, "Cash payment confirmed.")

        # Refresh querysets after any POST action
        todays_appointments = get_todays()
        upcoming_appointments = get_upcoming()
        offline_appointments = get_offline()

    return render(
        request,
        "dashboards/therapist_dashboard.html",
        {
            "todays_appointments": todays_appointments,
            "upcoming_appointments": upcoming_appointments,
            "offline_appointments": offline_appointments,
            "profile_form": profile_form,
            "unavailable_form": unavailable_form,
        },
    )


@therapist_required
def therapist_edit_visit(request, appointment_id):
    therapist = request.user.therapist_profile
    appointment = get_object_or_404(
        Appointment, id=appointment_id, therapist=therapist
    )
    visit, _ = Visit.objects.get_or_create(appointment=appointment)
    medical_card, _ = MedicalCard.objects.get_or_create(patient=appointment.patient)

    if request.method == "POST":
        form = VisitForm(request.POST, request.FILES, instance=visit)
        if form.is_valid():
            form.save()
            # Update medical card summary if provided
            summary = request.POST.get("medical_summary", "").strip()
            if summary:
                medical_card.summary = summary
                medical_card.save()
            log_action(request.user, "Visit notes updated", "visits", visit.id)
            messages.success(request, "Visit notes updated.")
            return redirect("therapist_dashboard")
    else:
        form = VisitForm(instance=visit)

    return render(
        request,
        "dashboards/therapist_visit_form.html",
        {
            "appointment": appointment,
            "visit_form": form,
            "medical_card": medical_card,
        },
    )


# ------------------------- Admin dashboard ------------------------- #

def admin_required(view_func):
    return login_required(
        user_passes_test(lambda u: u.role == "admin" or u.is_superuser)(view_func)
    )


@admin_required
def admin_dashboard(request):
    users = User.objects.all().select_related("therapist_profile")
    therapists = Therapist.objects.all().select_related("user")
    services = Service.objects.all()
    appointments = Appointment.objects.select_related(
        "patient", "therapist__user", "service"
    )[:50]
    payments = Payment.objects.select_related("appointment")[:50]
    contact_messages = Message.objects.order_by("-created_at")[:20]

    return render(
        request,
        "dashboards/admin_dashboard.html",
        {
            "users": users,
            "therapists": therapists,
            "services": services,
            "appointments": appointments,
            "payments": payments,
            "messages": contact_messages,
        },
    )


@admin_required
def admin_toggle_therapist(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.role != "therapist":
        user.role = "therapist"
        user.save()
        Therapist.objects.get_or_create(
            user=user,
            defaults={
                "qualifications": "",
                "specialization": "",
                "bio": "",
            },
        )
    else:
        user.role = "patient"
        user.save()
        Therapist.objects.filter(user=user).delete()
    log_action(request.user, "Admin toggled therapist role", "users", user.id)
    messages.success(request, "Therapist role updated.")
    return redirect("admin_dashboard")


@admin_required
def admin_service_crud(request):
    if request.method == "POST":
        name = request.POST.get("name")
        duration = int(request.POST.get("duration", 30))
        price = float(request.POST.get("price", 0))
        desc = request.POST.get("description", "")
        Service.objects.create(
            name=name,
            duration_minutes=duration,
            price=price,
            description=desc,
        )
        messages.success(request, "Service added successfully.")
    return redirect("admin_dashboard")


# ------------------------- Therapist services API ------------------------- #

def api_therapist_services(request):
    """
    Return list of services for a given therapist.
    If therapist has no specific services selected, fall back to all services.
    """
    therapist_id = request.GET.get("therapist_id")
    if not therapist_id:
        return JsonResponse({"services": [], "error": "Missing therapist_id"}, status=400)

    try:
        therapist = Therapist.objects.get(id=therapist_id)
    except Therapist.DoesNotExist:
        return JsonResponse({"services": [], "error": "Therapist not found"}, status=404)

    qs = therapist.services.all()
    if not qs.exists():
        qs = Service.objects.all()

    data = [{"id": s.id, "name": s.name} for s in qs]
    return JsonResponse({"services": data})


# ------------------------- Available slots API ------------------------- #

def api_available_slots(request):
    """
    Return available 1-hour slots for a therapist on a given date.

    Rules:
    - Workday starts at 9:00
    - 13:00–14:00 is lunch break (skipped)
    - 17:00–18:00 is an evening break/snack (skipped)
    - We generate consecutive 1-hour slots starting 9:00,
      skipping 13:00 and 17:00, until we reach therapist.daily_limit
      or we run out of hours in the day.
    - Removes slots already booked / unavailable (uses is_therapist_available)
    - Skips past times on the current day
    """
    therapist_id = request.GET.get("therapist_id")
    service_id = request.GET.get("service_id")
    date_str = request.GET.get("date")  # YYYY-MM-DD

    if not therapist_id or not service_id or not date_str:
        return JsonResponse(
            {"slots": [], "error": "Missing parameters (therapist_id, service_id, date)."},
            status=400,
        )

    try:
        therapist = Therapist.objects.get(id=therapist_id)
        service = Service.objects.get(id=service_id)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except Therapist.DoesNotExist:
        return JsonResponse({"slots": [], "error": "Therapist not found."}, status=404)
    except Service.DoesNotExist:
        return JsonResponse({"slots": [], "error": "Service not found."}, status=404)
    except ValueError:
        return JsonResponse(
            {"slots": [], "error": "Invalid date format (expected YYYY-MM-DD)."},
            status=400,
        )

    tz = timezone.get_current_timezone()
    daily_limit = therapist.daily_limit or 12

    now = timezone.now()
    slots = []

    start_hour = 9          # 9:00 AM
    max_hour = 23           # last start at 23:00 (23-24)

    hour = start_hour
    while hour <= max_hour and len(slots) < daily_limit:
        # Skip lunch 13:00–14:00 and snack 17:00–18:00
        if hour in (13, 17):
            hour += 1
            continue

        start_naive = datetime.combine(date_obj, time(hour=hour, minute=0))
        start_dt = timezone.make_aware(start_naive, tz)

        # Skip past times on the current day
        if start_dt <= now:
            hour += 1
            continue

        end_dt = start_dt + timedelta(minutes=service.duration_minutes)

        ok, _ = is_therapist_available(therapist, start_dt, end_dt)
        if ok:
            label_start = start_dt.strftime("%I:%M %p").lstrip("0")
            label_end = (start_dt + timedelta(hours=1)).strftime("%I:%M %p").lstrip("0")
            slots.append(
                {
                    "start_iso": start_dt.strftime("%Y-%m-%d %H:%M"),
                    "label": f"{label_start} - {label_end}",
                }
            )

        hour += 1  # move to next potential hour

    if not slots:
        return JsonResponse(
            {"slots": [], "error": "No available time slots for this date."}
        )

    return JsonResponse({"slots": slots})


# ------------------------- Live serial API ------------------------- #

def api_live_serial(request):
    now = timezone.now()
    upcoming = (
        Appointment.objects.filter(
            start_time__gte=now,
            status__in=[
                "pending_offline_verification",
                "confirmed",
                "pending_online_payment",
            ],
        )
        .select_related("patient", "therapist__user")
        .order_by("start_time")[:5]
    )

    data = []
    for appt in upcoming:
        data.append(
            {
                "id": appt.id,
                "patient": appt.patient.get_full_name() or appt.patient.username,
                "therapist": (
                    appt.therapist.user.get_full_name()
                    if appt.therapist and appt.therapist.user
                    else ""
                ),
                "start_time": appt.start_time.isoformat(),
            }
        )
    return JsonResponse({"appointments": data})