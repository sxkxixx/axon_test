from typing import Any

MOCK_SHIFT_TASK = dict(
    СтатусЗакрытия=False,
    ПредставлениеЗаданияНаСмену='Задание на смену 2345',
    Линия='Т2',
    Смена='1',
    Бригада='Бригада №4',
    НомерПартии='22222',
    ДатаПартии='2024-01-30',
    Номенклатура='Какая то номенклатура',
    КодЕКН='456678',
    ИдентификаторРЦ='A',
    ДатаВремяНачалаСмены='2024-01-30T20:00:00',
    ДатаВремяОкончанияСмены='2024-01-31T08:00:00',
)

UPDATED_MOCK_TASK = dict(
    is_closed=False,
    view_shift_task='Задание на смену 11',
    line='Т5',
    working_shift='7',
    brigade='Бригада №4',
    batch_number='22222',
    batch_date='2024-01-31',
    nomenclature='Изменённая номеклатура',
    csn_code='456678',
    distribution_center_id='A',
    shift_start_date='2024-01-15T20:00:00',
    shift_end_date='2024-01-16T08:00:00',
)

MOCK_SHIFT_TASKS: list[dict[str, Any]] = [
    dict(
        СтатусЗакрытия=False,
        ПредставлениеЗаданияНаСмену='Задание на смену 2345',
        Линия='Т2',
        Смена='1',
        Бригада='Бригада №4',
        НомерПартии='22222',
        ДатаПартии='2024-01-30',
        Номенклатура='Какая то номенклатура',
        КодЕКН='456678',
        ИдентификаторРЦ='A',
        ДатаВремяНачалаСмены='2024-01-30T20:00:00',
        ДатаВремяОкончанияСмены='2024-01-31T08:00:00',
    ),
    dict(
        СтатусЗакрытия=False,
        ПредставлениеЗаданияНаСмену='Задание на смену 3252',
        Линия='Т3',
        Смена='34',
        Бригада='Бригада №23',
        НомерПартии='3333',
        ДатаПартии='2024-01-31',
        Номенклатура='Какая то номенклатура 1',
        КодЕКН='456632',
        ИдентификаторРЦ='B',
        ДатаВремяНачалаСмены='2024-01-31T20:00:00',
        ДатаВремяОкончанияСмены='2024-02-01T08:00:00'
    )
]
