from tracker.models import Completer
from django.core.management.base import BaseCommand, CommandError
from users.models import PermissionGroup

class Command(BaseCommand):
    help = 'Initialized those entries in the database which are necessary for the application to work! Should ideally be only used once'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.create_completers()
        self.create_groups()

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

    def create_milestones(self):
        pass
