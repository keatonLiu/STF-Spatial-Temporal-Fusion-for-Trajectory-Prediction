import json

import matplotlib.pyplot as plt

# 假设你的 loss 数据存储在一个列表中
with open('log/log_test.json', 'r') as f:
    loss_list = json.load(f)
epochs = range(1, len(loss_list) + 1)  # 生成 epoch 序列

# 绘制 loss 曲线
plt.figure(figsize=(8, 5))
plt.plot(epochs, loss_list, marker='o', linestyle='-', color='b', label='Loss')

# 添加标题和标签
plt.title("Loss vs Epochs")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

# 显示图像
plt.savefig('log/loss.pdf', bbox_inches='tight')

plt.show()
