import datetime
from shopclients.models import StoreClient
from django.conf import settings
from bookings.models import Bookings
dt = datetime.datetime.now()
appos = Bookings.objects.filter(day=dt.day, month=(dt.month-1), year=dt.year, client__gt=1).all()
for booking in appos:
    print(booking.client_name,booking.shop.store_name)