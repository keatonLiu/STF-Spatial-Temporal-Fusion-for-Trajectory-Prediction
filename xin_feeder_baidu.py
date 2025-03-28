import pickle

import numpy as np
import torch

from layers.graph import Graph


class DataSet(torch.utils.data.Dataset):
    """ Feeder for skeleton-based action recognition
    Arguments:
        data_path: the path to '.npy' data, the shape of data should be (N, C, T, V, M)
    """

    def __init__(self, data_path, graph_args={}, train_val_test='train'):
        '''
        train_val_test: (train, val, test)
        '''
        self.data_path = data_path
        self.load_data()

        total_num = len(self.all_feature)
        # print('Total number:',total_num)###'train':5010, 'test':415,'val':5010
        # equally choose validation set
        train_id_list = list(np.linspace(0, total_num - 1, int(total_num * 0.8)).astype(int))
        val_id_list = list(set(list(range(total_num))) - set(train_id_list))

        # # last 20% data as validation set
        self.train_val_test = train_val_test

        if train_val_test.lower() == 'train':
            self.all_feature = self.all_feature[train_id_list]
            self.all_adjacency = self.all_adjacency[train_id_list]
            self.all_adjacency_biggraph = self.all_adjacency_biggraph[train_id_list]  ##new
            self.all_mean_xy = self.all_mean_xy[train_id_list]
        elif train_val_test.lower() == 'val':
            self.all_feature = self.all_feature[val_id_list]
            self.all_adjacency = self.all_adjacency[val_id_list]
            self.all_adjacency_biggraph = self.all_adjacency_biggraph[val_id_list]  # new
            self.all_mean_xy = self.all_mean_xy[val_id_list]

        self.graph = Graph(**graph_args)  # num_node = 120,max_hop = 1

    def load_data(self):
        with open(self.data_path, 'rb') as reader:
            # Training (N, C, T, V)=(5010, 11, 12, 120),(5010,720,720) (5010, 120, 120), (5010, 2)
            [self.all_feature, self.all_adjacency, self.all_adjacency_biggraph, self.all_mean_xy] = pickle.load(reader)
        print('self.all_feature shape in xin_feeder_baidu', self.all_feature.shape)
        print('self.all_adjacency shape in xin_feeder_baidu', self.all_adjacency.shape)
        print('self.all_adjacency_biggraph shape in xin_feeder_baidu',self.all_adjacency_biggraph.shape)#
        print('self.all_mean_xy shape in xin_feeder_baidu', self.all_mean_xy.shape)

    def __len__(self):
        return len(self.all_feature)

    def __getitem__(self, idx):
        # C = 11: [frame_id, object_id, object_type, position_x, position_y, position_z, object_length, pbject_width, pbject_height, heading] + [mask]
        print(f"idx in xin_feeder_baidu: {idx}")
        now_feature = self.all_feature[idx].copy()  # (C, T, V) = (11, 12, 120)
        print('now_feature shape in xin_feeder_baidu', now_feature.shape)
        now_mean_xy = self.all_mean_xy[idx].copy()  # (2,) = (x, y)
        print('now_mean_xy shape in xin_feeder_baidu', now_mean_xy.shape)

        # if self.train_val_test.lower() == 'train' and np.random.random() > 0.5:
        #     angle = 2 * np.pi * np.random.random()
        #     sin_angle = np.sin(angle)
        #     cos_angle = np.cos(angle)
        #
        #     angle_mat = np.array(
        #         [[cos_angle, -sin_angle],
        #          [sin_angle, cos_angle]])
        #
        #     xy = now_feature[3:5, :, :]  # (2,T,V)=(2,12,120)
        #     num_xy = np.sum(xy.sum(axis=0).sum(axis=0) != 0)  # get the number of valid data
        #
        #     # angle_mat: (2, 2), xy: (2, 12, 120)
        #     out_xy = np.einsum('ab,btv->atv', angle_mat, xy)
        #     now_mean_xy = np.matmul(angle_mat, now_mean_xy)
        #     xy[:, :, :num_xy] = out_xy[:, :, :num_xy]
        #
        #     now_feature[3:5, :, :] = xy  # (2,T, V_valid)=(2,12, n(<120))

        now_adjacency = self.graph.get_adjacency(self.all_adjacency[idx])  ##self.all_adjacency[idx]=(120,120)
        print(f"now_adjacency shape in xin_feeder_baidu: {now_adjacency.shape}")
        now_A = self.graph.normalize_adjacency(now_adjacency)
        print(f"now_A shape in xin_feeder_baidu: {now_A.shape}")
        now_A_biggraph = self.all_adjacency_biggraph[idx]  # new
        print(f"now_A_biggraph shape in xin_feeder_baidu: {now_A_biggraph.shape}")
        return now_feature, now_A, now_A_biggraph, now_mean_xy
