# Программа по взламыванию электронного дневника

## Возможности программы:
- исправление плохих оценок на отлично
- удаление всех замечаний школьника
- создание похвалы школьнику от учителя по выбранному предмету

## Запуск скрипта
1. положите файл **scripts.py** рядом с **manage.py**
2. запустите Django shell через командную строку
```
python manage.py shell
```

3. импортируйте функции
```
from scripts import fix_marks, remove_chastisements, create_commendation
```
4. запустите подходящую функцию

>исправление плохих оценок школьника
>```
>fix_marks("фамилия имя")
>```

>удаление всех замечаний школьника
>```
>remove_chastisements("фамилия имя")
>```

>создание похвалы школьнику от учителя по последнему уроку
> ```
> rcreate_commendation("фамилия имя", "предмет")
> ```


В случае если:
- данные школьника будут введены неверно
- будет найдено несколько школьников\
программа выведет уведомление. 