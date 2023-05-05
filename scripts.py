import random
import re

import django
from datacenter.models import Schoolkid, Lesson, Commendation, Subject
from django.shortcuts import get_object_or_404


class SubjectDoesNotExist(Exception):
    pass


class SchoolkidEmptyString(Exception):
    pass

def get_schoolkid(name):
    def check_name(name):
        if not name:
            raise SchoolkidEmptyString('Указана пустая строка. Необходимо указать имя ученика.')
    try:
        check_name(name)
    except SchoolkidEmptyString as error:
        print(error)
        return False
    try:
        schoolkid = get_object_or_404(Schoolkid.objects.all(), full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned as error:
        number_of_schoolkids = re.findall(r"\d+", error.args[0])[0]
        print(f'Найдено {number_of_schoolkids} ученика(ов) с таким именем. Уточните запрос.')
        return False
    except django.http.response.Http404:
        print(f'Ученик с именем {name} не найден. Уточните запрос.')
        return False
    else:
        return schoolkid


def check_subject(subject, schoolkid):
    subject = subject.title()
    def isexist(subject, schoolkid):
        subjects = Subject.objects.filter(year_of_study=schoolkid.year_of_study)
        subjects = [subject.title for subject in subjects]
        subjects_message = '\n'.join(subjects)
        if subject not in subjects:
            raise SubjectDoesNotExist(f'Предмет {subject} не найден в списке изучаемых предметов указанного ученика. Уточните запрос.\n'
                                      f'Необходимо указать предмет из списка:\n{subjects_message}')
    try:
        isexist(subject, schoolkid)
    except SubjectDoesNotExist as error:
        print(error)
        return
    else:
        return subject

def fix_marks(name):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return
    marks = schoolkid.mark_set.filter(points__in=[2, 3])
    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(name):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return
    chastisements = schoolkid.chastisement_set.all()
    for chastisement in chastisements:
        chastisement.delete()


def create_commendation(name, subject):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return
    subject = check_subject(subject, schoolkid)

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
