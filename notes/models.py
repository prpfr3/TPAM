from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def custom_slugify(value):
    """
    Custom slugify function that replaces hyphens with underscores.
    """
    return slugify(value).replace("-", "_")


class Topic(models.Model):
    type = models.ForeignKey(
        "mainmenu.MyDjangoApp",
        default=1,
        verbose_name="Topic Type",
        on_delete=models.SET_DEFAULT,
    )
    text = models.CharField(max_length=25, verbose_name="Topic Name")
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.text


# This custom object manager allows a different queryset to be used than the standard "all" objects.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


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
        (TYPE_BOOK, "Book"),
        (TYPE_WEBSITE, "Website"),
        (TYPE_MAGAZINE, "Journal, Periodical or Magazine"),
        (TYPE_VIDEO, "Video"),
        (TYPE_MYSIGHTING, "MySighting"),
        (TYPE_MYPHOTO, "MyPhoto"),
    )

    # Define a custom ISBN validator
    isbn_validator = RegexValidator(
        regex=r"^[0-9]{13}$|^[0-9]{10}$",
        message="Invalid ISBN number. It should be either 10 or 13 digits long.",
        code="invalid_isbn",
    )

    issn_validator = RegexValidator(
        regex=r"^\d{4}-\d{3}[\dX]$",
        message="Invalid ISSN number. It should be in the format XXXX-XXX(X).",
        code="invalid_issn",
    )

    type = models.IntegerField(choices=REFERENCE_TYPE)
    """
    Model definitions are based on the Wikipedia citation model
    https://en.wikipedia.org/wiki/Template:Citation
    https://en.wikipedia.org/wiki/Wikipedia:Citation_templates
    https://en.wikipedia.org/wiki/Wikipedia:Template_index/Sources_of_articles/Citation_quick_reference
    """
    full_reference = models.CharField(
        max_length=300, blank="True", null="True", default=None
    )
    url = models.URLField(blank=True, null=True, max_length=300)
    year = models.IntegerField(default=None, blank=True, null=True)
    month = models.IntegerField(default=None, blank=True, null=True)
    day = models.IntegerField(default=None, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    authors = models.CharField(max_length=50, blank=True, default=None, null=True)
    editors = models.CharField(max_length=50, blank=True, default=None, null=True)
    title = models.CharField(max_length=200, blank=True, default=None, null=True)
    description = models.TextField(blank=True, null=True, default=None)
    journal = models.CharField(max_length=200, blank=True, default=None, null=True)
    edition = models.CharField(max_length=10, blank=True, default=None, null=True)
    chapter = models.CharField(max_length=10, blank=True, default=None, null=True)
    volume = models.CharField(max_length=10, blank=True, default=None, null=True)
    issue = models.CharField(max_length=20, blank=True, default=None, null=True)
    pages = models.CharField(max_length=10, blank=True, default=None, null=True)
    publisher = models.CharField(max_length=50, blank=True, default=None, null=True)
    isbn = models.CharField(
        max_length=20, blank=True, default=None, null=True, validators=[issn_validator]
    )
    issn = models.CharField(max_length=20, blank=True, default=None, null=True)
    doi = models.CharField(max_length=50, blank=True, default=None, null=True)
    access_date = models.DateField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.full_reference = ""
        if self.authors:
            self.full_reference += f"{self.authors}, "
        if self.day or self.month:
            self.full_reference += "("
        if self.day:
            self.full_reference += f"{str(self.day)}/"
        if self.month:
            self.full_reference += f"{str(self.month)}/"
        if self.year:
            self.full_reference += str(self.year)
        if self.day or self.month:
            self.full_reference += ") "
        elif self.year:
            self.full_reference += " "
        if self.title:
            self.full_reference += f"{self.title}, "
        if self.journal:
            self.full_reference += f"{self.journal}, "
        if self.issn:
            self.full_reference += f"ISSN:{self.issn}, "
        if self.edition:
            self.full_reference += f"{self.edition} edition, "
        if self.chapter:
            self.full_reference += f"Ch.{self.chapter}, "
        if self.volume:
            self.full_reference += f"Volume:{self.volume}, "
        if self.issue:
            self.full_reference += f"Issue:{self.issue}, "
        if self.pages:
            self.full_reference += f"pp.{self.pages}, "
        if self.publisher:
            self.full_reference += f"{self.publisher}, "
        if self.isbn:
            self.full_reference += f"ISBN:{self.isbn}, "
        if self.doi:
            self.full_reference += f"doi:{self.doi}, "
        if self.url:
            self.full_reference += f"{self.url}, "
        if self.access_date:
            self.full_reference += f"Accessed on {self.access_date}, "
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.isbn:
            # Remove any non-digit characters from the ISBN
            isbn_digits = "".join(filter(str.isdigit, self.isbn))

            # Perform the ISBN validation
            if len(isbn_digits) not in [10, 13]:
                raise ValidationError(
                    "Invalid ISBN number. It should be either 10 or 13 digits long."
                )

            # Calculate the checksum for ISBN-10 or ISBN-13
            if len(isbn_digits) == 10:
                checksum = (
                    sum(
                        (i + 1) * int(digit) for i, digit in enumerate(isbn_digits[:-1])
                    )
                    % 11
                )
                if checksum != int(isbn_digits[-1]) and (
                    checksum != 10 or isbn_digits[-1] != "X"
                ):
                    raise ValidationError("Invalid ISBN-10 number.")
            else:
                checksum = (
                    sum(
                        (3 if i % 2 == 0 else 1) * int(digit)
                        for i, digit in enumerate(isbn_digits[:-1])
                    )
                    % 10
                )
                if checksum != 0:
                    raise ValidationError("Invalid ISBN-13 number.")

        if self.issn:
            # Remove any non-digit characters from the ISSN
            issn_digits = "".join(filter(str.isdigit, self.issn))

            # Perform the ISSN validation
            if len(issn_digits) != 8:
                raise ValidationError(
                    "Invalid ISSN number. It should be in the format XXXX-XXX(X)."
                )

            # Calculate the checksum for ISSN
            checksum = (
                11
                - (
                    sum(
                        (8 - i) * int(digit) for i, digit in enumerate(issn_digits[:-1])
                    )
                    % 11
                )
            ) % 11
            checksum = "X" if checksum == 10 else str(checksum)
            if checksum != issn_digits[-1]:
                raise ValidationError("Invalid ISSN number.")

    def __str__(self):
        return f"{self.full_reference}"


class Post(models.Model):
    STATUS_CHOICES = (("draft", "Draft"), ("published", "Published"))

    title = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_owner")
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    url = models.URLField(default=None, null=True, blank=True)
    slug = models.SlugField(
        default=None,
        null=True,
        blank=True,
        max_length=255,
        unique=True,
        help_text="Enter the slug for the URL. Uses underscore (_) as a separator.",
    )
    body = models.TextField(default=None)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    references = models.ManyToManyField(Reference, blank=True)
    liked = models.ManyToManyField(User, blank=True)
    # Default manager exceptionally needs to be defined because we have defined a second manager, PublishedManager
    objects = models.Manager()
    # Our model custom manager which retrieves only published.
    published = PublishedManager()

    class Meta:
        verbose_name_plural = "Posts"
        ordering = ("-publish",)  # default sort will be descending on publish

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title).replace("-", "_")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("notes:post_detail", args=[self.slug])

    def __str__(self):
        return f"{self.title[:50]}..." if len(self.title) > 50 else self.title
