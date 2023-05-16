# function for calculating the interferogram from SLC data
import h5py
import time
import numpy as np
import matplotlib.pyplot as plt

def read_dset(hdf5_file_path, group_name):
    dset = {}
    with h5py.File(hdf5_file_path, "r") as f:
        for key in f[group_name].keys():
            dset[key] = f[group_name][key][:]
    return dset


# def calculate_IFG(SLC_data, master_name):
#     cal_IFG_data = {}
#     for dset_name, dset_data in SLC_data.items():
#             cal_IFG_data[dset_name] = np.empty_like(dset_data)
#             for i in range(dset_data.shape[0]):
#                 for j in range(dset_data.shape[1]):
#                     cal_IFG_data[dset_name][i, j] = SLC_data[master_name][i, j] * np.conj(dset_data[i, j])
#     print("IFG :", cal_IFG_data)
#     return cal_IFG_data

def calculate_IFG(SLC_data, master_name):
    cal_IFG_data = {}
    master_data = SLC_data[master_name]
    for dset_name, dset_data in SLC_data.items():
        cal_IFG_data[dset_name] = np.multiply(master_data, np.conj(dset_data))
    print("IFG :", cal_IFG_data)
    return cal_IFG_data


def write_IFG(cal_IFG_data, hdf5_file_path, group_name):
    with h5py.File(hdf5_file_path, "a") as f:
        if group_name not in f.keys():
            g = f.create_group(group_name)
        else:
            g = f[group_name]
        for dset_name, dset_data in cal_IFG_data.items():
            if dset_name not in g.keys():
                g.create_dataset(dset_name, data = dset_data)
            else:
                g[dset_name][:] = dset_data
        f.flush()
        f.close()

def data2jpg(dset, path):
    for dset_name, dset_data in dset.items():
                # Convert to complex float array if necessary
        dset_data = np.asarray(dset_data, dtype=np.complex64)

        # Compute phase map
        phase = np.angle(dset_data)
        print(phase[1567][21000:21050])
        plt.title('phase Map')
        plt.figure(dpi=200)
        plt.imshow(phase, cmap='jet')
        plt.colorbar()
        plt.savefig(path + '/' + dset_name + '_new_IFG.jpg')
        plt.close()


if __name__ == "__main__":
    HDF_dataset_path = '/data/tests/hongcan/GF3/cn_inner_mongolia_gf3c_dsc_fsii/gf3.hdf5'
    jpg_path = '/data/tests/hongcan/GF3/map/IFG'
    group_name = 'SLC'
    master_name = '20230119'
    start_time = time.clock()
    SLC_data = read_dset(HDF_dataset_path, group_name)
    read_end_time = time.clock()
    print("The time required to read data: ", read_end_time - start_time, "s")
    cal_IFG_data = calculate_IFG(SLC_data, master_name)
    cal_end_time = time.clock()
    print("The time required to calculate IFG: ", cal_end_time - read_end_time, "s")
    write_IFG(cal_IFG_data, HDF_dataset_path, 'cal_IFG')
    write_end_time = time.clock()
    print("The time required to write data: ", write_end_time - cal_end_time, "s")
    data2jpg(cal_IFG_data, jpg_path)
    jpg_end_time = time.clock()
    print("The time required to save jpg: ", jpg_end_time - write_end_time, "s")