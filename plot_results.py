import matplotlib.pyplot as plt
import numpy as np

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, round(y[i],3), round(y[i],3), ha = 'center')

def plot_metric(sizes, list, title,ylabel, colors):
    fig = plt.figure(1, [12, 8])
    fig.clf()
    ax = fig.add_subplot(111)
    ax.bar(sizes, list, width=0.6, color=colors)
    addlabels(sizes, list)
    plt.xlabel("Model Size")
    plt.ylabel(ylabel)
    plt.title(title)
    #plt.setp(ax.get_xticklabels(), fontsize=10, rotation='vertical')
    plt.show()

result_dic = {
    "GPT_125M": [0.529412, 0.147059, -6.308, -6.665],
    "Bloom_560M": [0.647059, 0.235294, -7.289, -11.489],
    "Bloom_1.1B" :[0.676471, 0.294118, -6.966, -11.075],
    "GPT_1.3B": [0.558824, 0.176471, -5.772, -6.412],
    "Bloom_1.7B": [0.764706, 0.294118, -6.514, -11.028],
    "GPT_2.7B": [0.558824, 0.205882, -5.37, -6.333],
    "Bloom_3B": [0.794118, 0.470588, -6.202, -12.481],
}

def get_ith_element(dic, i):
    res = np.zeros(len(dic))
    keys = list(dic.keys())
    for j in range(len(keys)):
        res[j] = dic[keys[j]][i]
    return res

com_metric1 = get_ith_element(result_dic, 0)
com_color = ["orange", "steelblue","steelblue","orange", "steelblue","orange","steelblue"]
plot_metric(result_dic.keys(), com_metric1, "Percentage of Examples that Top 1 is correct", "Percentage", colors=com_color)