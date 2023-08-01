from django.db import models


class TimelineSlideHeader(models.Model):
    # location_line = models.BooleanField(default=True)
    media_caption = models.CharField(max_length=100, blank=True, default="")
    media_credit = models.CharField(max_length=200, blank=True, default="")
    media_url = models.URLField(blank=True, default="", max_length=300)
    text_headline = models.CharField(max_length=200, blank=True, null=True)
    text_text = models.TextField(blank=True, null=True)
    type = models.CharField(default="overview", max_length=20)
    wikipedia_name = models.CharField(max_length=1000, blank=True, default="")

    def __str__(self):
        return self.text_headline


class TimelineSlide(models.Model):
    slideheader = models.ManyToManyField(
        TimelineSlideHeader, through="TimelineSlidepack", related_name="slidepack_slide"
    )
    media_caption = models.CharField(max_length=100, blank=True, default="")
    media_credit = models.CharField(max_length=200, blank=True, default="")
    media_url = models.URLField(blank=True, max_length=400, default="")
    text_headline = models.CharField(max_length=200, blank=True, null=True)
    text_text = models.TextField(blank=True, null=True)
    wikipedia_name = models.CharField(max_length=1000, blank=True, default="")
    start_date = models.CharField(max_length=10, blank=True, default="")
    end_date = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        return self.text_headline


class TimelineSlidepack(models.Model):
    slideheader_fk = models.ForeignKey(TimelineSlideHeader, on_delete=models.CASCADE)
    slide_fk = models.ForeignKey(TimelineSlide, on_delete=models.CASCADE)
    slide_order = models.SmallIntegerField()

    def __str__(self):
        return (
            f"{self.slideheader_fk} TimelineSlide {self.slide_order} : {self.slide_fk}"
        )
