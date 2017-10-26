import random, sys
import xml.etree.ElementTree as ET

def get_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    root = [rev for rev in root]
    return root

root = get_xml(sys.argv[1])

random.shuffle(root)


train = root[:1700]
test = root[1700:]

## for train
a = ET.Element('train_root')
for e in train:
    a.append(e)

ET.ElementTree(a).write("small_train.xml")


## for test
b = ET.Element('test_root')
for e in test:
    b.append(e)

ET.ElementTree(b).write("small_test.xml")
