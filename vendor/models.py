from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from product.models import WasteCategory, Notification
from user.models import Vendor


class WasteCategoryPrice(models.Model):
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    price = models.IntegerField()

    class Meta:
        unique_together = ['category', 'vendor']

    def __str__(self):
        return "{} {} : {}".format(self.category.name, self.vendor.company_name, self.price)


class Order(models.Model):
    waste = models.OneToOneField('product.Waste', on_delete=models.CASCADE)
    client = models.ForeignKey('user.ClientUser', on_delete=models.CASCADE)
    vendor = models.ForeignKey('user.Vendor', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS = [
        ('onhold', 'On Hold'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(choices=STATUS, default='onhold', max_length=50)

    class Meta:
        ordering = ['created']

    def get_price(self):
        pp = WasteCategoryPrice.objects.get(category__waste=self.waste, vendor=self.vendor)
        return pp.price

    def __str__(self):
        return "{} {}".format(self.waste.name, self.vendor.company_name)


@receiver(post_save, sender=Order)
def create_notification_user(sender, instance, created, **kwargs):
    if created:
        nd = Notification(type='req', order_id=instance.id, vendor=instance.vendor, client=instance.client, waste=instance.waste)
        nd.save()
    else:
        if instance.status == 'sold':

            nd = Notification(type='sold', order_id=instance.id, vendor=instance.vendor, client=instance.client, waste=instance.waste)

            print(nd)
            nd.save()
        elif instance.status == 'canceled':
            nd = Notification(type='canceled', order_id=instance.id, vendor=instance.vendor, client=instance.client, waste=instance.waste)
            nd.save()
        else:
            pass
