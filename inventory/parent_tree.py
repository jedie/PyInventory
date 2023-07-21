class TreeNode:
    def __init__(self, pk, name, current_path):
        self.pk = pk
        self.name = name
        self.current_path = current_path
        self.parent_node = None
        self.path = None

    def _set_parent(self, parent_node):
        self.parent_node = parent_node

    def _get_path(self):
        if self.parent_node:
            parent_path = self.parent_node._get_path()
            return [*parent_path, self.name]
        else:
            return [self.name]

    def _set_tree_info(self):
        self.path = self._get_path()

    @property
    def path_string(self):
        return ' / '.join(self.path)

    def __str__(self):
        return f'pk:{self.pk} name:"{self.name}" path:"{self.path_string}"'

    def __repr__(self):
        return f'<TreeNode {self.__str__()}>'


class ValuesListTree:
    def __init__(self, values):
        nodes = {}

        # init all nodes:
        for entry in values:
            pk = entry['pk']
            name = entry['name']
            current_path = entry['path']
            nodes[pk] = TreeNode(pk=pk, name=name, current_path=current_path)

        # Set parents:
        for entry in values:
            parent_pk = entry['parent__pk']
            if parent_pk:
                pk = entry['pk']
                node = nodes[pk]
                parent_node = nodes[parent_pk]
                node._set_parent(parent_node=parent_node)

        # Set tree info:
        nodes = list(nodes.values())
        for node in nodes:
            node._set_tree_info()

        # Oder by hierarchy:
        nodes.sort(key=lambda x: x.path)

        self.nodes = nodes

    def get_tree_path(self):
        return [node.path_string for node in self.nodes]

    def get_update_path_info(self):
        update_info = {}
        for node in self.nodes:
            if node.current_path != node.path:
                update_info[node.pk] = node.path
        return update_info
