import datetime
import shutil
import uuid
from pathlib import Path


def new_uid():
    return str(uuid.uuid4())


def insert_srw_data(input_file, root_dir='/XF11ID/simulation', reg=None, **md):
    assert reg, 'reg must be provided, e.g. db.reg'

    # Define the destination of the persistent storage:
    datum_id = new_uid()
    date = datetime.datetime.now()
    dst_file = Path(root_dir) / Path(date.strftime('%Y/%m/%d')) / \
               Path('{}.dat'.format(datum_id))

    # Copy the specified file to the persistent storage:
    shutil.copy2(input_file, dst_file)

    # Insert datum into the databroker
    resource_id = reg.insert_resource('srw', dst_file, {})
    reg.insert_datum(resource_id, datum_id, {})

