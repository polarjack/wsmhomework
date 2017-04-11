import nltk
import math
import operator
test = []

test.append(["c", 100])
test.append(["m", 38134])
test.append(["a", 1])
test.append(["x", 1883])
test.append(["y", 993])




second = {}
second["a"] = 12321

second["b"] = 12
second["y"] = 78
second["t"] = 911
second["m"] = 200
second["p"] = 166
sorts = sorted(second.items(), key=operator.itemgetter(1))
sorts.reverse()
print(sorts)

for s,v in sorts:
    print(s, v)

