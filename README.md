# 贴花投影：裁剪、图集与淡出

弹孔贴花在斜面上拉伸、边缘被切：投影没有按投影器坐标，裁剪矩形没有求交，图集 UV 越界，淡出按距离线性但没夹紧，排序没有按深度，批次没拆分，法线混合没归一化，透明度混合顺序错，视锥裁剪漏掉相交矩形，批量贴花只提交一半。

## 目录结构

```
README.md
conftest.py
.gitignore
render/__init__.py
render/decals.py
tests/test_decals.py
```

## 当前状态

`render/decals.py` 中所有函数只保留签名与文档字符串，函数体统一
`raise NotImplementedError`。`tests/test_decals.py` 有 15 个参数化用例，
初始全部失败。

## 需要修复的 10 个问题

1. 按投影器坐标投影
2. 裁剪矩形求交
3. 图集 UV 计算
4. 淡出距离夹紧
5. 贴花按深度排序
6. 贴花批次拆分
7. 法线混合归一化
8. 透明度按顺序混合
9. 相交矩形也参与裁剪
10. 批量贴花统一提交

## 验收

```bash
python -m pytest -q
```

初始应得到 `15 failed`，且没有 collection error。实现 `render/decals.py`
后 15 条用例应全部通过。
