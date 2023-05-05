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


def fix_marks(name):
    schoolkid = get_schoolkid(name)
    marks = schoolkid.mark_set.filter(points__in=[2, 3])
    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(name):
    schoolkid = get_schoolkid(name)
    chastisements = schoolkid.chastisement_set.all()
    for chastisement in chastisements:
        chastisement.delete()
