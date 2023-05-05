import random
import re

from datacenter.models import Schoolkid, Lesson, Commendation


def get_schoolkid(name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned as error:
        number_of_schoolkids = re.findall(r"\d+", error.args[0])[0]
        print(f'Найдено {number_of_schoolkids} ученика(ов) с таким именем. Уточните запрос.')
    except Schoolkid.DoesNotExist:
        print(f'Ученик с именем {name} не найден. Уточните запрос.')
    else:
        return schoolkid
