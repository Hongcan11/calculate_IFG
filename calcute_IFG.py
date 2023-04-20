# function for calculating the interferogram from SLC data
import h5py
import numpy as np
import matplotlib.pyplot as plt

def read_dset(hdf5_file_path, group_name):
    dset = {}
    with h5py.File(hdf5_file_path, "r") as f:
        for key in f[group_name].keys():
            dset[key] = f[group_name][key][:]
    return dset


def calculate_IFG(SLC_data):
    master_name = '20220327'
    cal_IFG_data = {}
    for dset_name, dset_data in SLC_data.items():
            cal_IFG_data[dset_name] = np.empty_like(dset_data)
            for i in range(dset_data.shape[0]):
                for j in range(dset_data.shape[1]):
                    cal_IFG_data[dset_name][i, j] = SLC_data[master_name][i, j] * np.conj(dset_data[i, j])
    print("IFG :", cal_IFG_data)
    return cal_IFG_data


def write_IFG(cal_IFG_data, hdf5_file_path, group_name):
    with h5py.File(hdf5_file_path, "a") as f:
        g = f.create_group(group_name)
        for dset_name, dset_data in cal_IFG_data.items():
            if dset_name not in f[group_name]:
                f.create_dataset(group_name + '/' + dset_name, data = dset_data)
            else:
                f[group_name + '/' + dset_name][:] = dset_data
        f.flush()
        f.close()

def data2jpg(dset):
    for dset_name, dset_data in dset.items():
        # print(dset_name)
        # print(dset_data)
        mag_data = np.abs(dset_data)
        phase_data = np.angle(dset_data)
        plt.title('Phase Map')
        plt.figure(dpi=400)
        plt.imshow(phase_data, cmap='jet')
        plt.colorbar()
        plt.savefig('/data/tests/hongcan/gecoris_test/HDF5_test/map/cal_DIF/cal_DIF_'+dset_name+'.jpg')
        plt.close()


if __name__ == "__main__":
    data2jpg(read_dset('/data/tests/hongcan/gecoris_test/HDF5_test/stack_s1_asc84.hdf5', 'cal_DIF'))