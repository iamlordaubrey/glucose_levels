import csv
from datetime import datetime

from django.core.management.base import BaseCommand

from glucose_levels.models import CustomUser, GlucoseLevel


class Command(BaseCommand):
    help = 'Loads data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=str)
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        file_path = kwargs['file_path']

        # Create user
        user, created = CustomUser.objects.get_or_create(id=user_id)
        print('creagted user : ', user, created)

        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            # Skip the first 2 rows
            for _ in range(2):
                next(csvfile)

            for row in reader:
                # Parse timestamp to valid format
                timestamp = row['Gerätezeitstempel'],
                parsed_timestamp = datetime.strptime(timestamp[0], '%d-%m-%Y %H:%M')
                # Format the datetime object to Django DateTimeField
                formatted_timestamp = parsed_timestamp.strftime('%Y-%m-%d %H:%M:%S')

                GlucoseLevel.objects.create(
                    user=user,
                    device=row['Gerät'],
                    serial_number=row['Seriennummer'],
                    timestamp=formatted_timestamp,
                    recording_type=row['Aufzeichnungstyp'],
                    glucose_value_history=row['Glukosewert-Verlauf mg/dL'] or None,
                    glucose_scan=row['Glukose-Scan mg/dL'] or None,
                    non_numeric_rapid_acting_insulin=row['Nicht numerisches schnellwirkendes Insulin'],
                    rapid_acting_insulin=row['Schnellwirkendes Insulin (Einheiten)'] or None,
                    non_numeric_nutritional_data=row['Nicht numerische Nahrungsdaten'],
                    carbohydrates_grams=row['Kohlenhydrate (Gramm)'] or None,
                    carbohydrates_portion=row['Kohlenhydrate (Portionen)'] or None,
                    non_numeric_depot_insulin=row['Nicht numerisches Depotinsulin'],
                    depot_insulin=row['Depotinsulin (Einheiten)'] or None,
                    notes=row['Notizen'],
                    glucose_test_strip=row['Glukose-Teststreifen mg/dL'] or None,
                    ketone=row['Keton mmol/L'] or None,
                    meal_insulin=row['Mahlzeiteninsulin (Einheiten)'] or None,
                    correction_insulin=row['Korrekturinsulin (Einheiten)'] or None,
                    insulin_change_by_user=row['Insulin-Änderung durch Anwender (Einheiten)'] or None,
                )
