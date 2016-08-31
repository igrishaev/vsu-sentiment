
import pprint
import csv
import re
from collections import defaultdict
from functools import partial

SPLITTER = re.compile('\W*')


def init_state():
    return {
        'count': 0,
        'category': defaultdict(int),
        'feature': defaultdict(partial(defaultdict, int)),
    }


def get_features(text):
    word_list = SPLITTER.split(text)

    def criteria(word):
        return 2 <= len(word) <= 20

    def modify(word):
        return word.lower()

    return map(modify, filter(criteria, word_list))


def learn(state, text, category):

    feature_list = get_features(text)

    state['count'] += 1
    state['category'][category] += 1

    for feature in feature_list:
        state['feature'][feature][category] += 1


def parse_category(category_str):
    return bool(int(category_str))


def populate_state(state):

    with open('source.csv', 'rb') as f:

        reader = csv.reader(f)
        reader.next()  # skip header

        for row in reader:
            is_str, _category, _, text = row
            learn(state, text, parse_category(_category))

            if is_str == '5000':
                break


def f_count(state, feature, category):
    return state['feature'][feature][category]


def c_count(state, category):
    return state['category'][category]


def div(a, b):
    if a and b:
        return a / float(b)
    else:
        return 0.0


def p_feature_category(state, feature, category):
    a = f_count(state, feature, category)
    b = float(c_count(state, category))
    return div(a, b)


def get_categories(state):
    return state['category'].keys()


def p_feature_category_w(state, feature, category, weight=1, assump=0.5):
    prob = p_feature_category(state, feature, category)

    cats = get_categories(state)
    counts = [f_count(state, feature, cat) for cat in cats]
    print counts
    print cats
    totals = sum(counts)

    a = weight * assump + totals * prob
    b = weight + totals

    return div(a, b)


def pretty_print(state):
    pprint.pprint(state)


def fisher(state):
    pass


def main():
    state = init_state()
    populate_state(state)

    # pretty_print(state)
    print p_feature_category_w(state, 'love', True)


if __name__ == '__main__':
    main()
