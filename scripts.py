import random

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Subject


def fix_marks(schoolkid):
    try:
        choice_schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid)
        count_all_bad_marks = Mark.objects.filter(schoolkid=choice_schoolkid, points__lte=3).count()
        if count_all_bad_marks == 0:
            print("У школьника", choice_schoolkid.full_name, "нет плохих оценок")
        else:
            all_bad_marks = Mark.objects.filter(schoolkid=choice_schoolkid, points__lte=3)
            for mark in all_bad_marks:
                mark.points = 5
                mark.save()
            print("У школьника", choice_schoolkid.full_name, "произведена замена", count_all_bad_marks,
                  "плохих оценок на отличные оценки")
    except MultipleObjectsReturned:
        print("Найдено более одного школьника c данными", schoolkid, ". Уточните ФИО школьника")
    except ObjectDoesNotExist:
        print("Школьника c данными", schoolkid, " не существует")


def remove_chastisements(schoolkid):
    try:
        choice_schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid)
        count_chastisement = Chastisement.objects.filter(schoolkid=choice_schoolkid).count()
        if count_chastisement == 0:
            print("У школьника", choice_schoolkid.full_name, "нет замечаний")
        else:
            chastisement = Chastisement.objects.filter(schoolkid=choice_schoolkid)
            chastisement.delete()
            print("У школьника", choice_schoolkid.full_name, "удалено", count_chastisement, "замечаний")

    except MultipleObjectsReturned:
        print("Найдено более одного школьника c данными", schoolkid, ". Уточните ФИО школьника")
    except ObjectDoesNotExist:
        print("Школьника c данными", schoolkid, " не существует")


def create_commendation(name, subject):
    try:
        choice_schoolkid = Schoolkid.objects.get(full_name__contains=name)
        choice_subject = Subject.objects.filter(title__contains=subject).first()
        last_lesson = Lesson.objects.filter(
            year_of_study=choice_schoolkid.year_of_study,
            group_letter=choice_schoolkid.group_letter,
            subject__title__contains=subject
            ).order_by('-date', '-timeslot'
            ).first()

        praise = [
            'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
            'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
            'Именно этого я давно ждал от тебя!', 'Сказано здорово – просто и ясно!',
            'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
            'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!',
            'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!',
            'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!',
            'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
            'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
            'Теперь у тебя точно все получится!']

        last_commendation = Commendation.objects.filter(
            subject=choice_subject,
            created=last_lesson.date,
            schoolkid=choice_schoolkid,
            teacher=last_lesson.teacher
            ).exists()

        if last_commendation:
            print(choice_schoolkid.full_name, "уже имеет похвалу по последнему уроку", choice_subject.title,
                  "от преподавателя", last_lesson.teacher)

        else:
            new_commendation = Commendation.objects.create(
                text=random.choice(praise),
                subject=choice_subject,
                created=last_lesson.date,
                schoolkid=choice_schoolkid,
                teacher=last_lesson.teacher)
            print("Для школьника,", choice_schoolkid.full_name, "создана похвала:", new_commendation.text,
                  "по последнему уроку", choice_subject.title, new_commendation.created, "от преподавателя",
                  last_lesson.teacher, )

    except MultipleObjectsReturned:
        print("Найдено более одного школьника c данными", name, ". Уточните ФИО школьника")
    except ObjectDoesNotExist:
        print("Школьника c данными", name, " не существует")
