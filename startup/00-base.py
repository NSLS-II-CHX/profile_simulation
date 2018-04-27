import matplotlib.pyplot as plt
import databroker
from databroker import Broker
from srw_handler import SRWFileHandler

plt.ion()

db = Broker.named('chx-simulation')
db.reg.register_handler('srw', SRWFileHandler, overwrite=True)

