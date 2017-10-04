from task1 import twoSum

if __name__ == "__main__":
    test_data = [
            { # ans: [0, 3]
                'nums': [2, 7, 11, 15],
                'target': 17,
            },
            { # ans: [0, 1]
                'nums': [1, 2],
                'target': 3,
            },
            { # ans: [1, 3]
                'nums': [1, 2, 4, 8, 16],
                'target': 10,
            },
            { # ans: [1, 2]
                'nums': [1, 2, 2, 8, 16],
                'target': 4,
            },
        ]
    for i,test in enumerate(test_data):
        ans = twoSum(test['nums'], test['target'])
        print 'test ' + str(i) + ':'
        print ans
