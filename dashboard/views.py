from datetime import date, datetime
from collections import defaultdict
from itertools import chain

from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

from clients.models import Client
from projects.models import Project
from tasks.models import Task
from inventory.models import Inventory, InventoryTransaction
from invoices.models import Invoice
from expenses.models import Expense
from pos.models import Sale
from dashboard.utils import ActivityEntry

@login_required()
def dashboard_home(request):
    user = request.user

    # האם להציג דשבורד מלא
    full_dashboard = user.role in ['admin', 'manager']

    # שליפת רשומות מותאמות
    if full_dashboard:
        recent_projects = Project.objects.select_related('client').order_by('-created_at')[:3]
        recent_tasks = Task.objects.select_related('project').order_by('-created_at')[:3]
        recent_sales = Sale.objects.select_related('client').order_by('-sale_date')[:3]
        recent_transactions = InventoryTransaction.objects.select_related('item').order_by('-timestamp')[:3]
    else:
        recent_projects = Project.objects.filter(
            assigned_team=user,
            is_active=True
        ).order_by('-created_at')[:3]

        recent_tasks = Task.objects.filter(
            assigned_to=user,
            is_active=True
        ).order_by('-created_at')[:3]

        recent_sales = []  # עובדים רגילים לא רואים מכירות
        recent_transactions = []  # עובדים רגילים לא רואים תנועות מלאי

    # סיכומי מכירות, חשבוניות והוצאות - רק לאדמין/מנהל
    if full_dashboard:
        sales_summary = Sale.objects.annotate(
            month=TruncMonth('sale_date')
        ).values('month').annotate(
            total_sales=Sum('total_amount')
        ).order_by('month')

        invoices_summary = Invoice.objects.filter(
            status='Paid'
        ).annotate(
            month=TruncMonth('issue_date')
        ).values('month').annotate(
            total_invoices=Sum('total_amount')
        ).order_by('month')

        expenses_summary = Expense.objects.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total_expenses=Sum('amount')
        ).order_by('month')

        # יצירת סיכום חודשי
        months = set()
        sales_lookup, invoices_lookup, expenses_lookup = {}, {}, {}

        for sale in sales_summary:
            months.add(sale['month'])
            sales_lookup[sale['month']] = sale['total_sales'] or 0

        for invoice in invoices_summary:
            months.add(invoice['month'])
            invoices_lookup[invoice['month']] = invoice['total_invoices'] or 0

        for expense in expenses_summary:
            months.add(expense['month'])
            expenses_lookup[expense['month']] = expense['total_expenses'] or 0

        months = sorted([
            m.date() if isinstance(m, datetime) else m
            for m in months if m
        ])

        financial_summary = []
        for month in months:
            total_sales = sales_lookup.get(month, 0)
            total_invoices = invoices_lookup.get(month, 0)
            total_expenses = expenses_lookup.get(month, 0)

            total_income = total_sales + total_invoices
            net_profit = total_income - total_expenses

            financial_summary.append({
                'month': month,
                'total_sales': total_income,
                'total_expenses': total_expenses,
                'net_profit': net_profit,
            })

        sales_total = Sale.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        expenses_total = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0

    else:
        financial_summary = []
        sales_total = 0
        expenses_total = 0

    # פעילות אחרונה
    recent_activity = list(chain(
        [ActivityEntry(f"Project: {p.title}", p.created_at, 'project') for p in recent_projects],
        [ActivityEntry(f"Task: {t.task_name}", t.created_at, 'task') for t in recent_tasks],
    ))
    # (אין מכירות ותנועות מלאי לעובדים רגילים)

    recent_activity = sorted(recent_activity, key=lambda x: x.created_at, reverse=True)[:10]

    # משימות קרובות
    if user.role == 'employee':
        upcoming_tasks = Task.objects.filter(
            due_date__gte=date.today(),
            assigned_to=user
        ).order_by('due_date')[:3]
    else:
        upcoming_tasks = Task.objects.filter(
            due_date__gte=date.today()
        ).order_by('due_date')[:3]

    # בניית הקונטקסט
    context = {
        'client_count': Client.objects.count(),
        'project_count': Project.objects.count(),
        'task_count': Task.objects.filter(status__in=['Pending', 'In Progress']).count(),
        'inventory_count': Inventory.objects.count(),
        'sales_total': sales_total,
        'expenses_total': expenses_total,
        'financial_summary': financial_summary,
        'recent_activity': recent_activity,
        'upcoming_tasks': upcoming_tasks,
        'full_dashboard': full_dashboard,
    }

    # טעינת תבנית מתאימה
    if full_dashboard:
        template = 'dashboard/dashboard.html'
    else:
        template = 'dashboard/_employee_dashboard.html'

    return render(request, template, context)