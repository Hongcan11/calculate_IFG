import h5py
import numpy as np
from calcute_IFG import read_SLC_data, write_IFG

def calculate_DIF():
    origin_IFG_data = read_SLC_data('/data/tests/hongcan/gecoris_test/project_test/HDF5_test/stack_s1_asc84.hdf5', 'IFG')
    cal_IFG_data = read_SLC_data('/data/tests/hongcan/gecoris_test/project_test/HDF5_test/stack_s1_asc84.hdf5', 'cal_IFG')
    cal_DIF_data = {}
    for dset_name, dset_data in cal_IFG_data.items():
        for dset_name1, dset_data1 in origin_IFG_data.items():
            if dset_name == dset_name1:
                cal_DIF_data[dset_name] = np.empty_like(dset_data)
                for i in range(dset_data.shape[0]):
                    for j in range(dset_data.shape[1]):
                        cal_DIF_data[dset_name][i, j] = dset_data[i, j] - dset_data1[i, j]
    print("DIF :", cal_DIF_data)

    # write_IFG(cal_DIF_data, '/data/tests/hongcan/gecoris_test/project_test/HDF5_test/stack_s1_asc84.hdf5', 'cal_DIF')
    # return cal_DIF_data

if __name__ == "__main__":
    calculate_DIF()