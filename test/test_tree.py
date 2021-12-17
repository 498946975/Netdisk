"""
测试权限树
"""
datas = [
    {"id": 1, "name": "用户管理", "father_id": 0},
    {"id": 2, "name": "用户列表", "father_id": 1},  # 是id为1的子权限
    {"id": 3, "name": "部门管理", "father_id": 0},
    {"id": 4, "name": "部门列表", "father_id": 3},  # 是id为3的子权限
    {"id": 5, "name": "用户校验", "father_id": 1},  # 是id为3的子权限
]

trees = []

# 一级菜单
for data in datas:
    # 判断是不是一级菜单
    if data["father_id"] == 0:
        first_level = {
            "id": data["id"],
            "label": data["name"],
            "children": []
        }
        trees.append(first_level)

# 二级菜单
for first_level in trees:
    # 拿到一级菜单的id
    id = first_level["id"]
    for data in datas:
        # 判断二级菜单的father_id是否等于一级菜单的id
        if data["father_id"] == id:
            two_level = {
                "id": data["id"],
                "label": data["name"],
                "children": []
            }
            first_level["children"].append(two_level)

import json

print(json.dumps(trees))
