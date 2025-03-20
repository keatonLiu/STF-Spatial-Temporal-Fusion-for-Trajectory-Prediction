import json
import re
data = {}
with open('log/log_test.txt', 'r') as f:
    for line in f:
        if 'Epoch:' in line:
            """|2025-02-16 19:43:28.539270|     Epoch:   0/ 226|	Iteration:    0|	Loss:0.75477511|lr: 0.001|"""
            mt = re.search(r'Epoch:\s*(\d+).*?Loss:(.*?)\|', line)
            try:
                epoch = int(mt.group(1))
                loss = float(mt.group(2))
                data[epoch] = loss
            except:
                print(line)

with open('log/log_test.json', 'w') as f:
    json.dump(list(data.values()), f, ensure_ascii=False, indent=4)
