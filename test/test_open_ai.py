from tools.open_ai import *
data = {}
print(data.get("node_id",''))
title = "天气不错，"
content = "天气不错，今天适合出行。"
result = analyze_potential_customer(title, content)
print(result)