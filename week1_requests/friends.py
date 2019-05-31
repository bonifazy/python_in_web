import requests


ACCESS_TOKEN = '1bb72ff41bb72ff41bb72ff4141bd2b5a511bb71bb72ff440d9f2693b1ec32d7cb57585'


def calc_age(uid):
    user_id = uid
    search_field = "bdate"

    url = "https://api.vk.com/method/users.get?v=5.71&" \
        "access_token={}&user_ids={}".format(ACCESS_TOKEN, user_id)
    r = requests.get(url)
    user_id = r.json()["response"][0]["id"]

    url = "https://api.vk.com/method/friends.get?v=5.71&" \
          "access_token={}&user_id={}&fields={}".format(ACCESS_TOKEN, user_id, search_field)
    r = requests.get(url)
    friends = r.json()["response"]["items"]

    age_list = list()

    for user in friends:
        if search_field in user and len(user[search_field]) > 7:
            age_list.append(2019 - int(user[search_field][-4:]))
    age_dict = dict()
    for date in age_list:
        if date in age_dict:
            age_dict[date] = age_dict[date] + 1
        else:
            age_dict[date] = 1
    # на выходе получаем список пар (<возраст>, <количество друзей с таким возрастом>),
    # отсортированный по убыванию по второму ключу (количество друзей) и по возрастанию по первому ключу (возраст).
    return sorted(age_dict.items(), key=lambda x: (-x[1], x[0]))


if __name__ == '__main__':
    res = calc_age('mardim')
    print(res)

# [
# (31, 20), (33, 14), (32, 13), (27, 11), (26, 9), (29, 9), (30, 8), (24, 7), (35, 7), (38, 6), (25, 5), (28, 5),
# (19, 4), (34, 4), (39, 4), (43, 4), (23, 3), (49, 3), (21, 2), (22, 2), (37, 2), (66, 2), (15, 1), (18, 1), (36, 1),
# (40, 1), (41, 1), (45, 1), (50, 1), (52, 1), (55, 1), (58, 1), (71, 1), (99, 1)
# ]
