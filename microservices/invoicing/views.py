from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
import datetime
from users.views import UserView

# Create your views here.

class AddProductsView(APIView):
    def post(self,request):
        view = UserView()
        user = view.get(request)
        if not user:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        

        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message" : "Incorrect Format of Data Applied."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        Product.objects.create(**serializer.data)

        return Response({"message" : "Product Successfully Created"}, status=status.HTTP_200_OK)

class ProcessOrderView(APIView):
    def post(self, request):
        view = UserView()
        user = view.get(request)
        if not user:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        

        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        order_data = serializer.validated_data
        order = Order.objects.create(customer_name=order_data['customer_name'], date=datetime.datetime.now())

        for item_data in order_data['order_items']:
            
            # Check for validation
            if item_data['quantity'] > item_data['product'].stock:
                order.delete()
                return Response({"Quantity is greater than the stock in existance."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

            item_data['product'].stock -= item_data['quantity']
            item_data['product'].save()

            OrderItem.objects.create(order=order, product=item_data['product'], quantity=item_data['quantity'])
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)