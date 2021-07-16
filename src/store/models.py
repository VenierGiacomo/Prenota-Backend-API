from django.db import models
from django.conf import settings

# Create your models here.

class Store(models.Model):
    store_name              = models.CharField(max_length=50)
    owner_name              = models.CharField(max_length=50, null=True, blank=True)
    owner                   = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL )
    address                 = models.CharField(max_length=50)
    business_description    = models.CharField(max_length=100, null=True, blank=True)
    keywords                = models.TextField(null=True, blank=True)
    business_type           = models.IntegerField(null=True, blank=True)
    order_priority          = models.IntegerField(null=True, blank=True)
    city                    = models.CharField(max_length=50)
    zip_code                = models.CharField(max_length=50)
    phone_number            = models.CharField(null=True, blank=True, max_length=20)
    max_spots               = models.IntegerField(default=-1)
    lat_long                = models.CharField(max_length=100, null=True, blank=True)
    img_url                 = models.CharField(max_length=500, null=True, blank=True)
    website                 = models.CharField(max_length=500, null=True, blank=True)
    stripe_connect          = models.CharField(max_length=50, null=True, blank=True)
    payable                 = models.BooleanField(default=False)
    must_pay                = models.BooleanField(default=False)
    closed                  = models.BooleanField(default=False)
    closed_message          = models.CharField(max_length=150, default='Siamo spiacenti, al momento siamo chiusi! Non appena riapriremo saremo  prenotabili online!')
    display                 = models.BooleanField(default=False)
    display_1               = models.BooleanField(default=False)
    only_app                = models.BooleanField(default=False)
    credits                 = models.BooleanField(default=False)
    adons                   = models.BooleanField(default=False)
    custom_size             = models.BooleanField(default=False)
    has_category            = models.BooleanField(default=False)
    table_line_heigth       = models.IntegerField(default=60)
    table_font_size         = models.IntegerField(default=12)
    quarter_displ           = models.BooleanField(default=True)
    five_displ              = models.BooleanField(default=False)
    update_price_scroll     = models.BooleanField(default=False)
    cancel_advance          = models.IntegerField(default=2)
    book_advance            = models.IntegerField(default=2)
    available_on            = models.CharField(max_length=1, choices=(("a", "Always available"),("f", "Full hours"),("q", "Quater hours")), default='q')

    class Meta:
        ordering = ('closed','business_type')
    # def __str__(self):
    #     return str(self.store_name+" ("+self.address+") ID:"+ str(self.id) )
    def __str__(self):
        return self.store_name