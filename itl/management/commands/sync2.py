import xml.etree.ElementTree as ET
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        xml_data = open(settings.LIBRARY_PATH).read()
        root = ET.XML(xml_data)  # element tree
        keys = root[0].findall('key')
        for key in keys:
            if key.text == 'Tracks':
                tracks_key = key
                print("got", tracks_key)


        # import pdb; pdb.set_trace()
        all_records = []
        for i, child in enumerate(tracks_key):
            record = {}
            for subchild in child:
                record[subchild.tag] = subchild.text
                all_records.append(record)
        df = pd.DataFrame(all_records)
        import pdb; pdb.set_trace()
        return df


# keys = root[0].findall('key')
