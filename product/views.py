from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from drf_spectacular.utils import extend_schema


from .serializers import *
from .models import *
from .utils import *

# Create your views here.
class CategoriesCreate(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CategoryCreateSerializer
    queryset = Category.objects.all()
    @extend_schema(
    tags=['Category'],
    summary='create category api'
    )
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response = []
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
            response.append(serializer.data)
        else:
            error_msg_value = list(serializer.errors.values())[0]
            return error_400(request,message=(error_msg_value[0]))

        return Response(response[0], status=201)

class CategoriesListing(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

    @extend_schema(
    tags=['Category'],
    summary='category-listing api'
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def get_queryset(self):
        return Category.objects.filter(subcategory__isnull=True)

class CategoriesRetrieve(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

    @extend_schema(
    tags=['Category'],
    summary='retrieve category api'
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def get_queryset(self):
        return Category.objects.filter(subcategory__isnull=True)

class CategoriesDeletes(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    @extend_schema(
    tags=['Category'],
    summary='delete category api'
    )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message":"Category deleted successfully"
        },
        status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()

#############################

class ProductListing(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset=Product.objects.all()

    @extend_schema(
    tags=['Producd'],
    summary='product-listing api'
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ProductRetrieve(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset= Product.objects.all()

    @extend_schema(
    tags=['Producd'],
    summary='retrieve product api'
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ProductDelete(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    @extend_schema(
    tags=['Producd'],
    summary='delete product api'
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message":"Product deleted successfully"
        },
        status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


class ProductCreate(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()

    @extend_schema(
    tags=['Producd'],
    summary='create product api'
    )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response = []
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
            response.append(serializer.data)
        else:
            error_msg_value = list(serializer.errors.values())[0]
            return error_400(request,message=(error_msg_value[0]))
        
        return Response(response[0], status=201)
    
class ProductAttach(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    @extend_schema(
    tags=['Producd'],
    summary='attach product to category'
    )

    def post(self, request,product_id,category_id):
        if not Product.objects.filter(id=product_id).exists():
            return error_400(request,message="product id not exist")
        if not Category.objects.filter(subcategory__isnull=False,id=category_id).exists():
            return error_400(request,message="category id not exist")
        product=Product.objects.get(id=product_id)
        product.category.add(Category.objects.get(id=category_id))
        return Response({"message": "product linked succesfully"})
