import torch
import torch.nn as nn

# 定义 GRU 模型
input_size = 10  # 输入特征维度
hidden_size = 20  # 隐藏状态维度
num_layers = 2  # GRU 层数
batch_size = 3  # 批大小
seq_len = 5  # 序列长度

gru = nn.GRU(input_size, hidden_size, num_layers)

# 输入数据 (batch_size, seq_len, input_size)
input_data = torch.randn(seq_len, batch_size, input_size)

# 初始隐藏状态 (num_layers, batch_size, hidden_size)
h0 = torch.zeros(num_layers, batch_size, hidden_size)

# 前向传播
output, hn = gru(input_data, h0)

print("Output shape:", output.shape)  # (batch_size, seq_len, hidden_size)
print("Hidden state shape:", hn.shape)  # (num_layers, batch_size, hidden_size)