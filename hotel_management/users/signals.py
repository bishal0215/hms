from django.apps import apps
from django.contrib.auth.models import Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


ROLE_PERMISSIONS = {
    'Waiter': [
        'add_order',
        'change_order',
        'view_order',
        'view_orderitem',
        'view_table',
        'view_menuitem',
    ],
    'Kitchen': [
        'change_order',
        'view_order',
        'view_orderitem',
        'view_menuitem',
    ],
    'Cashier': [
        'view_order',
        'view_invoice',
        'add_payment',
        'change_payment',
        'view_payment',
    ],
    'Manager': [],
}


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    if not Permission.objects.exists():
        return

    Role = apps.get_model('users', 'Role')

    for role_name, codenames in ROLE_PERMISSIONS.items():
        role, _ = Role.objects.get_or_create(name=role_name)

        if role_name == 'Manager':
            role.permissions.set(Permission.objects.all())
        else:
            permissions = Permission.objects.filter(codename__in=codenames)
            role.permissions.set(permissions)

        role.save()
