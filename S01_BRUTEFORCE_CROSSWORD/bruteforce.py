import enchant
import tqdm
from nltk.corpus import words
import multiprocessing
from urllib import request
import requests
from bs4 import BeautifulSoup

data = """\
EFSLCSOLRQ
LEADONQPCW
AGRJOOOSAM
HCCEKWMARS
GMEFICSNOY
NIDVENVTLJ
MYFISMDASU
OSLTTQKENX
BELLSGAQEH
PIBMOTMXKR"""


# data = """\
# ERMYEYYEPARG
# RNUYRRRPENAS
# EUPYPROLLMST
# KYOYRERYIUPR
# YRTAOBABAMBA
# MRRGLENPYLEW
# PEMAEUGEARRB
# LBPNMLEBPNRE
# EKEEOBAKARYR
# YCABNYBIPNER
# BANANARWPEEY
# BLREWAOIEAOA
# LBWATERMELON
# TKYIPAPPLERP"""


# def check_word(word, min_chars=4):
#     if len(word) >= min_chars:
#         if any(list(map(lambda x: x in words.words(), [word.lower(), word.upper(), word.capitalize()]))):
#             return word, True
#         else:
#             return word, False
#     else:
#         return word, False
# return word, word in words.words() if len(word) >= min_chars else False

def search_oald(q):
    while True:
        try:
            url = "https://www.oxfordlearnersdictionaries.com/definition/english/" + q
            rq = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
            _ = rq.text
            soup = BeautifulSoup(_, "html.parser")
            headword = pos = None
            for h1_headword in soup("h1", {"class": "headword"}):
                headword = h1_headword.text
            for p_pos in soup("span", {"class": "pos"}):
                pos = p_pos.text
            if headword and pos and pos not in ["abbreviation", "suffix", "exclamation",
                                                "prefix"] and "abbreviation" not in _:
                print(headword, pos)
                return True
            else:
                return False
        except:
            pass


def check_word(word, min_chars=4):
    if len(word) >= min_chars:
        if any(list(map(search_oald, [word.lower(), word.capitalize(), word.upper()]))):
            return word, True
        else:
            return word, False
    else:
        return word, False


if __name__ == '__main__':
    queries = list()

    # rips rows
    rows = data.split("\n")
    row_length = len(rows[0])
    for row in rows:
        for i in range(row_length + 1):
            for j in range(i + 1, row_length + 1):
                queries.extend(row[i:j].split(" "))
    # print(queries)

    # rips columns
    column_list = []
    # print(rows)
    for i in range(row_length):
        col = "".join(rows[j][i] for j in range(len(rows)))
        # print(col)
        column_list.append(col)

    column_length = len(column_list[0])
    for column in column_list:
        for i in range(column_length + 1):
            for j in range(i + 1, column_length + 1):
                queries.extend(column[i:j].split(" "))

    # rips diagonals
    diagonal_list = []
    for y in range(column_length - 1, 0, -1):
        x = 0
        result = ""
        while True:
            try:
                result += rows[y][x]
            except:
                break
            else:
                x += 1
                y += 1
        diagonal_list.append(result)

    for x in range(row_length):
        y = 0
        result = ""
        while True:
            try:
                result += rows[y][x]
            except:
                break
            else:
                x += 1
                y += 1
        diagonal_list.append(result)

    for y in range(column_length - 1, 0, -1):
        x = row_length - 1
        result = ""
        while True:
            try:
                if x < 0:
                    break
                result += rows[y][x]
            except:
                break
            else:
                x -= 1
                y += 1
        diagonal_list.append(result)

    for x in range(row_length - 1, -1, -1):
        y = 0
        result = ""
        while True:
            try:
                if x < 0:
                    break
                result += rows[y][x]
            except:
                break
            else:
                x -= 1
                y += 1
        diagonal_list.append(result)

    # print(diagonal_list)

    for diagonal in diagonal_list:
        diagonal_length = len(diagonal)
        for i in range(diagonal_length + 1):
            for j in range(i + 1, diagonal_length + 1):
                # print(diagonal[i:j])
                queries.extend(diagonal[i:j].split(" "))

    reverse_queries = [x[::-1] for x in queries]

    process_pool = multiprocessing.Pool(multiprocessing.cpu_count())
    results = set()
    for _ in tqdm.tqdm(process_pool.imap_unordered(check_word, queries)):
        if _[1]:
            results.add(_[0])
    for _ in tqdm.tqdm(process_pool.imap_unordered(check_word, reverse_queries)):
        if _[1]:
            results.add(_[0])
    result_string = " ".join(results)
    print("The words found are:")
    print(result_string)
    with open("results.txt", "w") as file:
        print(result_string, file=file)
