import csv
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from locations.models import LocationHistoricEvent, EventType


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    # Try ISO first
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    # Fallback: try to parse YYYYMMDD
    if len(s) == 8 and s.isdigit():
        try:
            return datetime.strptime(s, "%Y%m%d").date()
        except Exception:
            pass
    raise ValueError(f"Unrecognised date format: {s}")


class Command(BaseCommand):
    help = "Import LocationHistoricEvent rows from CSV. CSV should have a header matching model fields. The 'object_id' column should contain the slug of the target object (location or route)."

    def add_arguments(self, parser):
        parser.add_argument('csvfile', help='Path to the CSV file')
        parser.add_argument('--dry-run', action='store_true', help='Parse and validate but do not write to DB')
        parser.add_argument('--commit', action='store_true', help='Commit changes (default is dry-run unless --commit provided)')
        parser.add_argument('--encoding', default='utf-8', help='File encoding')

    def handle(self, *args, **options):
        path = options['csvfile']
        dry = options['dry_run'] and not options['commit']
        commit = options['commit']

        created = 0
        skipped = 0
        errors = []

        try:
            f = open(path, encoding=options.get('encoding') or 'utf-8')
        except Exception as e:
            raise CommandError(f"Could not open file: {e}")

        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            self.stdout.write(self.style.WARNING('No rows found in CSV'))
            return

        if commit:
            tx = transaction.atomic()
            tx.__enter__()

        try:
            for i, row in enumerate(rows, start=1):
                try:
                    # Required fields
                    et_val = row.get('event_type')
                    if not et_val:
                        raise ValueError('event_type is required')

                    # Resolve EventType: accept pk or code
                    event_type = None
                    if et_val.isdigit():
                        event_type = EventType.objects.filter(pk=int(et_val)).first()
                    if not event_type:
                        event_type = EventType.objects.filter(code__iexact=et_val).first()
                    if not event_type:
                        raise ValueError(f'Unknown event_type: {et_val}')

                    ct_val = row.get('content_type')
                    if not ct_val:
                        raise ValueError('content_type is required')
                    ct_val = ct_val.strip()

                    # Support either numeric ContentType id or app_label.model or plain model name (assume app_label 'locations')
                    ct = None
                    model = None
                    if ct_val.isdigit():
                        ct = ContentType.objects.filter(pk=int(ct_val)).first()
                    else:
                        if '.' in ct_val:
                            app_label, model_name = ct_val.split('.', 1)
                            ct = ContentType.objects.filter(app_label=app_label, model=model_name.lower()).first()
                        else:
                            ct = ContentType.objects.filter(app_label='locations', model=ct_val.lower()).first()

                    if ct:
                        model = ct.model_class()
                    if not model:
                        raise ValueError(f'Unknown content_type: {ct_val}')

                    # Slug is provided in object_id column per spec
                    slug = row.get('object_id')
                    if not slug:
                        raise ValueError('object_id (slug) is required')

                    # Lookup object by slug
                    target = model.objects.filter(slug=slug).first()
                    if not target:
                        # Try alternative fields commonly used
                        alt_fields = ['wikiname', 'name']
                        for af in alt_fields:
                            if hasattr(model, af):
                                target = model.objects.filter(**{af: slug}).first()
                                if target:
                                    break
                    if not target:
                        raise ValueError(f'No {model.__name__} found with slug/name/wikiname="{slug}"')

                    # Parse datefield
                    date_s = row.get('datefield')
                    if not date_s:
                        raise ValueError('datefield is required')
                    datefield = parse_date(date_s)

                    description = row.get('description') or ''
                    displaydate = row.get('displaydate') or ''

                    inst = LocationHistoricEvent(
                        event_type=event_type,
                        description=description,
                        displaydate=displaydate,
                        datefield=datefield,
                        content_type=ct,
                        object_id=target.pk,
                    )

                    if dry:
                        self.stdout.write(f'Row {i}: would create event for {ct.app_label}.{ct.model} id={target.pk}')
                        created += 1
                    else:
                        inst.full_clean()
                        inst.save()
                        created += 1
                except Exception as e:
                    skipped += 1
                    errors.append((i, str(e)))
                    self.stdout.write(self.style.ERROR(f'Row {i} skipped: {e}'))

        finally:
            f.close()
            if commit:
                if errors:
                    # rollback
                    tx.__exit__(Exception, Exception('errors occurred'), None)
                    self.stdout.write(self.style.ERROR('Errors occurred; transaction rolled back'))
                else:
                    tx.__exit__(None, None, None)

        self.stdout.write(self.style.SUCCESS(f'Imported {created} events; skipped {skipped} rows'))
        if errors:
            self.stdout.write('Errors detail:')
            for r, msg in errors:
                self.stdout.write(f'  Row {r}: {msg}')
