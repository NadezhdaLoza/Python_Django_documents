from django.db import models
from accounts.models import Account


class Organization(models.Model):
    name = models.CharField("Название", max_length=255)
    address = models.CharField("Адрес", max_length=255)
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name="Счёт",
        null=True,
        blank=True,
    )
    chief = models.ForeignKey(
        'employees.Employee',
        on_delete=models.PROTECT,
        verbose_name="Руководитель",
        related_name='organizations_as_chief',
    )
    financial_chief = models.ForeignKey(
        'employees.Employee',
        on_delete=models.PROTECT,
        verbose_name="Главный бухгалтер",
        related_name='organizations_as_financial_chief',
    )

    def __str__(self):
        return self.name

    @staticmethod
    def _short_name(employee):
        if not employee:
            return ''
        middle = f"{employee.middle_name[0]}." if employee.middle_name else ''
        return f"{employee.last_name} {employee.first_name[0]}.{middle}"

    @property
    def chief_short_name(self):
        return self._short_name(self.chief)

    @property
    def accountant_short_name(self):
        return self._short_name(self.financial_chief)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
