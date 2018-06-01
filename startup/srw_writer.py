import datetime
import shutil
from pathlib import Path

import numpy as np

from ophyd import Device, Signal, Component as Cpt
from ophyd.sim import SynAxis, NullStatus, new_uid

from srw_handler import read_srw_file
from chxtools import xfuncs


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
    file_name = Cpt(Signal)
    shape = Cpt(Signal)
    mean = Cpt(Signal)
    total = Cpt(Signal)
    horizontal_extent = Cpt(Signal)
    vertical_extent = Cpt(Signal)

    beam_center_x = Cpt(Signal)
    beam_center_y = Cpt(Signal)
    wavelength = Cpt(Signal)
    det_distance = Cpt(Signal)
    threshold_energy = Cpt(Signal)
    photon_energy = Cpt(Signal)

    def __init__(self, name, input_file, root_dir=None, reg=None, **kwargs):
        assert root_dir, 'root_dir must be specified'
        assert reg, 'reg must be provided, e.g. db.reg'
        # self.update_file(input_file)

        super().__init__(name=name, **kwargs)

        self.persistent_file = None
        self.reg = reg
        self._root_dir = root_dir
        self._resource_id = None
        self._result = {}
        self._input_file = None
        self._distance = None

        # Hints:
        self.mean.kind = 'hinted'
        self.total.kind = 'hinted'
        self.photon_energy.kind = 'hinted'
        self.file_name.kind = 'hinted'

    def update_file(self, input_file):
        assert Path(input_file).exists(), 'File <{}> is not found'.format(input_file)
        self._input_file = input_file

    def update_distance(self, distance):
        self._distance = distance

    def trigger(self):
        assert self._input_file, 'Please specify the input file before triggering.'
        super().trigger()
        datum_id = new_uid()
        date = datetime.datetime.now()
        self.persistent_file = Path(self._root_dir) / \
                               Path(date.strftime('%Y/%m/%d')) / \
                               Path('{}.dat'.format(datum_id))

        # Copy the specified file to the persistent storage:
        shutil.copy2(self._input_file, self.persistent_file)

        ret = read_srw_file(self.persistent_file)

        self.image.put(datum_id)
        self.file_name.put(str(self.persistent_file))
        self.shape.put(ret['shape'])
        self.mean.put(ret['mean'])
        self.total.put(ret['total'])
        self.horizontal_extent.put(ret['horizontal_extent'])
        self.vertical_extent.put(ret['vertical_extent'])

        # Configure parameters used in Eiger:
        self.threshold_energy.put(0)  # a placeholder for now
        self.photon_energy.put(ret['photon_energy'])  # [eV]
        max_pos = np.where(ret['data'] == ret['data'].max())
        self.beam_center_x.put(max_pos[1][0])  # [pixels]
        self.beam_center_y.put(max_pos[0][0])  # [pixels]

        try:
            wavelength = xfuncs.get_Lambda(ret['photon_energy'] / 1e3, 'A')  # [Angstroms]
        except:
            wavelength = 0

        self.wavelength.put(wavelength)
        self.det_distance.put(self._distance)  # [m]

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

