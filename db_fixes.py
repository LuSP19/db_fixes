import random

from datacenter.models import (
    Schoolkid,
    Lesson,
    Mark,
    Chastisement,
    Commendation
)


def get_commendation_variants():
    with open('commendations.txt', 'r', encoding='utf-8') as file:
        commendation_variants = file.read().splitlines()
    return commendation_variants


def get_schoolkid(name):
    return Schoolkid.objects.get(full_name__contains=name)


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject):
    commendation_variants = get_commendation_variants()
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject,
    ).order_by('-date').first()
    if lesson:
        Commendation.objects.create(
            text=random.choice(commendation_variants),
            created=lesson.date,
            schoolkid=schoolkid,
            subject=lesson.subject,
            teacher=lesson.teacher,
        )
    else:
        raise Lesson.DoesNotExist()


def fix_all(name, subject=None):
    try:
        schoolkid = get_schoolkid(name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject)
    except (Schoolkid.DoesNotExist, Schoolkid.MultipleObjectsReturned):
        print('Введите корректные фамилию и имя')
    except FileNotFoundError:
        print('Файл commendations.txt не найден')
    except Lesson.DoesNotExist:
        print('Введите корректное название предмета')
