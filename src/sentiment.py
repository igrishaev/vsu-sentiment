
import os
import math
import csv
import re
import json
import operator
from collections import defaultdict
from functools import partial

import f

SPLITTER = re.compile('\W*')

_STATE_FILE = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        '_state.json'
    ))


class CATEGORY:
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    UNKNOWN = 'unknown'

    __ALL__ = (
        POSITIVE,
        NEGATIVE,
        UNKNOWN,
    )


THRESHOLD = {
    CATEGORY.POSITIVE: 0.7,
    CATEGORY.NEGATIVE: 0.7,
    CATEGORY.UNKNOWN: 0,
}


def state_save(state):
    with open(_STATE_FILE, 'wb') as f:
        json.dump(state, f)


def state_load():
    with open(_STATE_FILE, 'rb') as f:
        return json.load(f)


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

    return set(map(modify, filter(criteria, word_list)))


def learn(state, text, category):

    state['count'] += 1
    state['category'][category] += 1

    feature_set = get_features(text)
    for feature in feature_set:
        state['feature'][feature][category] += 1


def parse_category(category_str):
    if '0' == category_str:
        return CATEGORY.NEGATIVE
    if '1' == category_str:
        return CATEGORY.POSITIVE
    return CATEGORY.UNKNOWN


def populate_state(state):

    with open('source.csv', 'rb') as f:

        reader = csv.reader(f)
        reader.next()  # skip header

        for row in reader:

            try:
                # some rows are corrupted
                is_str, _category, _, text = row
            except Exception as e:
                continue

            learn(state, text, parse_category(_category))


def f_count(state, feature, category):
    return f.ichain(state, 'feature', feature, category) or 0


def c_count(state, category):
    return f.ichain(state, 'category', category) or 0


def div(a, b):
    if a and b:
        return a / float(b)
    else:
        return 0.0


def p_feature_category(state, feature, category):
    return div(
        f_count(state, feature, category),
        c_count(state, category)
    )


def get_categories(state):
    return state['category'].keys()


def p_feature_category_w(state, feature, category, weight=1, assump=0.5):
    prob = p_feature_category(state, feature, category)
    cats = get_categories(state)
    counts = [f_count(state, feature, cat) for cat in cats]
    totals = sum(counts)
    a = weight * assump + totals * prob
    b = weight + totals
    return div(a, b)


def p_category(state, category):
    a = state['category'][category]
    b = state['count']
    # a = f.ichain(state, 'category', category) or 0
    # b = f.ichain(state, 'count') or 0
    return div(a, b)


def p_item(state):
    a = 1
    b = f.ichain(state, 'count') or 0
    return div(1, b)


def p_item_cat(state, item, cat):
    feature_set = get_features(item)
    probs = [
        p_feature_category_w(state, feature, cat)
        for feature in feature_set
    ]
    return reduce(operator.mul, probs, 1)


def p_cat_item(state, item, cat):
    return p_item_cat(state, item, cat) * p_category(state, cat)


def coerce_category(ratio_pairs):

    for (cat, rat) in sorted(ratio_pairs, key=lambda (cat, rat): -rat):
        if rat > THRESHOLD[cat]:
            return cat

    return CATEGORY.UNKNOWN


def get_ratio_pairs(pair_list):
    prob_sum = sum([prob for (_, prob) in pair_list])
    ratio_list = [div(prob, prob_sum) for (_, prob) in pair_list]
    composed = [
        (cat, rat)
        for ((cat, _), rat)
        in zip(pair_list, ratio_list)
    ]
    return composed


def get_text_category(state, text):
    category_list = get_categories(state)

    prob_list = [p_cat_item(state, text, cat)
                 for cat in category_list]

    pairs = zip(category_list, prob_list)
    ratio_pairs = get_ratio_pairs(pairs)

    return coerce_category(ratio_pairs)


def learn_save_quit():
    state = init_state()
    populate_state(state)
    state_save(state)
    exit(0)


def main():
    learn_save_quit()

    # state = state_load()
    # print get_text_category(state, 'dsfgsdfg88sfsd')
    # print get_text_category(state, 'love')
    # print get_text_category(state, 'hate')


if __name__ == '__main__':
    main()
