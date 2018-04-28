import datetime
import shutil
from pathlib import Path

from ophyd import Device, Signal, Component as Cpt
from ophyd.sim import SynAxis, NullStatus, new_uid

from srw_handler import read_srw_file


class SRWFileWriter(Device):
    """
    Save SRW simulation result into databroker.

    Parameters
    ----------
    name : str
        The name of the detector

    TODO: complete doc-string.
    """
    image = Cpt(Signal)
    shape = Cpt(Signal)
    mean = Cpt(Signal)
    photon_energy = Cpt(Signal)
    horizontal_extent = Cpt(Signal)
    vertical_extent = Cpt(Signal)

    def __init__(self, name, input_file, root_dir=None, reg=None, **kwargs):
        assert root_dir, 'root_dir must be specified'
        assert reg, 'reg must be provided, e.g. db.reg'
        self.update_file(input_file)

        super().__init__(name=name, **kwargs)

        self.persistent_file = None
        self.reg = reg
        self._root_dir = root_dir
        self._resource_id = None
        self._result = {}
        self._hints = None

    def update_file(self, input_file):
        assert Path(input_file).exists(), 'File <{}> is not found'.format(input_file)
        self.input_file = input_file

    @property
    def hints(self):
        if self._hints is None:
            return {'fields': [self.mean.name]}
        return self._hints

    @hints.setter
    def hints(self, val):
        self._hints = dict(val)

    def trigger(self):
        super().trigger()
        datum_id = new_uid()
        date = datetime.datetime.now()
        self.persistent_file = Path(self._root_dir) / \
                               Path(date.strftime('%Y/%m/%d')) / \
                               Path('{}.dat'.format(datum_id))

        # Copy the specified file to the persistent storage:
        shutil.copy2(self.input_file, self.persistent_file)

        ret = read_srw_file(self.persistent_file)

        self.image.put(datum_id)
        self.shape.put(ret['shape'])
        self.mean.put(ret['mean'])
        self.photon_energy.put(ret['photon_energy'])
        self.horizontal_extent.put(ret['horizontal_extent'])
        self.vertical_extent.put(ret['vertical_extent'])

        self._resource_id = self.reg.insert_resource('srw', self.persistent_file, {})
        self.reg.insert_datum(self._resource_id, datum_id, {})

        return NullStatus()

    def describe(self):
        res = super().describe()
        res[self.image.name].update(dict(external="FILESTORE"))
        return res

    def unstage(self):
        super().unstage()
        self._resource_id = None
        self._result.clear()

