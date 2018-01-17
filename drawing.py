from matplotlib import pyplot as plt

if __name__ == '__main__':
    plt.bar(('true1','false'), (10,20))
    # plt.bar(('aa',), (20,))
    plt.legend()
    plt.xlabel('words')
    plt.ylabel('rate')
    plt.title('xxxx')
    # plt.show()
    plt.savefig('bar.png')
