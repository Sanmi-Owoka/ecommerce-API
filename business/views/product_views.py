from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from business.models import Product
from ..serializers.product_serializer import (
    ProductSerializer,
    GetProductSerializer
)
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, When, Case, Q


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"message": "failure", "data": "null", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            response = GetProductSerializer(request.data)
            return Response(
                {
                    "message": "success",
                    "data": response.data,
                    "errors": "null"
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        try:
            search = request.GET.get('search', None)
            if search:
                search = search.lower()
                products = self.queryset.filter(
                    Q(name__icontains=search)
                    | Q(category__icontains=search)
                )
            else:
                products = self.queryset
            serializer = GetProductSerializer(products, many=True)
            return Response(
                {
                    "message": "success",
                    "data": serializer.data,
                    "errors": "null"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            product_queryset = self.queryset.filter(id=pk)
            if not product_queryset.exists():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"Product with ID:{pk} does not exist"
                    },
                    status=status.HTTP_404_NOT_FOUND)
            product = product_queryset.first()
            serializer = GetProductSerializer(product)
            return Response(
                {
                    "message": "success",
                    "data": serializer.data,
                    "errors": "null"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)
