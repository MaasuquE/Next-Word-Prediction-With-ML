train_data = 'test_text.txt'

first_possible_words = {}
second_possible_words = {}
transitions = {}

def expandDict(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)
    
def get_next_probability(given_list):   #returns dictionary
    probability_dict = {}
    given_list_length = len(given_list)
    for item in given_list:
        probability_dict[item] = probability_dict.get(item, 0) + 1
    for key, value in probability_dict.items():
        probability_dict[key] = value / given_list_length
    return probability_dict

def trainMarkovModel():
    for line in open(train_data):
        tokens = line.rstrip().lower().split()
        tokens_length = len(tokens)
        for i in range(tokens_length):
            token = tokens[i]
            if i == 0:
                first_possible_words[token] = first_possible_words.get(token, 0) + 1
            else:
                prev_token = tokens[i - 1]
                if i == tokens_length - 1:
                    expandDict(transitions, (prev_token, token), 'END')
                if i == 1:
                    expandDict(second_possible_words, prev_token, token)
                else:
                    prev_prev_token = tokens[i - 2]
                    expandDict(transitions, (prev_prev_token, prev_token), token)
    
    first_possible_words_total = sum(first_possible_words.values())
    for key, value in first_possible_words.items():
        first_possible_words[key] = value / first_possible_words_total
        
    for prev_word, next_word_list in second_possible_words.items():
        second_possible_words[prev_word] = get_next_probability(next_word_list)
        
    for word_pair, next_word_list in transitions.items():
        transitions[word_pair] = get_next_probability(next_word_list)
    

