nodes = {}
instructions = []
with open('./2015/7.txt') as f:
    for line in f.readlines():
        line = line.strip()
        instructions.append(line)

class Node:
    def __init__(self, name, value=None, left=None, right=None, op=None):
        self.name = name
        self.value = value
        self.left = left
        self.right = right
        self.op = op

    def __repr__(self): 
        return f'Node({self.name}, {self.value}, {self.left}, {self.right}, {self.op})'
    def __str__(self):
        return self.__repr__()

def loadInstructions():
    for i in instructions:
        nodeName = i.split(' ')[-1]
        if 'AND' in i:
            left, right = i.split(' AND ')
            left = left.split(' ')[0]
            right = right.split(' ')[0]
            if left.isdigit():
                left = int(left)
            if right.isdigit():
                right = int(right)
            nodes[nodeName] = Node(nodeName, None, left, right, 'AND')
        elif 'OR' in i:
            left, right = i.split(' OR ')
            left = left.split(' ')[0]
            right = right.split(' ')[0]
            if left.isdigit():
                left = int(left)
            if right.isdigit():
                right = int(right)
            nodes[nodeName] = Node(nodeName, None, left, right, 'OR')
        elif 'NOT' in i:
            left = i.split(' ')[1]
            if left.isdigit():
                left = int(left)
            nodes[nodeName] = Node(nodeName, None, left, None, 'NOT')
        elif 'LSHIFT' in i:
            left, right = i.split(' LSHIFT ')
            left = left.split(' ')[0]
            right = right.split(' ')[0]
            if left.isdigit():
                left = int(left)
            if right.isdigit():
                right = int(right)
            nodes[nodeName] = Node(nodeName, None, left, right, 'LSHIFT')
        elif 'RSHIFT' in i:
            left, right = i.split(' RSHIFT ')
            left = left.split(' ')[0]
            right = right.split(' ')[0]
            if left.isdigit():
                left = int(left)
            if right.isdigit():
                right = int(right)
            nodes[nodeName] = Node(nodeName, None, left, right, 'RSHIFT')
        else: # literal
            left = i.split(' ')[0]
            if left.isdigit():
                left = int(left)
            nodes[nodeName] = Node(nodeName, left, None, None, None)

def get_value(nodeName):
    if isinstance(nodeName, int):
        return nodeName
    node = nodes[nodeName]
    if node.value is not None:
        return get_value(node.value)
    if node.op is None:
        node.value = get_value(node.left)
        node.value = node.value & 0xffff        
        return node.value
    if node.op == 'NOT':
        node.value = ~get_value(node.left)
        node.value = node.value & 0xffff
        return node.value
    if node.op == 'AND':
        node.value = get_value(node.left) & get_value(node.right)
        node.value = node.value & 0xffff
        return node.value
    if node.op == 'OR':
        node.value = get_value(node.left) | get_value(node.right)
        node.value = node.value & 0xffff
        return node.value
    if node.op == 'LSHIFT':
        node.value = get_value(node.left) << get_value(node.right)
        node.value = node.value & 0xffff
        return node.value
    if node.op == 'RSHIFT':
        node.value = get_value(node.left) >> get_value(node.right)
        node.value = node.value & 0xffff
        return node.value


# part 1
loadInstructions()
aVal = get_value('a')
print(aVal)

# part 2
nodes = {}
loadInstructions()    
nodes['b'] = Node('b', aVal, None, None, None)
aVal = get_value('a')
print(aVal)