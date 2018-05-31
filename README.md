# Simulation profile for SRW data analysis

Start `bsui` as follows:
```
$ BS_PROFILE=simulation BS_ENV=collection-2018-2.1 bsui
```

How to use:
----

### Prepare the detector and trigger it:

- Specify the input SRW file:
  `srw_writer.update_file('/home/xf11id/res_int_pr_me_s2_0_03mm_smp50nm_det.dat')`
- Specify the detector distance:
  `srw_writer.update_distance(16.046)`
- Count the simulated detector:
  `RE(bp.count([srw_writer]), Simulation='random posts (SRW)')`

### Get data back as a NumPy array:
```python
hdr = db[-1]
imgs, = list(hdr.data('srw_writer_image'))
plt.imshow(np.log10(imgs), origin='bottom')
```

### Check the configuration attributes:
```python
In [26]: hdr.config_data('srw_writer')
Out[26]: 
{'primary': [{'srw_writer_beam_center_x': 1035,
   'srw_writer_beam_center_y': 1081,
   'srw_writer_wavelength': 1.2848102140613589,
   'srw_writer_det_distance': 16.046,
   'srw_writer_threshold_energy': 0,
   'srw_writer_photon_energy': 9650.0}]}
```
