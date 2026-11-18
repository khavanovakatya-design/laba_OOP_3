import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        errors = []

        if len(password) < self.min_length:
            errors.append(
                _("Пароль должен содержать минимум %(min_length)d символов.")
                % {'min_length': self.min_length}
            )

        if not re.search(r'[A-ZА-Я]', password):
            errors.append(_("Пароль должен содержать хотя бы одну заглавную букву."))

        if not re.search(r'[a-zа-я]', password):
            errors.append(_("Пароль должен содержать хотя бы одну строчную букву."))

        if not re.search(r'\d', password):
            errors.append(_("Пароль должен содержать хотя бы одну цифру."))

        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>/?]', password):
            errors.append(_("Пароль должен содержать хотя бы один спецсимвол."))

        if ' ' in password:
            errors.append(_("Пароль не должен содержать пробелов."))

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            "Пароль должен содержать минимум %(min_length)d символов, "
            "включая заглавные и строчные буквы, цифры и спецсимволы. "
            "Пробелы запрещены."
        ) % {'min_length': self.min_length}