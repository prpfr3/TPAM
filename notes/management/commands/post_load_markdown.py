from csv import DictReader
from django.core.management import BaseCommand
from notes.models import Reference
import os
import markdown

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads a Post written in a markdown text file into Posts, converting to html"

    def handle(self, *args, **options):
        print("Adding Post")
        with open(
            os.path.join(DATAIO_DIR, "Post_markdown.txt"), encoding="utf-8-sig"
        ) as file:
            for row in DictReader(file):
                try:
                    r_fk, reference_created = Reference.objects.get_or_create(
                        journal=row["journal"],
                        issue=row["issue"],
                        title=row["title"],
                        type=row["type"],
                    )
                    print(r_fk)
                except Exception as e:
                    print(e)

                print(r_fk, reference_created)
                if row["authors"]:
                    r_fk.authors = row["authors"]
                if row["chapter"]:
                    r_fk.chapter = row["chapter"]
                if row["day"]:
                    r_fk.day = row["day"]
                if row["description"]:
                    r_fk.description = row["description"]
                if row["doi"]:
                    r_fk.doi = row["doi"]
                if row["edition"]:
                    r_fk.edition = row["edition"]
                if row["editors"]:
                    r_fk.editors = row["editors"]
                if row["isbn"]:
                    r_fk.isbn = row["isbn"]
                if row["issn"]:
                    r_fk.issn = row["issn"]
                if row["issue"]:
                    r_fk.issue = row["issue"]
                if row["journal"]:
                    r_fk.journal = row["journal"]
                if row["month"]:
                    r_fk.month = row["month"]
                if row["pages"]:
                    r_fk.pages = row["pages"]
                if row["publisher"]:
                    r_fk.publisher = row["publisher"]
                if row["title"]:
                    r_fk.title = row["title"]
                if row["year"]:
                    r_fk.year = row["year"]
                if row["volume"]:
                    r_fk.volume = row["volume"]

                try:
                    r_fk.save()
                    print(f"{r_fk} saved")
                except Exception as e:
                    print(f"{r_fk} not saved due to {e}")
