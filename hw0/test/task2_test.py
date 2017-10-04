from task2 import Node, Solution

def test0():
    '''9 + 15 = 24'''
    root = Node(3)
    root.left = Node(9)
    root.right = Node(20)
    root.right.left = Node(15)
    root.right.right = Node(7)
    return root

def test1():
    '''0'''
    root = Node(1)
    return root

def test2():
    '''16 + 128 = 144'''
    root = Node(1)
    root.left = Node(2)
    root.left.left = Node(4)
    root.left.left.right = Node(8)
    root.left.left.right.left = Node(16)
    root.left.left.right.right = Node(32)
    root.right = Node(64)
    root.right.left = Node(128)
    root.right.right = Node(256)
    return root

if __name__ == '__main__':
    test_data = [
            test0(),
            test1(),
            test2()
            ]
    sol = Solution()
    for i,root in enumerate(test_data):
        print 'test ' + str(i) + ':'
        print sol.sumOfLeftLeaves(root)
