from pathlib import Path
import matplotlib.pyplot as plt
import databroker
from databroker import Broker
from bluesky.run_engine import RunEngine
import bluesky.plans as bp
from srw_handler import SRWFileHandler, read_srw_file
from bluesky.callbacks.best_effort import BestEffortCallback


PROFILE_STARTUP_PATH = Path(get_ipython().profile_dir.startup_dir)

plt.ion()

db = Broker.named('chx-simulation')
db.reg.register_handler('srw', SRWFileHandler, overwrite=True)

RE = RunEngine()
RE.subscribe(db.insert)

bec = BestEffortCallback()
RE.subscribe(bec)

