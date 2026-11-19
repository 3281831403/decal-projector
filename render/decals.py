"""贴花投影：裁剪、图集与淡出。"""

import math


def project_point(point, projector):
    """把点投影到投影器局部坐标。

    以投影器原点为基准做分量相减，得到投影器坐标系下的坐标，
    避免贴花在斜面上按世界坐标拉伸。
    """
    return [coord - origin for coord, origin in zip(point, projector)]


def _intersects(rect, bounds):
    """判断两个 [x, y, w, h] 矩形是否相交（含边缘相切）。"""
    x, y, w, h = rect
    bx, by, bw, bh = bounds
    return not (x >= bx + bw or x + w <= bx or y >= by + bh or y + h <= by)


def clip_rect(rect, bounds):
    """裁剪矩形与边界求交。

    返回相交后的 [x, y, w, h]；完全不相交时返回 None。
    """
    x, y, w, h = rect
    bx, by, bw, bh = bounds

    x1 = max(x, bx)
    y1 = max(y, by)
    x2 = min(x + w, bx + bw)
    y2 = min(y + h, by + bh)

    if x2 < x1 or y2 < y1:
        return None

    return [x1, y1, x2 - x1, y2 - y1]


def atlas_uv(index, columns, rows):
    """图集 UV。

    按列优先把索引拆成行列，返回 (u, v, width, height)，
    并把索引夹紧到图集范围内，防止 UV 越界采样到相邻贴花。
    """
    cell_w = 1.0 / columns
    cell_h = 1.0 / rows

    index = max(0, min(index, columns * rows - 1))
    col = index % columns
    row = index // columns

    return (col * cell_w, row * cell_h, cell_w, cell_h)


def fade_distance(distance, start, end):
    """淡出距离夹紧。

    距离从 start 到 end 线性淡出到 0，结果夹紧在 [0, 1]：
    近于 start 完全不透明，远于 end 完全透明。
    """
    if distance <= start:
        return 1.0
    if distance >= end or end <= start:
        return 0.0
    return 1.0 - (distance - start) / (end - start)


def sort_decals(decals):
    """按深度从远到近排序（深度值越大越远），返回新列表。"""
    return sorted(decals, key=lambda item: item[1], reverse=True)


def batch_count(count, max_batch):
    """贴花批次拆分：返回容纳 count 个贴花所需的批次数（向上取整）。"""
    if count <= 0:
        return 0
    if max_batch <= 0:
        raise ValueError("max_batch 必须为正数")
    return (count + max_batch - 1) // max_batch


def normal_blend(a, b, weight):
    """法线混合后归一化。

    先按 weight 线性混合两条法线，再单位化，避免混合后法线变短
    导致光照发暗。零向量兜底返回零向量。
    """
    blended = [
        ax * (1.0 - weight) + bx * weight
        for ax, bx in zip(a, b)
    ]
    length = math.sqrt(sum(component * component for component in blended))
    if length == 0.0:
        return [0.0] * len(blended)
    return [component / length for component in blended]


def opacity_blend(base, decal, alpha):
    """透明度按 alpha 混合。

    贴花覆盖在基底之上：result = decal * alpha + base * (1 - alpha)，
    混合顺序不能颠倒。
    """
    return decal * alpha + base * (1.0 - alpha)


def cull_decals(rects, bounds):
    """相交矩形也参与裁剪。

    返回与 bounds 相交（含部分相交）的矩形下标列表，
    完全落在视锥外的矩形被剔除。
    """
    return [
        index
        for index, rect in enumerate(rects)
        if _intersects(rect, bounds)
    ]


def commit_decals(statuses):
    """批量贴花全部成功才提交：任一失败则整体放弃。"""
    return all(statuses)
