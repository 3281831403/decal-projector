"""贴花投影：裁剪、图集与淡出：待实现的核心模块。"""


def project_point(point, projector):
    """把点投影到投影器局部坐标。"""
    raise NotImplementedError

def clip_rect(rect, bounds):
    """裁剪矩形与边界求交。"""
    raise NotImplementedError

def atlas_uv(index, columns, rows):
    """图集 UV。"""
    raise NotImplementedError

def fade_distance(distance, start, end):
    """淡出距离夹紧。"""
    raise NotImplementedError

def sort_decals(decals):
    """按深度从远到近排序。"""
    raise NotImplementedError

def batch_count(count, max_batch):
    """贴花批次拆分。"""
    raise NotImplementedError

def normal_blend(a, b, weight):
    """法线混合后归一化。"""
    raise NotImplementedError

def opacity_blend(base, decal, alpha):
    """透明度按 alpha 混合。"""
    raise NotImplementedError

def cull_decals(rects, bounds):
    """相交矩形也参与裁剪。"""
    raise NotImplementedError

def commit_decals(statuses):
    """批量贴花全部成功才提交。"""
    raise NotImplementedError
