import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, default='./Results', required=True)
parser.add_argument('-t', '--target_lang', type=str, default='Chinese')
args = parser.parse_args()

result_dic = {}

key_order = ["gpt-neo_125M","bloom_560m","bloom_1b1", "gpt-neo_1.3B", "bloom_1b7","gpt-neo_2.7B", "bloom_3b"]

for model in key_order:
    general_model = model.split("_")[0]
    model_size = model.split("_")[1]
    dir = os.listdir(os.path.join(args.path, general_model))
    file = [filename for filename in dir if filename.startswith(f"{general_model}_{args.target_lang}_{model_size}")][0]
    with open(os.path.join(args.path, general_model, file), "r", encoding="utf-8") as f:
        file_parts = file.split("_")
        model_name = file_parts[0] + "_" + file_parts[2]
        target_lang = file_parts[1]
        lines = f.read().splitlines()
        metric1 = lines[1].split("; ")
        top1 = str(metric1[0].split(": ")[1])
        topk = str(metric1[1].split(": ")[1])
        metric2 = lines[3].split("; ")
        pos_log = str(metric2[0].split(": ")[1])
        neg_log = str(metric2[1].split(": ")[1])

        num_correct = 0
        count = 0
        for line in lines[5:]:
            parts = line.split("\t")
            top1_trans = parts[2]
            correct_translations = eval(parts[4])
            if top1_trans in correct_translations:
                num_correct += 1
            count += 1
        
        result_dic[model_name] = {}
        result_dic[model_name][target_lang] = [top1, topk, pos_log, neg_log, round(num_correct/count, 6)]


def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, round(y[i],3), round(y[i],3), ha = 'center')

def plot_metric(sizes, list, title,ylabel, colors, save_path):
    fig = plt.figure(1, [12, 8])
    fig.clf()
    ax = fig.add_subplot(111)
    ax.bar(sizes, list, width=0.6, color=colors)
    addlabels(sizes, list)
    plt.xlabel("Model Size")
    plt.ylabel(ylabel)
    plt.title(title)
    #plt.setp(ax.get_xticklabels(), fontsize=10, rotation='vertical')
    fig.savefig(save_path)
    plt.show()


def get_ith_element(dic, lang, i):
    res = np.zeros(len(dic))
    keys = list(dic.keys())
    for j in range(len(keys)):
        res[j] = dic[keys[j]][lang][i]
    return res

lang = args.target_lang

com_color = ["orange", "steelblue","steelblue","orange", "steelblue","orange","steelblue"]

plot_metric(result_dic.keys(), get_ith_element(result_dic, lang, 0), "Percentage of Examples that the Top 1 is correct", "Percentage", colors=com_color, save_path=f"./Results/plots/{lang}_top1.png")

plot_metric(result_dic.keys(), get_ith_element(result_dic, lang, 1), "Percentage of Examples that Top K is correct", "Percentage", colors=com_color, save_path=f"./Results/plots/{lang}_topK.png")

plot_metric(result_dic.keys(), get_ith_element(result_dic, lang, 2), "Average Correct Log-Likelihood by Using the Metric 2", "Average Log-Likelihood", colors=com_color, save_path=f"./Results/plots/{lang}_correct.png")

plot_metric(result_dic.keys(), get_ith_element(result_dic, lang, 3), "Average Incorrect Log-Likelihood by Using the Metric 2", "Average Log-Likelihood", colors=com_color, save_path=f"./Results/plots/{lang}_incorrect.png")

plot_metric(result_dic.keys(), (get_ith_element(result_dic, lang, 3)/get_ith_element(result_dic, lang, 2)), "Ratios of Two Log-Likelihoods by Using the Metric 2", "Average Log-Likelihood", colors=com_color, save_path=f"./Results/plots/{lang}_ratio_log.png")

plot_metric(result_dic.keys(), get_ith_element(result_dic, lang, 4), "WSD Accuracy", "Percentage", colors=com_color, save_path=f"./Results/plots/{lang}_WSD_Acc.png")


