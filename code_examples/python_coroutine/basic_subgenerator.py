from pprint import pprint

#subgenerator
def power():
    print('Start subgenerator')
    result = {}
    while True:
        num = yield
        if num is None:
            print('Finish subgenerator')
            break
        print(num)
        result[num] = num**2
    return result


#delegating generator
def del_gen(results, set_id):
    while True:
        print('*'*40)
        print('Start delegating generator')
        results[set_id] = yield from power()
        print(results.keys())
        print('Finish delegating generator')
        print('*'*40)


#caller
def main(num_sets):
    results = {}
    for set_id, num_set in num_sets.items():
        collect = del_gen(results, set_id)
        next(collect)
        for num in num_set:
            print(collect.send(num))
        collect.send(None)
    return results

all_numbers = {'set1': [1, 2, 3, 4, 5],
               'set2': [10, 20, 30, 40, 50]}

result = main(all_numbers)
pprint(result)

