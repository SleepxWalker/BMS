from django import template
from tasks.models import Task
from projects.models import Project
from pos.models import Sale
from inventory.models import InventoryTransaction



register = template.Library()

@register.filter
def activity_icon(obj):
    if isinstance(obj, Task):
        return "check2-square"
    elif isinstance(obj, Project):
        return "kanban"
    elif isinstance(obj, Sale):
        return "cash-coin"
    elif isinstance(obj, InventoryTransaction):
        return "arrow-left-right"
    return "question-circle"

@register.filter
def activity_description(obj):
    if isinstance(obj, Task):
        return f"Task created: {obj.task_name}"
    elif isinstance(obj, Project):
        return f"Project created: {obj.title}"
    elif isinstance(obj, Sale):
        return f"Sale recorded: {obj.total_amount} ₪"
    elif isinstance(obj, InventoryTransaction):
        return f"Inventory {obj.get_transaction_type_display()}: {obj.quantity_changed} × {obj.item.product_name}"
    return str(obj)

@register.filter
def get_total_task_time(task):
    return total_task_time(task)