class Bar(object):
    def __init__(self):
        self.value = ''
    def __get__(self, instance, owner):
        print ("returned from descriptor object")
        return [1,2,3,4,5]
    def __iter__(self, instance, value):
        print ("set in descriptor object")
        self.value = value
    def __delete__(self, instance):
        print ("deleted in descriptor object")
        del self.value
    def __getattribute__(self, item):
        print('lol')
class Foo(object):
    bar = Bar()

f = Foo()
f.bar = 10
print (f.bar)
del f.bar

for x in f:
    print(x)