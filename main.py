import numpy as np


def candidate_elimination(examples):
    '''
    Implements the Candidate Elimination algorithm.

    Parameters:
        - examples: a list of tuples, where each tuple represents an example
          and its classification. Each example is a tuple of feature values.
          For example: [(1, 0, 1, 'yes'), (0, 1, 0, 'no'), ...]

    Returns:
        - S: a set of maximally specific hypotheses
        - G: a set of maximally general hypotheses
    '''
    # Get the number of features and the target variable
    num_features = len(examples[0]) - 1
    target = examples[0][-1]

    # Initialize S and G
    S = [{(None,) * num_features: target}]
    G = [{(None,) * num_features: '?'}]

    # Iterate over each example
    for example in examples:
        x, y = example[:-1], example[-1]

        # If the example is positive
        if y == target:
            # Remove from S any hypothesis that does not cover x
            S = [hypothesis for hypothesis in S if covers(hypothesis, x)]

            # For each hypothesis in G that covers x, generalize it and add it to S
            new_S = []
            for hypothesis in G:
                if covers(hypothesis, x):
                    for h in generalize(hypothesis, x, num_features):
                        if covers_any(examples, S, h):
                            new_S.append(h)
            S += new_S

        # If the example is negative
        else:
            # Remove from G any hypothesis that covers x
            G = [hypothesis for hypothesis in G if not covers(hypothesis, x)]

            # For each hypothesis in S that does not cover x, specialize it and add it to G
            new_G = []
            for hypothesis in S:
                if not covers(hypothesis, x):
                    for h in specialize(hypothesis, x):
                        if covers_any(examples, [h], y):
                            new_G.append(h)
            G += new_G

    return S, G


def covers(hypothesis, example):
    '''
    Returns True if the hypothesis covers the example, False otherwise.
    '''
    for i in range(len(example)):
        if hypothesis[(i,)] != '?' and hypothesis[(i,)] != example[i]:
            return False
    return True


def generalize(hypothesis, example, num_features):
    '''
    Returns a list of new hypotheses generalized from the given hypothesis
    and example.
    '''
    new_hypotheses = []
    for i in range(num_features):
        if hypothesis[(i,)] == example[i]:
            continue
        new_hypothesis = dict(hypothesis)
        new_hypothesis[(i,)] = '?'
        new_hypotheses.append(new_hypothesis)
    return new_hypotheses


def covers_any(examples, hypotheses, classification):
    '''
    Returns True if any of the given hypotheses covers an example with
    the given classification, False otherwise.
    '''
    for example in examples:
        if example[-1] != classification:
            continue
        for hypothesis in hypotheses:
            if covers(hypothesis, example[:-1]):
                return True
    return False


def specialize(hypothesis, example):
    '''
    Returns a list of new hypotheses specialized from the given hypothesis
    and example.
    '''
    new_hypotheses = []
    for i in range(len(example)):



