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


def create_commendation(name, subject):
    schoolkid = get_schoolkid(name)

    texts = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
    ]

    lesson = Lesson.objects.filter(
        group_letter=schoolkid.group_letter,
        year_of_study=schoolkid.year_of_study,
        subject__title=subject,
    ).order_by('-date').first()

    Commendation.objects.create(
        text=random.choice(texts),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )
