# """
# processed_data utility functions
# """
# # todo: this script is written badly, and ideally should be a dataloader as saving all the data to memory is not sustainable.
#
# import ast
# import os
# import random

import os

import numpy as np
import pandas as pd

from .objects import Tensor


class DataLoader:
    def load(self):
        ...

    def reset(self):
        ...

    def __iter__(self):
        ...

    def __next__(self):
        ...

    def __getitem__(self, item):
        ...


class DataLoaderCSV(DataLoader):
    def __init__(self, root, values_file, labels_file, number_files=1, shuffle_order=False, **kwargs):
        self._root = root
        self.values_file = os.path.join(root, values_file)
        self.labels_file = os.path.join(root, labels_file)
        self._values = None
        self._labels = None
        self._shuffle_order = shuffle_order
        self._idx = 0
        self.number_files = number_files

        self._order = np.arange(0, self.number_files)

    def load(self, file_num=0):
        if file_num == 0:
            file_num = ""
        self._values = Tensor(np.array(pd.read_csv(str(self.values_file).replace(".csv", "") + str(file_num) + ".csv")))
        self._labels = Tensor(np.array(pd.read_csv(str(self.labels_file).replace(".csv", "") + str(file_num) + ".csv")))

    def reset(self):
        if self._shuffle_order:
            self.shuffle()
        self._idx = 0

    def shuffle(self):
        np.random.shuffle(self._order)

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        self._idx += 1
        if self._idx >= len(self._indexes):
            raise StopIteration
        self.load(self._order[self._idx])

        return self._labels, self._values

    def __getitem__(self, idx):
        if idx >= len(self._indexes):
            raise IndexError("Index out of range")

        self.load(idx)

        return self._values, self._labels


class DataLoaderCSVOld:
    def __init__(self, root, values_folder, labels_folder, batch_size=5, save_to_memory=False, shuffle=False):
        self._root = root
        self._labels_dir = os.path.join(root, labels_folder)
        self._values_dir = os.path.join(root, values_folder)
        self._memory = save_to_memory
        self._values = None
        self._labels = None
        self._get_memory()
        self._indexes = np.array(pd.read_csv(self._labels_dir).index)
        self._idx = 0
        self._batch_size = batch_size
        self._shuffle = shuffle
        self.reset()

    def _get_memory(self):
        if self._memory:
            self._values = np.array(pd.read_csv(self._values_dir))
            self._labels = np.array(pd.read_csv(self._labels_dir))

    def reset(self):
        if self._shuffle:
            np.random.shuffle(self._indexes)
        self._idx = 0

    def __len__(self):
        return len(self._indexes)

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        if self._idx >= len(self._indexes):
            raise StopIteration

        start_idx = self._idx
        end_idx = min(self._idx + self._batch_size, len(self._indexes))
        self._idx = end_idx

        batch_indexes = self._indexes[start_idx:end_idx]
        if self._memory:
            values = self._values[batch_indexes]
            labels = self._values[batch_indexes]
        else:
            values = pd.read_csv(self._values_dir, skiprows=lambda x: x not in batch_indexes + 1).values
            labels = pd.read_csv(self._labels_dir, skiprows=lambda x: x not in batch_indexes + 1).values

        return values, labels

    def __getitem__(self, idx):
        if idx >= len(self._indexes):
            raise IndexError("Index out of range")

        start_idx = idx * self._batch_size
        end_idx = min(start_idx + self._batch_size, len(self._indexes))

        batch_indexes = self._indexes[start_idx:end_idx]
        values = pd.read_csv(self._values_dir, skiprows=lambda x: x not in batch_indexes + 1).values
        labels = pd.read_csv(self._labels_dir, skiprows=lambda x: x not in batch_indexes + 1).values

        return values, labels

