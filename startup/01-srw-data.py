from srw_writer import SRWFileWriter

default_srw_file = str(PROFILE_STARTUP_PATH / Path('data/res_int_pr_se.dat'))
srw_writer = SRWFileWriter('srw_writer', default_srw_file, root_dir='/XF11ID/simulation', reg=db.reg)
srw_writer.read_attrs = ['image', 'mean', 'photon_energy']
srw_writer.configuration_attrs = ['horizontal_extent', 'vertical_extent', 'shape']

