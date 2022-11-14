from django.contrib.auth import get_user_model


USER_MODEL = get_user_model()


def get_full_name(self):
    return f"{self.first_name} {self.last_name}"


# Inject get_full_name method instead of __str__ to User model
USER_MODEL.add_to_class("__str__", get_full_name)