from pathlib import Path
import matplotlib.pyplot as plt
import databroker
from databroker import Broker
from srw_handler import SRWFileHandler, read_srw_file

PROFILE_STARTUP_PATH = Path(get_ipython().profile_dir.startup_dir)

plt.ion()

db = Broker.named('chx-simulation')
db.reg.register_handler('srw', SRWFileHandler, overwrite=True)

