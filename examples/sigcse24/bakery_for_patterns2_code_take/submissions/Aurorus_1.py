from bakery import assert_equal
def until_period(words:list[str])->list[str]:
    newords=[]
    take=True
    for word in words:
        if '.' in word:
            take=False
            return take
        else:
            newords=newords.append(word)
            return newords
assert_equal(until_period(['a','.','b']),['a'])