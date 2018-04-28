from srw_writer import SRWFileWriter

srw_writer = SRWFileWriter('srw_writer', 'data/res_int_pr_se.dat', root_dir='/XF11ID/simulation', reg=db.reg)
srw_writer.read_attrs = ['image', 'mean', 'photon_energy']
srw_writer.configuration_attrs = ['horizontal_extent', 'vertical_extent', 'shape']

