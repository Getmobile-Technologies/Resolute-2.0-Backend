from django.core.management.base import BaseCommand, CommandError
import json


class Command(BaseCommand):
    help = 'Create Dummy Box locations'


    def handle(self, *args, **options):
        
        with open('/Users/DELL/Desktop/Resolute/res_config/resolute.json', 'r') as f:
            info = json.load(f)
            credentials = json.dumps(info)
            
        with open('/Users/DELL/Desktop/Resolute/res_config/.env', 'a') as f:
            f.write(f'\nFIREBASE_CREDENTIALS={credentials}')
            
        self.stdout.write('firebase credentials updated')