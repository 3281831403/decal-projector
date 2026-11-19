import pytest

from render import decals as mod

CASES = [
    ('project_point', [[3, 4], [1, 1]], [2, 3], False),
    ('clip_rect', [[0, 0, 2, 2], [1, 1, 2, 2]], [1, 1, 1, 1], False),
    ('clip_rect', [[5, 5, 1, 1], [0, 0, 2, 2]], None, False),
    ('atlas_uv', [5, 4, 2], (0.25, 0.5, 0.25, 0.5), False),
    ('fade_distance', [5, 0, 10], 0.5, True),
    ('fade_distance', [15, 0, 10], 0.0, True),
    ('sort_decals', [[('a', 1), ('b', 3), ('c', 2)]], [('b', 3), ('c', 2), ('a', 1)], False),
    ('batch_count', [100, 32], 4, False),
    ('normal_blend', [[0, 0, 1], [0, 1, 0], 0.5], [0.0, 0.7071067811865475, 0.7071067811865475], True),
    ('opacity_blend', [0.0, 1.0, 0.25], 0.25, True),
    ('cull_decals', [[[0, 0, 2, 2], [5, 5, 1, 1]], [0, 0, 3, 3]], [0], False),
    ('commit_decals', [[True, True]], True, False),
    ('project_point', [[0, 0], [0, 0]], [0, 0], False),
    ('fade_distance', [10, 0, 10], 0.0, True),
    ('atlas_uv', [0, 2, 2], (0.0, 0.0, 0.5, 0.5), False),
]


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_decals_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert result == pytest.approx(expected)
    else:
        assert result == expected
