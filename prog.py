import random
from razdel import tokenize
from pymorphy3 import MorphAnalyzer

def generate_line(word, sample_dict):
    pm = MorphAnalyzer()
    normal = pm.parse(word)[0].normal_form
    all_variants = []
    others = []
    for idx in sample_dict.keys():
        normal_forms = sample_dict[idx][1]
        if normal in normal_forms:
            all_variants.append(sample_dict[idx][0])
        else:
            others.append(sample_dict[idx][0])
    to_choose_from = random.sample(all_variants, min(3, len(all_variants)))
    num = len(to_choose_from)
    if num < 3:
        to_choose_from += random.sample(others, 3 - num)
    print("Есть три варианта строки:")
    print()
    print(f"1 {to_choose_from[0]}")
    print(f"2 {to_choose_from[1]}")
    print(f"3 {to_choose_from[2]}")
    i = int(input("Введите номер строки, которую хотите добавить в трехстишие: "))
    return to_choose_from[i - 1]

def filtered(pm, tokens):
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    res = []
    for token in tokens:
        t = token.text
        if t[0] in alphabet:
            res.append(pm.parse(t)[0].normal_form)
    return res

def form_sample(filename):
    d = dict()
    idx = 0
    pm = MorphAnalyzer()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            d[idx] = line, filtered(pm, list(tokenize(line.lower())))
            idx += 1
    return d

def print_haiku(text_list):
    print("\nТакое хайку получилось:\n")
    print("***\n")
    idx = 0
    while idx < len(text_list):
        print(text_list[idx], text_list[idx + 1], text_list[idx + 2], sep='')
        idx += 3
    print("***\n")

def main():
    print("Программа для генерации хайку. Загрузка...")
    sample_dict = form_sample('haiku.txt')
    print("Готово.")
    print()
    proceed = True
    while proceed:
        success = True
        num_of_tercets = int(input("Сколько трехстиший будет в вашем хайку? Введите число: "))
        haiku = []
        for i in range(num_of_tercets):
            words = input(f"Трехстишие {i + 1}. Введите 3 слова через пробел: ").lower().split()
            if len(words) != 3:
                print("Некорректный ввод!")
                proceed = False
                success = False
                break
            for idx in range(3):
                word = words[idx]
                line = generate_line(word, sample_dict)
                haiku.append(line)
        if success:
            print_haiku(haiku)
            reply = input("Продолжить? (да/нет) ")
            if reply == 'нет':
                break
    print("Программа завершена.")

if __name__ == '__main__':
    main()