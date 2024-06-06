windowW = 1000
windowH = 700

fps = 60

blockMap1 = [
    '          ',
    '1111111111',
    '          ',
    '1111111111',
    '          ',
    '1111111111',
    '          ',
    '          ',
    '          ',
    '          ',
    '          ',
    '          ']

blockMapTest = [
    '          ',
    ' 1        ',
    '          ',
    '          ',
    '          ',
    '          ',
    '          ',
    '          ',
    '          ',
    '          ',
    '          ',
    '          ']

colorLegend = {
    '0' : 'gray',
    '1' : 'blue',
    '2' : 'red',
    '3' : 'green'
    }

blockHeight = windowH / len(blockMap1)
blockWidth = windowW / len(blockMap1[0])

upgrades = ['speed+', 'size+', 'speed-', 'size-']