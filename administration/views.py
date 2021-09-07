from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.models import User
from administration.models import Commission
from datetime import datetime

from month import Month
# Create your views here.

def commissions(request, year):
    months = Month(year, 1).range(Month(year, 12))
    users = User.objects.filter(is_active=True)

    employees = {user:Commission.objects.get_from_user_and_months(user, months) for user in users}
    employees = {user:data for user, data in employees.items() if len([d for d in data.values() if d is not None]) != 0} #1 Weil Gesamt immer 0 ist

    for name in employees.keys():
        e = employees[name]
        e['sum'] = sum([v.amount for v in e.values() if v is not None])

    print(employees)

    context = {
        'year': year,
        'months': months,
        'employees': employees
    }
    return render(request, 'administration/commissions.html', context)

def commissions_without_year(request):
    return redirect('administration:commissions_with_year', year=datetime.now().year)


#javascript views

def json_commission(request, commission_id):
    try:
        commission = Commission.objects.get(id=commission_id)
    except Commission.DoesNotExist:
        return JsonResponse({'error': 'Commission not found'})

    json = commission.to_json()
    return JsonResponse(json, safe=False)