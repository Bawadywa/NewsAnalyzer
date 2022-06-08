import re
import pandas as pd

bad_words = ('фото', 'відео', 'змі', 'про',
             'них', 'від', 'під', 'при',
             'для', 'три', 'над', 'нас',
             'так', 'але', 'кого', 'проти',
             'через', 'щодо', 'один', 'два',
             'перед', 'вже', 'понад', 'після',
             'вперше', 'знову', 'вас', 'серед')

word_ends = ('вати', 'ує', 'ає', 'іли',
             'ює', 'гти', 'ила', 'ться',
             'іла', 'али', 'вся', 'или',
             'ив', 'шла', 'яли', 'ять',
             'ано', 'ють', 'ити', 'ів',
             'яє', 'яв', 'сло', 'ати',
             'ала', 'ить', 'уть', 'ав',
             'ула', 'уло', 'ути', 'йти',
             'ило', 'шов', 'ало', 'гла',
             'ули', 'ося', 'шло', 'ило',
             'оже', 'йти', 'омо', 'иті',
             'ені', 'ліг', 'ели', 'ася',
             'ися', 'ного', 'лого', 'ено',
             'іде', 'сть', 'ий', 'ій', 'их',
             'іх')

word_starts = ('стан', 'сво', 'хоч', 'перш',
               'млр', 'тися', 'сот', 'нов',
               'близ', 'гото', 'міль', 'сто',
               'най', 'потр', 'біль', 'менш',
               'біля', 'чому', 'майж', 'може',
               'буде', 'кому', 'без', 'коли',
               'поча', 'його', 'йому', 'як',
               'друг', 'сам', 'мож', 'вели',
               'багат', 'мал', 'вон', 'лиш',
               'дуж', 'дво', 'поки', 'досі',
               'вед', 'цьо', 'ці', 'то',
               'потім', 'треба')


def make_forbidden_words():
    words = []
    for word in bad_words:
        words.append(word)
        words.append(word.upper())
        words.append(word.capitalize())
    return tuple(words)


forbidden_words = make_forbidden_words()


def merge_similar(words):
    words_copy = words[:]
    merged_words = []

    for item in words:
        if item not in words_copy:
            continue
        word = item[0]
        main_part = word[:int(len(word) * 0.75) + 1]
        amount = 0
        remove_items = []
        for compare_item in words_copy:
            compare_word = compare_item[0]
            if compare_word.startswith(main_part):
                amount += compare_item[1]
                remove_items.append(compare_item)

        for remove_item in remove_items:
            words_copy.remove(remove_item)

        merged_words.append((word, amount))

    merged_words.sort(key=lambda tup: tup[1], reverse=True)
    return merged_words


def merge(old_words, new_words):
    merged_words = []

    for item in old_words:
        word = item[0]
        main_part = word[:int(len(word) * 0.5) + 1]
        amount = 0
        remove_items = []
        flag_present = False
        for new_item in new_words:
            new_word = new_item[0]
            if new_word.startswith(main_part):
                amount += new_item[1]
                remove_items.append(new_item)
                flag_present = True

        for remove_item in remove_items:
            new_words.remove(remove_item)
        if flag_present:
            merged_words.append((word, amount))
        else:
            merged_words.append((word, 0))

    return merged_words


def extract_data(file_news, file_stat):
    all_words = []
    with open(file_news, 'r', encoding='utf-8') as file:
        content = file.read()
        if len(content) > 0:
            news = content.lower().replace(',', '').replace('.', '').replace('\"', '').replace('!', '').replace('?', '')\
                   .replace(':', '')
        else:
            return

    split_news = news.split()
    words = set(list(filter(lambda word: len(word) > 3, split_news)))

    clean_words = set()
    for word in words:
        match = re.fullmatch(r"[а-щА-ЩЬьЮюЯяЇїІіЄєҐ']{3,}", word)
        if match:
            word = match.group(0)
            flag = False
            for end in word_ends:
                if end in word[-4:]:
                    flag = True
                    break
            for start in word_starts:
                if start in word[:4]:
                    flag = True
                    break
            if not flag:
                clean_words.add(word)
    clean_words = clean_words.difference(set(forbidden_words))

    stat_words = list([(word, split_news.count(word)) for word in clean_words])
    stat_words.sort(key=lambda tup: tup[1], reverse=True)

    result_words = merge_similar(stat_words)

    worksheet = pd.read_excel(file_stat, engine='openpyxl', index_col=0)

    day = 1
    day_pattern = '{} day'
    day_string = day_pattern.format(day)
    columns = ['word']
    if worksheet.empty:
        result_words = result_words[:50]
        df = pd.DataFrame(result_words)
        columns.append(day_string)
        df.columns = columns
        with pd.ExcelWriter(file_stat, engine='openpyxl') as writer:
            df.to_excel(writer)
        all_words = result_words
    else:
        old_words = worksheet[worksheet.columns[0:2]].values.tolist()
        merged_words = merge(old_words, result_words)
        df = pd.DataFrame(merged_words)
        last_day = int(worksheet.columns[-1].split()[0])
        day = last_day + 1
        day_string = day_pattern.format(day)
        columns.append(day_string)
        df.columns = columns
        new_worksheet = pd.merge(worksheet, df, on='word')
        with pd.ExcelWriter(file_stat, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            new_worksheet.to_excel(writer)
        all_words = old_words
    return all_words


def get_all_words(file_stat):
    worksheet = pd.read_excel(file_stat, engine='openpyxl', index_col=0)
    all_words = []
    if not worksheet.empty:
        all_words = worksheet.loc[:, "word"].values.tolist()
    return all_words
