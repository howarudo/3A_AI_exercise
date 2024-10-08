import torch
import torch.nn as nn


class DQNModel(nn.Module):
    """
    1次元ベクトルからQ値を返すQ関数モデル。
    Args:
        in_size: 入力される次元数 (例えば、EazyMazeの場合はx, y座標の2つ)
        out_size: 出力される次元数（actionの数 例えば、EazyMazeの場合は上下左右の4つ）
    """

    def __init__(self, in_size, out_size):
        """
        初期値を代入。
        """
        print('in_size:', in_size)
        print('out_size:', out_size)
        unit_sizes = [in_size, 32, 256, 128, 32, out_size]
        super(DQNModel, self).__init__()
        # self.l_1 = nn.Linear(unit_sizes[0], unit_sizes[1])
        # self.l_2 = nn.Linear(unit_sizes[1], unit_sizes[2])
        # self.l_out = nn.Linear(unit_sizes[2], out_size)
        self.layers = nn.Sequential()
        for i in range(len(unit_sizes)-1):
            self.layers.add_module('layer_{}'.format(i), nn.Linear(unit_sizes[i], unit_sizes[i+1]))
            self.layers.add_module('relu_{}'.format(i), nn.Tanhshrink())
            # self.layers.add_module('dropout_{}'.format(i), nn.Dropout(0.5))


    def forward(self, x):
        """
        順伝搬の処理を行う
        """
        # h = x
        # h = self.l_1(h)
        # h = torch.relu(h)
        # h = self.l_2(h)
        # h = torch.relu(h)
        # h = self.l_out(h)
        h = self.layers(x)
        return h
