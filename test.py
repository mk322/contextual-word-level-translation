print("hi")
dic = {
    "good": (4, "32 "),
    "mid": (1, "32 "),
    "good3": (333, "32 "),
    "good4": (21231, "32 "),
}

list = [(4, "32 "), (1, "32 "), (3, "32 "), (6, "32 "), (999, "32 ")]
dic1 = sorted(list, key=lambda key: key[0])

print(dic1)