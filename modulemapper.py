import collections


class ModuleMapper(collections.OrderedDict):

    def iloc(self, index):
        return self[list(self.keys())[index]]


if __name__ == '__main__':
    d = ModuleMapper()
    d['first'] = 111
    d['second'] = 222
    d['third'] = 333
    print(d['second'])
    print(d.iloc(0))