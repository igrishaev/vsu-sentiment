
import math
import csv
import re
import json
import operator
from collections import defaultdict
from functools import partial

SPLITTER = re.compile('\W*')

_STATE_FILE = '_state.json'


class CATEGORY:
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    UNKNOWN = 'unknown'

    __ALL__ = (
        POSITIVE,
        NEGATIVE,
        UNKNOWN,
    )


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

    return map(modify, filter(criteria, word_list))


def learn(state, text, category):

    feature_list = get_features(text)

    state['count'] += 1
    state['category'][category] += 1

    for feature in feature_list:
        state['feature'][feature][category] += 1


def parse_category(category_str):
    if '0' == category_str:
        return CATEGORY.NEGATIVE
    if '1' == category_str:
        return CATEGORY.POSITIVE
    return CATEGORY.UNKNOWN


def ichain(obj, *items):

    def get_item(obj, item):
        if obj is None:
            return None
        try:
            return obj[item]
        except:
            return None

    return reduce(get_item, items, obj)


def populate_state(state):

    with open('source.csv', 'rb') as f:

        reader = csv.reader(f)
        reader.next()  # skip header

        for row in reader:
            # print row
            try:
                is_str, _category, _, text = row
            except Exception as e:
                print e
                continue

            learn(state, text, parse_category(_category))

            # if is_str == '9000':
            #     break


def f_count(state, feature, category):
    return ichain(state, 'feature', feature, category) or 0


def c_count(state, category):
    return ichain(state, 'category', category) or 0


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


# def p_feature_category_w(state, feature, category, weight=1, assump=0.5):
#     prob = p_feature_category(state, feature, category)
#     cats = get_categories(state)
#     counts = [f_count(state, feature, cat) for cat in cats]
#     totals = sum(counts)
#     a = weight * assump + totals * prob
#     b = weight + totals
#     return div(a, b)


def p_fisher_prob(state, feature, category):

    prob = p_feature_category(state, feature, category)

    category_list = get_categories(state)
    prob_list = [p_feature_category(state, feature, cat)
                 for cat in category_list]

    return div(prob, sum(prob_list))


# def invchi2(chi, df):
#     m = chi / 2.0
#     sum = term = math.exp(-m)
#     for i in range(1, df//2):
#         term *= m / i
#         sum += term
#     return min(sum, 1.0)


def p_fisher_item(state, text, category):

    feature_list = get_features(text)
    if not feature_list:
        return 0

    prob_list = [
        p_fisher_prob(state, feature, category)
        for feature in feature_list

    ]

    mult = reduce(operator.mul, prob_list, 1)
    if not mult:
        return 0

    return mult

    # score = -2 * math.log(mult)
    # return invchi2(score, len(feature_list) * 2)


def get_text_category(state, text):
    category_list = get_categories(state)

    prob_list = [p_fisher_item(state, text, cat)
                 for cat in category_list]

    pairs = zip(category_list, prob_list)
    pairs.sort(key=(lambda (cat, prob): -prob))

    return pairs[0][0]


def main():
    # state = init_state()
    # populate_state(state)
    # state_save(state)
    # exit(0)

    state = state_load()

    for text in (
            'I love you',
            'I hate you',
            'The movie was pretty good',
            'The movie was quite boring',

    ):
        print text, ' -- ', get_text_category(state, text)

    # pretty_print(state)
    # print p_feature_category_w(state, 'love', True)
    # print p_fisher(state, 'fuck', CATEGORY.NEGATIVE)

    # print p_fisher_item(state, 'I hate you', CATEGORY.NEGATIVE)
    # print p_fisher_item(state, 'I hate you', CATEGORY.POSITIVE)

    # print p_fisher_item(state, 'I love you', CATEGORY.NEGATIVE)
    # print p_fisher_item(state, 'I love you', CATEGORY.POSITIVE)

    # print p_fisher_item(state, 'kiss her hug her', CATEGORY.NEGATIVE)
    # print p_fisher_item(state, 'kiss her hug her', CATEGORY.POSITIVE)


if __name__ == '__main__':
    main()
