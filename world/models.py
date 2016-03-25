from django.contrib.gis.db import models

class Member(models.Model):
        name = models.CharField(max_length=500)
        image = models.CharField(max_length=500)
        point = models.PointField()
        objects = models.GeoManager()

    # Returns the string representation of the model.
        def __str__(self):              # __unicode__ on Python
            return self.name
