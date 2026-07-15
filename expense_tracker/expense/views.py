from django.shortcuts import render,get_object_or_404,redirect
from .models import Transaction
# Create your views here.

from django.db.models import Sum

def expenses_list(request):
    expenses = Transaction.objects.all()
    total_balance = 0

    month = request.GET.get('month', '').strip()
    year = request.GET.get('year', '').strip()

    if month and year:
        expenses = expenses.filter(
            date__month=month,
            date__year=year
        )

    total_income = sum(
        expense.amount
        for expense in expenses
        if expense.type == "Income"
    )

    total_expense = sum(
        expense.amount
        for expense in expenses
        if expense.type == "Expense"
    )

    total_balance = total_income - total_expense

    return render(request, "expenses_list.html", {
        "expenses": expenses,
        "total_balance": total_balance,
    })

def add_expense(request):
    if request.method=='POST':
        title=request.POST.get('title')
        amount=request.POST.get('amount')
        type=request.POST.get('type')
        category=request.POST.get('category')
        Transaction.objects.create(title=title,amount=amount,type=type,category=category)
        return redirect('expenses_list')
    return render(request,'add_expense.html')

def update_expense(request,pk):
    expense=get_object_or_404(Transaction,pk=pk)
    if request.method=='POST':
        expense.title=request.POST.get('title')
        expense.amount=request.POST.get('amount')
        expense.type=request.POST.get('type')
        expense.category=request.POST.get('category')
        expense.save()
        return redirect('expenses_list')
    return render(request,"update_expense.html",{"expense":expense})

def delete_expense(request,pk):
    expense=get_object_or_404(Transaction,pk=pk)
    if request.method=='POST':
        expense.delete()
        return redirect('expenses_list')
    return render(request,'delete_expense.html',{"expense":expense})



    