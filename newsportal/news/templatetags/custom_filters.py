from django import template
from Levenshtein import distance
from .filter_library import letters, bad_words


register = template.Library()
allow_value = 0.25  # допустимая погрешность для расстояние Левенштейна


@register.filter()
def censor(value: str):
    if type(value) is not str:
        raise TypeError('Фильтр применён не к строке')

    words_orig = value.split()  # оригинальный список слов и символов
    words = value.lower().split()  # делаем список для обработки
    new_words = []

    for key, val in letters.items():  # проверка замены букв на английские в словах (только односимвольных)
        for lt in val:
            for word in words:  # обходим слова из списка
                for ch in word:  # и далее посимвольно
                    if ch == lt:
                        word = word.replace(ch, key)

    i = 0  # итератор для работы со словами из списков
    for word in words:  # тут уже измененный список слов (если были символы на замену)

        new_word = words_orig[i]
        if word[0] in bad_words:
            # word = (word.replace('!', '').replace('.', '').replace('$', '')
            #         .replace(',', '').replace(':', '').replace('&', '')
            #         .replace('%', '').replace('#', ''))
            word = word.translate({ord(i): None for i in '!.,:$#%^&'})
            for bw in bad_words[word[0]]:  # список плохих слов которые начинаются на туже букву что и наше слово
                if distance(bw, word) <= len(word)*allow_value:  # тест нашего слова с плохим + расстояние Левенштейна
                    new_word = f'{words_orig[i][0]}' + '*' * (len(word) - 1)
                    break

        if len(new_word) == len(words_orig[i]):  # если в оригинале нет доп символов в конце слова
            new_words.append(new_word)
        else:  # а если есть то добавляем их к слову
            new_word += words_orig[i][len(new_word):]
            new_words.append(new_word)
        i += 1
    return ' '.join(new_words)
