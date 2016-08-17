import re
def word_count(s):
    first_list = re.findall(r'[a-zA-Z]+', s)
    final_list = []
    corner_words = ["a", "the", "on", "at", "of", "upon", "in", "as"]
    for e in first_list:
        if e.lower() not in corner_words:
            final_list.append(e)
    return len(final_list)