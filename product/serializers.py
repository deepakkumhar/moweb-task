from rest_framework import serializers
from .models import *

class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id',)
    

class CategorySerializer(serializers.ModelSerializer):
    product=CategoryProductSerializer(many=True)    
    class Meta:
        model = Category
        fields = ('id', 'title', 'order' , 'product','subcategories')

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['subcategories'] = CategorySerializer(many=True)
        return fields

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=('subcategory', 'title', 'order')

    def __init__(self, *args, **kwargs):
        super(CategoryCreateSerializer, self).__init__(*args, **kwargs)
        self.fields['title'].error_messages['blank'] = u'title cannot be blank'
        self.fields['title'].error_messages['required'] = u'title is required'

    def validate(self, data):
        if data.get('subcategory'):
            if Category.objects.filter(id=data.get('subcategory').id,title=data['title']).exists() or Category.objects.filter(subcategory=data.get('subcategory'),title=data['title']):
                raise serializers.ValidationError("subcategory with this title name already exist")
        return data

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk','title')

class ProductSerializer(serializers.ModelSerializer):
    category=ProductCategorySerializer(many=True)  
    class Meta:
        model = Product
        fields = ('id', 'name', 'price' ,'category')
        

class ProductCategoryCreateSerializer(serializers.Serializer):
    id=serializers.IntegerField()

class ProductCreateSerializer(serializers.ModelSerializer):
    category=ProductCategoryCreateSerializer(many=True,)  

    class Meta:
        model = Product
        fields = ('id', 'name', 'price' ,'category')

    def __init__(self, *args, **kwargs):
        super(ProductCreateSerializer, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages['blank'] = u'name cannot be blank'
        self.fields['name'].error_messages['required'] = u'name is required'
        self.fields['price'].error_messages['blank'] = u'price cannot be blank'
        self.fields['price'].error_messages['required'] = u'price is required'
        self.fields['category'].error_messages['blank'] = u'category cannot be blank'
        self.fields['category'].error_messages['required'] = u'category is required'
    
    def validate(self, data):
        if not data.get('category'):
            raise serializers.ValidationError("please enter valid cateory id")
        if  Product.objects.filter(name=data['name']):
                raise serializers.ValidationError("product name must be uniqe")
        if  data['price']<=0:
                raise serializers.ValidationError("please enter a valid price")
        categories_data =data.get('category', [])
        for category in categories_data:
            if not Category.objects.filter(subcategory__isnull=False,id=category.get('id')).exists():
                msg="category id: "+str(category.get('id'))+" can not link with product"
                raise serializers.ValidationError(msg)

        return data

    def create(self, validated_data):
        categories_data =validated_data.pop('category')
        product=Product.objects.create(**validated_data)
        for categorys in categories_data:
            ct=Category.objects.get(id=categorys.get('id'))
            product.category.add(ct)
        product.save()
        return product


class ProductAttachSerializer(serializers.Serializer):
    message=serializers.CharField()