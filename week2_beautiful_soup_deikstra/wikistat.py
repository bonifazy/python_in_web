# Для работы программы, распакуйте архив week2_Beautiful_soup.zip


from bs4 import BeautifulSoup
import re
import os


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, path):

    file = open(os.path.join(path, start)).read()
    link_re = re.findall(r"\"\/wiki\/([\w\(\)]{0,50})\"", file)  # Искать ссылки
    files_in_path = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}
    files = list()
    for _file in link_re:  # бегаем по ссылкам
        if _file in files_in_path:  # если файл из папки, совпадает с найденной ссылкой
            if _file not in files and _file != start:
                files.append(_file)

    return files

    # Проставить всем ключам в files правильного родителя в значение, начиная от start


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):

    layer = 0
    level = {start: layer}  # уровень вложенности ссылки
    parents = {start: 'Start'}  # родители для исходных ссылок
    visited = [start]  # ступенчатый список следующих шагов в след цикле
    is_done = True  # истина, если еще не нашли конец

    # поиск кратчайшего пути в графе graph от A к F
    while is_done:
        now = visited[layer]  # now = a
        files = build_tree(now, path)
        for maybe in files:  # бегаем по всем соседям maybe = b, c, e
            if maybe not in level.keys():  # новая точка, которая встретилась впервые
                parents[maybe] = now
                visited.append(maybe)  # добавляем в список посещенных
                level[maybe] = level[now] + 1  # записываем важность точки
                if maybe == end:  # финиш найден
                    is_done = False  # конец пути найден!
        layer += 1  # переходим на след уровень в глубину только тогда, когда посмотрели весь свой уровень

    # поиск дерева родителей
    bridge = list()
    is_done = True
    next = end
    while is_done:
        bridge.insert(0, next)
        next = parents[next]
        if next == start:
            is_done = False
    bridge.insert(0, start)

    return bridge


def parse(start, end, path):

    bridge = build_bridge(start, end, path)
    out = {}

    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        imgs = 0
        for img in body('img'):
            try:
                if int(img['width']) >= 200: imgs += 1
            except:
                pass

        headers = 0
        for header in body(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if re.search(r">([ETC]{1}).*?<", str(header)):
                headers += 1

        linkslen = 0
        counter = 1
        for link in body('a'):
            if link.find_next_sibling():
                if link.find_next_sibling().name == 'a':
                    counter += 1
                else:
                    if counter > linkslen: linkslen = counter
                    counter = 1
            else:
                if counter > linkslen: linkslen = counter
                counter = 1

        lists = 0
        for _list in body(['ol', 'ul']):
            list_parents = [i.name for i in _list.parents]
            if 'ol' not in list_parents and 'ul' not in list_parents:
                lists += 1

        out[file] = [imgs, headers, linkslen, lists]

    return out


if __name__ == "__main__":

    start = 'Python_(programming_language)'
    end = 'Stone_Age'
    path = './wiki/'

    result = parse(start, end, path)

    print(result)
