import random

from inventory.parent_tree import ValuesListTree


def test_values_list_tree():
    values_list = [
        (1, '1.', None),
        (2, '1.1.', 1),
        (3, '1.1.1', 2),
        (4, '1.1.2', 2),
        (5, '1.2.', 1),
        (6, '2.', None),
    ]
    random.shuffle(values_list)
    values = [{'pk': entry[0], 'name': entry[1], 'parent__pk': entry[2], 'path': ''} for entry in values_list]
    tree = ValuesListTree(values)

    tree_path = tree.get_tree_path()
    assert tree_path == [
        '1.',
        '1. / 1.1.',
        '1. / 1.1. / 1.1.1',
        '1. / 1.1. / 1.1.2',
        '1. / 1.2.',
        '2.',
    ]
    update_path_info = tree.get_update_path_info()
    assert update_path_info == {
        1: ['1.'],
        2: ['1.', '1.1.'],
        3: ['1.', '1.1.', '1.1.1'],
        4: ['1.', '1.1.', '1.1.2'],
        5: ['1.', '1.2.'],
        6: ['2.'],
    }

    node_three = tree.nodes[2]
    assert str(node_three) == 'pk:3 name:"1.1.1" path:"1. / 1.1. / 1.1.1"'
    assert repr(node_three) == '<TreeNode pk:3 name:"1.1.1" path:"1. / 1.1. / 1.1.1">'
