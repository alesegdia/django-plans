from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from plans.models import Order, Invoice, UserPlan, Plan
from plans.signals import order_completed, activate_user_plan

from datetime import timedelta

@receiver(post_save, sender=Order)
def create_proforma_invoice(sender, instance, created, **kwargs):
    """
    For every Order if there are defined billing_data creates invoice proforma,
    which is an order confirmation document
    """
    if created:
        Invoice.create(instance, Invoice.INVOICE_TYPES['PROFORMA'])


@receiver(order_completed)
def create_invoice(sender, **kwargs):
    Invoice.create(sender, Invoice.INVOICE_TYPES['INVOICE'])

@receiver(order_completed)
def create_userplan(sender, **kwargs):
    try:
        next_bill = sender.created.replace(month=sender.created.month+1, day=1)
    except ValueError:
        if today.month == 12:
            next_bill = sender.created.replace(year=sender.month.year+1, month=1, day=1)

    end_of_month = (next_bill -timedelta(days=1)).date()
    print('UserPlan creation')
    userplan = UserPlan.objects.create(user = sender.user, plan_id = sender.plan_id, expire = end_of_month)
	# TODO mettre à jour l'order avec le userplan_id
    print('sender.userplan update')
    sender.userplan = userplan
    sender.save()

@receiver(post_save, sender=Invoice)
def send_invoice_by_email(sender, instance, created, **kwargs):
    if created:
        instance.send_invoice_by_email()

@receiver(post_save, sender=User)
def set_default_user_plan(sender, instance, created, **kwargs):
    """
    Creates default plan for the new user but also extending an account for default grace period.
    """
    SET_DEFAULT_USER_PLAN = getattr(settings, 'PLANS_SET_DEFAULT_USER_PLAN', True)
    if created and SET_DEFAULT_USER_PLAN:
        default_plan = Plan.get_default_plan()
        if default_plan is not None:
            UserPlan.objects.create(user=instance, plan=default_plan, active=False, expire=None)


# Hook to django-registration to initialize plan automatically after user has confirm account

@receiver(activate_user_plan)
def initialize_plan_generic(sender, user, **kwargs):
    try:
        user.userplan.initialize()
    except UserPlan.DoesNotExist:
        return


try:
    from registration.signals import user_activated
    @receiver(user_activated)
    def initialize_plan_django_registration(sender, user, request, **kwargs):
        try:
             user.userplan.initialize()
        except UserPlan.DoesNotExist:
            return


except ImportError:
    pass


# Hook to django-getpaid if it is installed
try:
    from getpaid.signals import user_data_query
    @receiver(user_data_query)
    def set_user_email_for_getpaid(sender, order, user_data, **kwargs):
        user_data['email'] = order.user.email
except ImportError:
    pass
