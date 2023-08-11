from django.core.management.base import BaseCommand, CommandError

from .library.test_lib import out_hoge

class Command(BaseCommand):
    help = 'test module'
    
    def handle(self, *args, **options):
        out_hoge()
