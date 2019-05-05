import synonyms


def getTop10(Allwords, Allbag_file='work2vec/bag.txt'):
    user_words = Allwords
    with open(Allbag_file, 'r') as f:
        text = f.read()
        all_bag = text.split(',')

    bag_num = dict()
    bag_len = len(all_bag)
    for i in range(bag_len):
        num = 0
        for word in user_words:
            num = num + synonyms.compare(word, all_bag[i])/bag_len
        bag_num[all_bag[i]] = num

    test_dict = sorted(bag_num.items(), key=lambda e: e[1], reverse=True)[:10]

    re_list = []
    for one in test_dict:
        re_list.append(one[0])
    return re_list


if __name__ == '__main__':
    # words = ['篮球', '足球', '化妆品']
    # result = getTop10(words)
    # print(result)
    s = 'haha,hahahaha1'
    s = s.split(',')
    print(s)
