from tracker.models import Completer, Milestone
from django.core.management.base import BaseCommand, CommandError
from users.models import PermissionGroup, Department
from datetime import timedelta

class Command(BaseCommand):
    help = 'Initialized those entries in the database which are necessary for the application to work! Should ideally be only used once'

    def add_arguments(self, parser):
        parser.add_argument(
            '--only_completers',
            action='store_true',
        )
        parser.add_argument(
            '--only_groups',
            action='store_true',
        )
        parser.add_argument(
            '--only_milestones',
            action='store_true',
        )
        parser.add_argument(
            '--only_departments',
            action='store_true',
        )

    def handle(self, *args, **options):
        if options['only_completers']:
            self.create_completers()
        elif options['only_groups']:
            self.create_groups()
        elif options['only_milestones']:
            self.create_milestones()
        elif options['only_departments']:
            self.create_departments()
        else:        
            self.create_completers()
            self.create_groups()
            self.create_milestones()

    def create_completers(self):
        completers = [
            Completer(
                name = 'ClickCompleter',
                handler = 'tracker.contrib.completers.ClickCompleter'
            ),
            Completer(
                name = 'UploadCompleter',
                handler = 'tracker.contrib.completers.UploadCompleter'
            )
        ]

        for completer in completers: completer.save()

    def create_groups(self):
        groups = [
            PermissionGroup(name="Admin", codename="ADMIN"),
            PermissionGroup(name="Benutzer", codename="USER"),
            PermissionGroup(name="ReadOnly", codename="READONLY")
        ]
        for group in groups: group.save()

    def create_departments(self):
        departments = [
            Department(name="Vertrieb"),
            Department(name="Kampagne"),
            Department(name="Grafiker")
        ]
        for department in departments: department.save()

    def create_milestones(self):
        milestones = [
            Milestone(
                name="Vertrag schicken",
                duration=timedelta(days=1),
                department=vertrieb(),
                completer=upload_completer(),
                upload_dir="contracts",
                upload_name="Vertrag"
            ),
            Milestone(
                name="Vertrag unterschrieben",
                duration=timedelta(days=1),
                is_external=True,
                department=vertrieb(),
                completer=upload_completer(),
                upload_dir="returned_contracts",
                upload_name="Unterschriebener Vertrag"
            ),
            Milestone(
                name="Rechnung schicken",
                duration=timedelta(days=1),
                department=vertrieb(),
                completer=upload_completer(),
                upload_dir="invoices",
                upload_name="Rechnung",
            ),
            Milestone(
                name="Banner erstellen",
                duration=timedelta(days=2),
                department=grafiker(),
                completer=upload_completer(),
                upload_dir="banners",
                upload_name="Banner",
            ),
            Milestone(
                name="Trackingcode schicken",
                duration=timedelta(days=1),
                department=kampagne(),
                completer=click_completer()
            ),
            Milestone(
                name="Banner schicken",
                duration=timedelta(days=1),
                department=kampagne(),
                completer=click_completer()
            ),
            Milestone(
                name="Trackingcode bestätigt",
                duration=timedelta(days=1),
                is_external=True,
                department=kampagne(),
                completer=click_completer(),
            ),
            Milestone(
                name="Banner bestätigt",
                duration=timedelta(days=1),
                is_external=True,
                department=kampagne(),
                completer=click_completer()
            ),
            Milestone(
                name="Trackingcode-Kontrolle",
                duration=timedelta(days=1),
                department=kampagne(),
                completer=click_completer()
            ),
            Milestone(
                name="Bezahlt",
                duration=timedelta(days=1),
                is_external=True,
                department=vertrieb(),
                completer=click_completer()
            ),
            Milestone(
                name="Kampagne Starten",
                duration=timedelta(days=1),
                department=vertrieb(),
                completer=click_completer()
            ),
        ]
        for milestone in milestones: milestone.save()

def upload_completer():
    return Completer.objects.get(name="UploadCompleter")

def click_completer():
    return Completer.objects.get(name="ClickCompleter")

def vertrieb():
    return Department.objects.get(name="Vertrieb")

def kampagne():
    return Department.objects.get(name="Kampagne")

def grafiker():
    return Department.objects.get(name="Grafiker")