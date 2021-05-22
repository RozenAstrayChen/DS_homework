from collections import defaultdict
import itertools
import sys


class Apriori():
    def __init__(self, filename, sup, w_filename):
        self.filename = filename
        self.sup = sup
        self.frequecy = 0
        self.w_filename = w_filename
        # new file
        f = open(self.w_filename, "w", encoding='UTF-8')
        f.close()

    def Read_itemsets(self, f):
        row_num = f.readline()
        items = row_num.replace("\n", "").split(',')
        items = [int(x) for x in items]
        if not items:
            return None
        else:
            items = frozenset(items)
            return items

    def Read_data(self):
        itemsets = []
        with open(self.filename, 'r') as f:
            while True:
                try:
                    # load data
                    itemset = self.Read_itemsets(f)
                    itemsets.append(itemset)
                    if itemset == None:
                        break
                except BaseException:
                    break

        return itemsets

    def Generate_2items_sets(self, items):
        items = sorted(items)
        lst = []
        i = 1
        for a in items:
            for b in items[i:]:
                lst.append(frozenset([a, b]))
            i += 1
        return lst


    def Get_frequent_single_items(self, results):
        '''

        :param D: DataSet
        :param results: frequent candidates
        :return: k=2 itemsets
        '''
        f = open(self.w_filename, "a", encoding='UTF-8')

        items_counter = defaultdict(int)
        dhp = defaultdict(int)
        # generate C1
        self.frequecy = len(self.D)
        for TID in self.D:
            for itemset in TID:
                items_counter[itemset] += 1

        # count items and collect need delete items
        delete_item = set()
        single_counter = sorted(items_counter.keys())

        for k in single_counter:
            # use frequency to find
            if items_counter[k]/self.frequecy >= self.sup:
                f.writelines('%d:%.3f\n' %  (k, items_counter[k] / self.frequecy))
                #print(k, ':%.4f' %  (items_counter[k] / self.frequecy))
                results[frozenset([k])] = items_counter[k]/ self.frequecy
            else:
                delete_item.add(k)

        # delete items from D
        delete_item = sorted(delete_item)
        for i in range(len(self.D)):
            temp = self.D[i] - set(delete_item)
            self.D[i] = temp

        # generate C2:
        for TID in self.D:
            for itemset in self.Generate_2items_sets(TID):
                dhp[itemset] += 1

        f.close()
        return dhp

    def IsFrequent(self, candidates, c):
        for each in c:
            c = frozenset(c)
            one_subset = c - frozenset([each])

            if one_subset not in candidates:
                return False
        return True
    '''
    remove sort <= k-1 from DataSet
    '''
    def Filter_dataSet(self, k):
        pop_i = []
        for i in range(len(self.D)):
            sort = len(self.D[i])
            if sort <= k-1:
                pop_i.append(i)
        #print('pop', pop_i)
        # if you pop one ,the items will move ahead, so should n-1
        j = 0
        for i in pop_i:
            self.D.pop(i-j)
            j += 1

    def Generate_candidates(self, candidates, k):

        #res = set()
        res = defaultdict(int)
        for TID in self.D:
            frequent_itemset = itertools.combinations(TID, k)
            for itemset in frequent_itemset:
                if self.IsFrequent(candidates, itemset):
                    res[frozenset(itemset)] += 1

        return res


    def Count_candidates(self, candidates):
        counted = defaultdict(int)
        for TID in self.D:

            bucket = [candidate for candidate in candidates if candidate <= TID]
            for each in bucket:
                counted[each] += 1


        return counted


    def Generate_support_candidates(self, counted, support):
        results = {}
        f = open(self.w_filename, "a", encoding='UTF-8')
        for item in counted:
            if counted[item]/self.frequecy >= support:
                f.writelines('%s:%.3f\n' % (str(list(item)), counted[item] / self.frequecy))
                #print(item, ':%.4f' % (counted[item]/self.frequecy))
                results.update({item: counted[item]})
        f.close()
        return results

    def Apriori(self):
        results = {}
        support_candidates = {}
        f = open(self.w_filename, "a", encoding='UTF-8')
        self.D = self.Read_data()
        candidates = self.Get_frequent_single_items(results)

        if candidates:
            for item in candidates:
                if candidates[item]/self.frequecy >= self.sup:
                    #print(item,':%.4f' % (candidates[item]/self.frequecy))
                    f.writelines('%s:%.3f\n' % (str(list(item)), candidates[item] / self.frequecy))
                    support_candidates.update({item: candidates[item]})

        f.close()
        results.update(support_candidates)
        candidates = support_candidates
        k = 3

        while candidates:
            self.Filter_dataSet(k)
            candidates =self.Generate_candidates(candidates.keys(), k)

            if not candidates: break
            candidates = self.Generate_support_candidates(candidates, self.sup)
            results.update(candidates)
            #print('L%s====================================' % (k))

            k += 1



ap = Apriori(filename=str(sys.argv[2]), sup=float(sys.argv[1]), w_filename=str(sys.argv[3]))
#ap = Apriori(filename='sample.txt', sup=0.2, w_filename='123.txt')

ap.Apriori()