list1=[1,2,3,4,5,6,7,8,9,10]

def two_sum(list, target):
    for i in list:
        for ii in list:
            if (int(i) + int(ii) == int(target)):
                print(f"{list.index(i)},{list.index(ii)}")
    return 0
two_sum(list1,12)