#
# import numpy as np
# import pandas as pd
#
# from .helper_functions import (
#     print_color
# )
#
# from colorama import Fore, Style
# from tqdm import tqdm
#
# tqdm_color = f'{Fore.GREEN}{{l_bar}}{{bar}}{{r_bar}}{Style.RESET_ALL}'
#
#
# def trim(data, trim_frac=0.5):
#     """ trim data based on a fraction """
#     data = data[0:trim_frac * len(data)]
#     return data
#
#
# def test_val(values, labels, val_frac=0.3):
#     """ randomly split data into training and validation sets """
#     # zip & shuffle data
#     data = list(zip(values, labels))
#     random.shuffle(data)
#     # split data
#     train = data[round(len(data) * val_frac):]
#     val = data[0:round(len(data) * val_frac)]
#     # unzip data
#     train_values, train_labels = zip(*train)
#     val_values, val_labels = zip(*val)
#     # reformat data
#     train_values, train_labels = list(train_values), list(train_labels)
#     val_values, val_labels = list(val_values), list(val_labels)
#     # return data
#     return train_values, train_labels, val_values, val_labels
#
#
# def shuffle(values, labels):
#     """ shuffle values and labels """
#     # zip & shuffle data
#     data = list(zip(values, labels))
#     random.shuffle(data)
#     # unzip data
#     values, labels = zip(*data)
#     # return data
#     return values, labels
#
#
# def format_parameters(file_path, status_bars=True):
#     """ format parameters from a .txt file """
#     # find errors
#     if not file_path.endswith('.txt'):
#         raise ValueError(f'{file_path} is not a .txt file')
#     # load parameters
#     parameters = []
#     if status_bars:
#         print_color('formatting parameters...')
#     with open(file_path, 'r') as f:
#         for line in f:
#             # reformat parameters
#             parameters.append(np.array(ast.literal_eval(line)))
#     # return parameters
#     return parameters
#
#
# def format_parameters_new(root, m_type='scratch', status_bars=True):
#     """ format parameters from file paths """
#     # check for valid model types
#     val_m_types = ['scratch', 'torch']
#     if m_type not in val_m_types:
#         raise TypeError(f'{m_type} is not a valid model type {val_m_types}')
#     if m_type == 'scratch':
#         # set valid and required file types
#         val_files = ['weights.txt', 'biases.txt', 'kernels.txt']
#         req_files = val_files[0:2]
#         files = []
#         # get list of files
#         for file in os.listdir(root):
#             files.append(file)
#         # check if dir includes required files
#         if not set(files).issubset(req_files):
#             raise TypeError(f'{files} does not include all required files {req_files}')
#         # load parameters
#         if status_bars:
#             print_color('formatting parameters...')
#         weights = []
#         biases = []
#         kernels = []
#         with open(os.path.join(root, 'weights.txt'), 'r') as f:
#             for line in f:
#                 # reformat weights
#                 weights.append(np.array(ast.literal_eval(line)))
#         with open(os.path.join(root, 'biases.txt'), 'r') as f:
#             for line in f:
#                 # reformat biases
#                 biases.append(np.array(ast.literal_eval(line)))
#         if os.path.exists(os.path.join(root, 'kernels.txt')):
#             with open(os.path.join(root, 'kernels.txt'), 'r') as f:
#                 for line in f:
#                     # reformat kernels
#                     kernels.append(np.array(ast.literal_eval(line)))
#         # return parameters
#         return weights, biases, kernels if kernels else None
#     if m_type == 'torch':
#         # todo
#         # set valid and required file types
#         val_files = ['params.pth']
#         req_files = val_files
#         files = []
#         # get list of files
#         for file in os.listdir(root):
#             files.append(file)
#         # check if dir includes required files
#         if not set(files).issubset(req_files):
#             raise TypeError(f'{files} does not include all required files {req_files}')
#         raise ValueError('torch data formatting is currently unsupported')
#
#
# def format_data(file_path, status_bars=True):
#     """ format data from a .csv file """
#     # find errors
#     if not file_path.endswith('.csv'):
#         raise ValueError(f'{file_path} is not a .csv file')
#     # load data
#     if status_bars:
#         print_color('loading dataframe...')
#     arr = np.array(pd.read_csv(file_path)).tolist()
#     # reformat data
#     for i in tqdm(range(len(arr)), ncols=100, desc='formatting', disable=not status_bars, bar_format=tqdm_color):
#         arr[i] = np.array([arr[i]])
#     # return data
#     return np.array(arr)
#
#
# def format_data_raw(df, status_bars=True):
#     """ format data from a pandas dataframe """
#     arr = np.array(df).tolist()
#     for i in tqdm(range(len(arr)), ncols=100, desc='formatting', disable=not status_bars, bar_format=tqdm_color):
#         arr[i] = np.array([arr[i]])
#     # return processed_data
#     return np.array(arr)
#
#
# def save_parameters(file_path, parameters, status_bars=True):
#     """ save parameters into a .txt file """
#     # find errors
#     if not file_path.endswith('.txt'):
#         raise ValueError(f'{file_path} is not a .txt file')
#     # save parameters
#     with open(file_path, 'w') as f:
#         for layer in tqdm(range(len(parameters)), ncols=100, desc='saving', disable=not status_bars, bar_format=tqdm_color):
#             f.write(str(parameters[layer].tolist()) + "\n")
#     return None
