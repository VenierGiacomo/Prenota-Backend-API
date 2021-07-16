from rest_framework import serializers

from bookings.models import Bookings

class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Bookings
        fields  =[
            'id',
            'shop',
            'client',
            'employee',
            'start',
            'start_t',
            'end_t',
            'end' ,
            'day'   ,
            'week',
            'month' ,
            'year'       ,
            'address',
            'location',
            'recurring_id',
            'client_name' ,
            'store_name',
            'store_phone',
            'phone',
            'note',
            'details' ,
            'service_n' ,
            'payed',
            'day_to_delete',
            'price',
            'booked_on_plt',
            'store_client',
        ]
        read_only_fields = [ 'payed','price']
        # read_only_fields = [ 'client']

class BookingsLightSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Bookings
        fields  =[
            'day'   ,
            'employee',
            'client',
            'start_t',
            'end_t' ,
            'service_n' ,
            'booked_on_plt',
            'payed',
            'price'
        ]
