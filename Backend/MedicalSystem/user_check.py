def is_logged(user):
    return user.is_authenticated


def is_user(user):
    return user.is_authenticated and hasattr(user, 'id')


def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'doctor_id')


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'admin_id')
