from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Employees
from .serializers import EmployeesSerializer
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
@csrf_exempt
def employees_handler(request):
    if request.method == 'GET':
        employees = Employees.objects.all()
        serializer = EmployeesSerializer(employees, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = EmployeesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=200)
        return JsonResponse(data=serializer.errors, status=400)
    return JsonResponse({'message': 'Request is not supported'}, status=400)


def get_employees(pk):
    try:
        return {
            'status': 200,
            'employees': employees
        }
    except Employees.DoesNotExist as e:
        return {
            'status': 404,
            'employees': None
        }


@csrf_exempt
def employee_handler(request, pk):
    result = get_employees(pk)

    if result['status'] == 404:
        return JsonResponse({'message': 'Employee not found'}, status=404)

    employee = result['employee']

    if request.method == 'GET':
        serializer = EmployeesSerializer(employee)
        return JsonResponse(serializer.data, status=200)
    if request.method == 'PUT':
        data = json.loads(request.body)
        serializer = EmployeesSerializer(data=data, instance=employee)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data)
        return JsonResponse(data=serializer.errors, status=400)
    if request.method == 'DELETE':
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully!'})
    return JsonResponse({'message': 'Request is not supported'}, status=400)