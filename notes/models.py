from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class Topic(models.Model):
    type = models.ForeignKey('mainmenu.MyDjangoApp', default=1,
                             verbose_name="Topic Type", on_delete=models.SET_DEFAULT)
    text = models.CharField(max_length=25, verbose_name="Topic Name")
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.text

# This custom object manager allows a different queryset to be used than the standard "all" objects.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Reference(models.Model):

    # Choices are enumerated here using a technique recommended @
    # https://www.b-list.org/weblog/2007/nov/02/handle-choices-right-way/

    TYPE_BOOK = 1
    TYPE_WEBSITE = 2
    TYPE_MAGAZINE = 3
    TYPE_VIDEO = 4
    TYPE_MYSIGHTING = 5
    TYPE_MYPHOTO = 6

    REFERENCE_TYPE = (
        (TYPE_BOOK, 'Book'),
        (TYPE_WEBSITE, 'Website'),
        (TYPE_MAGAZINE, 'Magazine'),
        (TYPE_VIDEO, 'Video'),
        (TYPE_MYSIGHTING, 'MySighting'),
        (TYPE_MYPHOTO, 'MyPhoto'),
    )
    ref = models.IntegerField()
    type = models.IntegerField(choices=REFERENCE_TYPE)
    # Based on the Wikipedia citation model
    # https://en.wikipedia.org/wiki/Template:Citation
    # https://en.wikipedia.org/wiki/Wikipedia:Citation_templates
    # https://en.wikipedia.org/wiki/Wikipedia:Template_index/Sources_of_articles/Citation_quick_reference
    citation = models.TextField(blank='True', null='True',
                                default='cite book | last1 = | first1 = | title = [[ ]] | publisher = [[]] | pages = 1-2  | date = ??/??/?? | isbn = 0-786918-50-0 | journal = | volume = | issue = | issn = ')
    url = models.URLField(blank=True, null=True, max_length=300)
    notes = models.TextField(blank='True', null='True', default=None)
    date = models.CharField(max_length=10, blank=True, null=True)
    date_datetime = models.DateField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    date_added = models.DateTimeField(auto_now_add=True)
    # POTENTIAL FUTURE FIELDS
    # author = models.CharField(max_length=10, default=None, null=True)
    # author_last = models.CharField(max_length=10, default=None, null=True)
    # author_first = models.CharField(max_length=10, default=None, null=True)
    # author_link = models.CharField(max_length=10, default=None, null=True)
    # editor = models.CharField(max_length=10, default=None, null=True)
    # editor_last = models.CharField(max_length=10, default=None, null=True)
    # editor_first = models.CharField(max_length=10, default=None, null=True)
    # editor_link = models.CharField(max_length=10, default=None, null=True)
    # publication_date = models.CharField(max_length=20, default=None, null=True)
    # date = models.CharField(max_length=10, default=None, null=True)
    # year = models.CharField(max_length=10, default=None, null=True)
    # title = models.CharField(max_length=200, default=None, null=True)
    # chapter = models.CharField(max_length=10, default=None, null=True)
    # #Recommended values are book, journal, newspaper, magazine, periodical, web, conference, AV_media
    # type = models.CharField(max_length=10, default=None, null=True)
    # edition = models.CharField(max_length=10, default=None, null=True)
    # series = models.CharField(max_length=10, default=None, null=True)
    # volume = models.CharField(max_length=10, default=None, null=True)
    # issue = models.CharField(max_length=10, default=None, null=True)
    # publisher = models.CharField(max_length=10, default=None, null=True)
    # page = models.CharField(max_length=10, default=None, null=True)
    # pages = models.CharField(max_length=10, default=None, null=True)
    # no_pp = models.CharField(max_length=10, default=None, null=True)
    # isbn = models.CharField(max_length=20, default=None, null=True)
    # issn = models.CharField(max_length=20, default=None, null=True)
    # doi = models.CharField(max_length=50, default=None, null=True)
    # url = models.URLField(default=None, null=True)
    # access_date = models.CharField(max_length=10, default=None, null=True)

    def __str__(self):
        return f'{self.citation}'


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))

    title = models.CharField(max_length=250)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post_owner')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    url = models.URLField(default=None, null=True, blank=True)
    slug = models.SlugField(default=None, null=True, blank=True, max_length=255)
    body = models.TextField(default=None)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    references = models.ManyToManyField(Reference, blank=True)
    liked = models.ManyToManyField(User, blank=True)
    # Default manager exceptionally needs to be defined because we have defined a second manager, PublishedManager
    objects = models.Manager()
    # Our model custom manager which retrieves only published.
    published = PublishedManager()

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ('-publish',)  # default sort will be descending on publish

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title[:50]}..." if len(self.title) > 50 else self.title

    # Returns a canonical url which is the main url to be used for a specific post
    def get_absolute_url(self):
        return reverse('notes:post_update',
                       args=[self.id])
