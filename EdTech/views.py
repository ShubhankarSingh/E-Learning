from django.views.generic import TemplateView
from django.shortcuts import render, redirect 
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
model = apps.get_model('courses', 'Course')

import razorpay

class HomePage(TemplateView):
    template_name = 'index.html'


def pay_with_razor(request, slug):
    if request.method == "POST":
        amount = 5000
        
        client = razorpay.Client(
            auth=("TEST_KEY", "SECRET_KEY"))
        
        client.set_app_details({"title" : "Django", "version" : "3.0"})

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
    context = {'slug':slug}
    return render(request, 'pay_index.html', context)

@csrf_exempt
def success_payment(request, slug):
    this_course = model.objects.get(slug=slug)
    this_course.add_user_to_list_of_students(user=request.user)
    return render(request, "pay_success.html")