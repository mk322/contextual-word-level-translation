import json
import 


# Find 3 metrics

# Metric 1a: calculated percentage of examples that the top 1 translation is correct.
num_correct_top1 = len(words_dict) * 2
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        topk_translations = sorted(result_dict[(source_word, j)], key=lambda key: key[1], reverse=True)[0]
        if topk_translations[0] not in words_dict[source_word][j]:
            num_correct_top1 -= 1
            break
percent_correct_top1 = num_correct_top1 / (len(words_dict) * 2)


# Metric 1b: calculated percentage of examples that correct translations are on the top k.
num_correct_topk = len(words_dict) * 2
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        topk_translations = sorted(result_dict[(source_word, j)], key=lambda key: key[1], reverse=True)[:len(words_dict[source_word][j])]
        for top_pair in topk_translations:
            if top_pair[0] not in words_dict[source_word][j]:
                num_correct_topk -= 1
                break

percent_correct_topk = num_correct_topk / (len(words_dict) * 2)

# Metric 2: What is the average log likelihood score of the correct translations (across pairs) vs. 
# average across all other word (non correct) pairs
sum_correct_log = 0
num_correct = 0
num_wrong = 0
sum_wrong_log = 0
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        for pair in result_dict[(source_word, j)]:
            if pair[0] in words_dict[source_word][j]:
                sum_correct_log += pair[1]
                num_correct += 1
            else:
                sum_wrong_log += pair[1]
                num_wrong += 1

avg_log_correct = round(sum_correct_log / num_correct, 6)
avg_log_wrong = round(sum_wrong_log / num_wrong, 6)

# Metric 3: For words with multiple correct translations, which translations does the model give a higher log likelihood to?
top1_dict = {}
correct_dict = {}
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        correct_dict[(source_word, j//2)] = words_dict[source_word][j]
        high = -np.inf
        #if len(words_dict[source_word]) > 1:
        for pair in result_dict[(source_word, j)]:
            if (pair[0] not in wrong_word_list) and (pair[1] > high):
                high = pair[1]
                top1_dict[(source_word, j//2)] = pair

# print out the results
with open(result_txt, "w", encoding='utf-8') as r:
    print("Metric 1:", file=r)
    print(f"top1: {round(percent_correct_top1, 6)}; topk: {round(percent_correct_topk, 6)}", file=r)
    print("Metric 2", file=r) 
    print(f"average correct log-likelihood: {avg_log_correct}; average wrong log-likelihood: {avg_log_wrong}", file=r)
    print("Metric 3", file=r)
    for key in top1_dict:
        print(f"{key[0]}\t{key[1]}\t{top1_dict[key][0]}\t{top1_dict[key][1]}\t{correct_dict[key]}", file=r)

print("finish")