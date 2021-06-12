from django.contrib.gis.db import models


class WasteCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="catg_img", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STAT = [
        ('dr', 'Draft'),
        ('pd', 'Published'),
    ]

    status = models.CharField(
        max_length=3,
        choices=STAT, default="dr"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "waste_category"
        ordering = ('-name',)


class Waste(models.Model):
    Waste_Status = [
        ('not-working', 'Not Working'),
        ('working', 'Working'),
        ('good', 'Good'),
    ]
    Status = [
        ('sold', 'Sold'),
        ('in-bucket', 'In Bucket'),
        ('canceled', 'Canceled'),
    ]
    name = models.CharField(max_length=230)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='waste_image', null=True, blank=True)
    image2 = models.ImageField(upload_to='waste_image', null=True, blank=True)
    image3 = models.ImageField(upload_to='waste_image', null=True, blank=True)
    waste_status = models.CharField(choices=Waste_Status, default='working', max_length=50)
    # status = models.CharField(choices=Status, default='working', max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    location_lat = models.FloatField()
    location_long = models.FloatField()
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Notification(models.Model):
    NT_TYPE = [
        ('sold', 'Item Sold'),
        ('canceled', 'Item Canceled'),
        ('req', 'Requested'),]
    type = models.CharField(max_length=10, choices=NT_TYPE)
    seen = models.BooleanField(default=False)
    order = models.ForeignKey('vendor.Order', on_delete=models.CASCADE, blank=True, null=True)
    waste = models.ForeignKey('product.Waste', on_delete=models.CASCADE)
    client = models.ForeignKey('user.ClientUser', on_delete=models.CASCADE)
    vendor = models.ForeignKey('user.Vendor', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notification"
        ordering = ('-created',)

    def __str__(self):
        return "{}-{}".format(self.type, self.waste.name)