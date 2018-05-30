from srw_writer import SRWFileWriter

default_srw_file = str(PROFILE_STARTUP_PATH / Path('data/res_int_pr_se.dat'))
srw_writer = SRWFileWriter('srw_writer', default_srw_file, root_dir='/XF11ID/simulation', reg=db.reg)
srw_writer.read_attrs = ['image', 'mean', 'total', 'photon_energy']
srw_writer.configuration_attrs = ['beam_center_x', 'beam_center_y',
                                  'wavelength', 'det_distance',
                                  'threshold_energy', 'photon_energy']

