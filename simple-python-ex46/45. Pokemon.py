from collections import defaultdict


names = 'audino bagon baltoy banette bidoof braviary bronzor carracosta charmeleon cresselia croagunk darmanitan deino emboar emolga exeggcute gabite girafarig gulpin haxorus heatmor heatran ivysaur jellicent jumpluff kangaskhan kricketune landorus ledyba loudred lumineon lunatone machamp magnezone mamoswine nosepass petilil pidgeotto pikachu pinsir poliwrath poochyena porygon porygonz registeel relicanth remoraid rufflet sableye scolipede scrafty seakingsealeo silcoon simisear snivy snorlax spoink starly tirtouga trapinch treeckotyrogue vigoroth vulpix wailord wartortle whismur wingull yamask'.split()
def make_dic(words):
    dic = defaultdict(dict)
    for letter in [chr(x) for x in range(ord('a'), ord('z') + 1)]:
        dic[str(letter)] = {'start':0, 'end':0}
    for name in words:
        dic[name[-1]]['end'] += 1
        dic[name[0]]['start'] += 1
    to_pop = ''
    for letter, cout in dic.items():
        start = cout['start']
        end = cout['end']
        if end == 0:
            end = 0.0001
        dic[letter]['value'] = start/end
        if cout['start'] == 0 and cout['end'] == 0:
            to_pop += letter
    for letter in to_pop:
        dic.pop(letter)
    return dic

def show(test):
    for y,i in test.items():
        print(y,i)

def values(words, dic):
    with_values = {}
    for word in words:
        start = dic[word[0]]['start']
        end = dic[word[-1]]['end']
        with_values[word] = {'start':start,'end':end}
    return with_values


def do_it(pokemons, dictionary):
    size = len(pokemons)
    first = ''
    last = ''

    seq = []
    for po in range(size):
        highest_value = 0
        for letter, stats in dictionary.items():
            if stats['end'] == 0 or stats['start'] == 0:
                continue
            if stats['value'] > highest_value:
                if last  == '':
                    first = letter
                    highest_value = stats['value']
                elif letter == last:
                    first = letter
                    highest_value = stats['value']

        best = {'name': '', 'start': 0, "end": 0}
        for pokemon, stats in pokemons.items():
            start = pokemon[0]
            end = pokemon[-1]
            if start == first:
                if stats['end'] > best['end']:
                    best['name'] = pokemon
                    best['start'] = stats['start']
                    best['end'] = stats['end']
        if best['name'] != '':
            seq.append(best['name'])
            pokemons.pop(best['name'])
            last = best['name'][-1]
            dictionary[best['name'][-1]]['end'] -= 1
            dictionary[best['name'][0]]['start'] -= 1
    return seq





d = make_dic(names)
v = values(names, d)
show(d)
print(v)

output = do_it(v, d)
print('output',len(output),output)
