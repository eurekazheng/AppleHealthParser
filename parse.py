import pandas as pd
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt


path = 'apple_health_export/导出.xml'
types = [['HeartRate'],
         ['BloodPressureSystolic', 'BloodPressureDiastolic']]

xtree = et.parse(path)
health_data = xtree.getroot()


def agg_subtypes(type):
    first = True
    for subtype in type:
        subtype_name = 'HKQuantityTypeIdentifier' + subtype
        records = health_data.findall('./Record[@type=\'%s\']' % subtype_name)
        values = [r.attrib.get('value') for r in records]
        values = pd.to_numeric(values)
        if first:
            dates = [r.attrib.get('startDate') for r in records]
            dates = pd.to_datetime(dates)
            yield 'dates', dates
            first = False
        yield subtype, values


for type in types:
    records = agg_subtypes(type)
    records = pd.DataFrame(records)
    records = records.set_index('dates')
    records = records.sort_index()
    records.plot()
    plt.show()
