from django.db import models
from organizations.models import Organization
from employees.models import Employee
from departments.models import Department
from positions.models import Position


class TransferOrder(models.Model):
    """Приказ о перемещении (форма Т-5а)."""
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name="Организация"
    )
    document_number = models.CharField("Номер документа", max_length=50)
    document_date = models.DateField("Дата составления")

    class Meta:
        verbose_name = "Приказ о перемещении"
        verbose_name_plural = "Приказы о перемещении"
        ordering = ['-document_date']

    def __str__(self):
        return f"Приказ №{self.document_number} от {self.document_date}"


class TransferOrderItem(models.Model):
    """Строка приказа (сотрудник)."""
    TRANSFER_TYPES = [
        ('permanent', 'Постоянно'),
        ('temporary', 'Временно'),
    ]

    order = models.ForeignKey(
        TransferOrder, on_delete=models.CASCADE, related_name='items', verbose_name="Приказ"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, verbose_name="Сотрудник"
    )
    tab_number = models.CharField("Табельный номер", max_length=20)
    
    # Структурные подразделения
    old_department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='transfers_from', verbose_name="Прежнее подразделение"
    )
    new_department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='transfers_to', verbose_name="Новое подразделение"
    )
    
    # Должности
    old_position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name='transfers_from_pos', verbose_name="Прежняя должность"
    )
    new_position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name='transfers_to_pos', verbose_name="Новая должность"
    )
    
    # Оклады
    old_salary = models.DecimalField("Прежний оклад", max_digits=10, decimal_places=2, default=0)
    new_salary = models.DecimalField("Новый оклад", max_digits=10, decimal_places=2, default=0)
    
    transfer_type = models.CharField("Вид перевода", max_length=20, choices=TRANSFER_TYPES, default='permanent')
    date_from = models.DateField("С")
    date_to = models.DateField("По", blank=True, null=True)
    
    # Основание
    basis_document = models.CharField("Основание (документ)", max_length=255)
    basis_date = models.DateField("Дата основания")

    class Meta:
        verbose_name = "Позиция приказа"
        verbose_name_plural = "Позиции приказа"

    def __str__(self):
        return f"{self.employee} -> {self.new_position}"