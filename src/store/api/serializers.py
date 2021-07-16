from rest_framework import serializers

from store.models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Store
        fields  =[
            'id',
            'store_name',
            'business_type',
            'keywords',
            'owner',
            'address',
            'city',
            'zip_code',
            'img_url',
            'website',
            'phone_number',
            'max_spots',
            'business_type',
            'business_description',
            'stripe_connect',
            'payable',
            'must_pay',
            'closed',
            'only_app',
            'closed_message',
            'credits',
            'adons',
            'custom_size',
            'has_category',
            'table_line_heigth',
            'table_font_size',
            'quarter_displ' ,
            'five_displ',
            'book_advance',
            'cancel_advance',
            'available_on',

        ]
        extra_kwargs={'payment_method': {'write_only': True}}
        read_only_fields = ['img_url', 'business_type','business_description', 'stripe_connect','payable','closed','closed_message']

class UpdateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Store
        fields  =[
            # 'id',
            # 'store_name',
            'business_type',
            # 'owner',
            # 'address',
            # 'city',
            # 'zip_code',
            # 'img_url',
            # 'max_spots',
            # 'business_type',
            # 'business_description',
        ]
        # extra_kwargs={'payment_method': {'write_only': True}}
        # read_only_fields = ['img_url', 'business_type','business_description',]



