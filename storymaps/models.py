from django.db import models


class SlideHeader(models.Model):
    location_line = models.BooleanField(default=True)
    media_caption = models.CharField(max_length=100, blank=True, null=True)
    media_credit = models.CharField(max_length=200, blank=True, null=True)
    media_url = models.URLField(blank=True, null=True, max_length=300)
    text_headline = models.CharField(max_length=200, blank=True, null=True)
    text_text = models.TextField(blank=True, null=True)
    type = models.CharField(default='overview', max_length=20)
    wikipedia_name = models.CharField(max_length=1000, blank=True, default='')

    def __str__(self):
        return self.text_headline


class Slide(models.Model):
    slideheader = models.ManyToManyField(
        SlideHeader, through='Slidepack', related_name='slidepack_slide')
    background = models.URLField(blank=True, null=True, max_length=300)
    northing = models.FloatField(blank=True, null=True)
    easting = models.FloatField(blank=True, null=True)
    zoom = models.SmallIntegerField(default=12)
    media_caption = models.CharField(max_length=100, blank=True, null=True)
    media_credit = models.CharField(max_length=200, blank=True, null=True)
    media_url = models.URLField(blank=True, null=True, max_length=400)
    text_headline = models.CharField(max_length=200, blank=True, null=True)
    text_text = models.TextField(blank=True, null=True)
    wikipedia_name = models.CharField(max_length=1000, blank=True, default='')

    def __str__(self):
        return self.text_headline


class Slidepack(models.Model):
    slideheader_fk = models.ForeignKey(SlideHeader, on_delete=models.CASCADE)
    slide_fk = models.ForeignKey(Slide, on_delete=models.CASCADE)
    slide_order = models.SmallIntegerField()

    def __str__(self):
        return f"{self.slideheader_fk} Slide {self.slide_order} : {self.slide_fk}"
