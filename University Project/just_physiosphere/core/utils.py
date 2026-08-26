from datetime import timedelta, date
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment, Therapist, Payment, AuditLog

THERAPIST_DEFAULT_DAILY_LIMIT = 12

def is_therapist_available(therapist: Therapist, start_time, end_time):
    # Check vacation
    local_date = start_time.date().isoformat()
    if local_date in (therapist.unavailable_dates or []):
        return False, "Therapist is unavailable on this date."

    # Daily limit
    day_start = timezone.make_aware(timezone.datetime.combine(start_time.date(), timezone.datetime.min.time()))
    day_end = day_start + timedelta(days=1)
    daily_count = Appointment.objects.filter(
        therapist=therapist,
        start_time__gte=day_start,
        start_time__lt=day_end,
        status__in=['pending_offline_verification', 'confirmed', 'pending_online_payment']
    ).count()
    limit = therapist.daily_limit or THERAPIST_DEFAULT_DAILY_LIMIT
    if daily_count >= limit:
        return False, "Therapist has reached the daily appointment limit."

    # Overlap check
    overlapping = Appointment.objects.filter(
        therapist=therapist,
        start_time__lt=end_time,
        end_time__gt=start_time,
        status__in=['pending_offline_verification', 'confirmed', 'pending_online_payment']
    ).exists()
    if overlapping:
        return False, "Selected time overlaps with another appointment."

    return True, ""


def calculate_price_for_appointment(patient, is_student):
    attended_count = Appointment.objects.filter(
        patient=patient,
        attended=True
    ).count()

    if is_student:
        if attended_count == 0:
            return 200
        else:
            return 100
    else:
        if attended_count == 0:
            return 300
        else:
            return 200


def create_payment(appointment, amount, method):
    payment = Payment.objects.create(
        appointment=appointment,
        amount=amount,
        method=method,
        status='initiated'
    )
    appointment.payment_id = payment.id
    appointment.save(update_fields=['payment_id'])
    return payment


def simulate_online_payment(payment: Payment):
    # Stub for real gateway.
    payment.status = 'success'
    payment.txn_id = f"SIM-{payment.id}"
    payment.gateway_response = "Simulated successful payment."
    payment.save()
    appt = payment.appointment
    appt.status = 'confirmed'
    appt.save()
    return payment


def handle_offline_payment(appointment, payment):
    # Cash payment to be verified later.
    appointment.status = 'pending_offline_verification'
    appointment.save()
    payment.status = 'initiated'
    payment.save()


def refund_payment(appointment: Appointment, reason=""):
    payment = getattr(appointment, 'payment', None)
    if payment and payment.status == 'success':
        payment.status = 'refunded'
        payment.gateway_response += f"\nRefunded: {reason}"
        payment.save()
    appointment.status = 'refunded'
    appointment.save()


def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@just-physiosphere.local'),
        recipient_list,
        fail_silently=True
    )


def log_action(actor, action, target_table, target_id=None):
    AuditLog.objects.create(
        actor=actor if actor and actor.is_authenticated else None,
        action=action,
        target_table=target_table,
        target_id=target_id
    )


def can_modify_appointment(appointment, now=None):
    if not now:
        now = timezone.now()
    delta = appointment.start_time - now
    return delta.total_seconds() > 24 * 3600