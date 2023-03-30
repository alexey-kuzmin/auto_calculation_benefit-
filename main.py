import datetime as dt
from calendar import monthrange
from decimal import Decimal
from doc import create_doc, set_p_setting, Mm

MONTH_rp = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
            'ноября', 'декабря']
MONTH_pp = ['январе', 'феврале', 'марте', 'апреле', 'мае', 'июне', 'июле', 'августе', 'сентябре', 'октябре',
            'ноябре', 'декабре']


def string_date_to_dt(dates: list) -> list:
    result = []
    for date in dates:
        shar = '-' if date.find('—') == -1 else '—'
        start, finish = date.split(shar)
        start, finish = list(map(int, start.split('.')[::-1])), list(map(int, finish.split('.')[::-1]))
        result.append((dt.date(*start), dt.date(*finish)))
    return result


def formatted_mass_duration(duration: list) -> list:
    """Форматированный вывод расчета"""
    return [f'({dur[4]} / {dur[1]} * {dur[0]})' for dur in duration]


def formatted_unemployment_benefits(duration: list):
    """Финансовое округление"""
    return sum([Decimal(str(dur[4] / dur[1] * dur[0])).quantize(Decimal("1.00")) for dur in duration])


def create_first_paragraph(doc, FIO, delta_dates):
    start, finish = delta_dates[0][0], delta_dates[-1][1]
    start = f'{start.day} {MONTH_rp[start.month - 1]} {start.year}'
    finish = f'{finish.day} {MONTH_rp[finish.month - 1]} {finish.year}'

    text = f'Расчет суммы пособия по безработице, перечисленного {FIO} за период ' \
           f'с {start} года по {finish} года'

    p = doc.add_paragraph()
    p.alignment = 1
    runner = p.add_run(text)
    runner.bold = True
    p_frm = p.paragraph_format
    p_frm.first_line_indent = Mm(0)

    doc.add_paragraph()


def create_mid_paragraph(doc, FIO, benefits, delta_dates):
    all_amount_ben, all_unemployment_benefits = [], []
    for i, duration in enumerate(delta_dates, 1):
        start_duration, finish_duration = duration[0], duration[1]
        days_on_month = monthrange(start_duration.year, start_duration.month)[1]
        mass_duration = []

        if start_duration.month == finish_duration.month:
            mass_duration.append(((finish_duration - start_duration).days + 1, days_on_month,
                                  start_duration.month, start_duration.year, benefits[i - 1]))
        else:
            now_month = start_duration.month
            now_year = start_duration.year
            while (now_month <= finish_duration.month and now_year == finish_duration.year) or \
                  (now_year < finish_duration.year):
                days_on_month = monthrange(now_year, now_month)[1]
                if now_month == start_duration.month:
                    mass_duration.append((days_on_month - start_duration.day + 1, days_on_month, now_month, now_year, benefits[i - 1]))
                elif now_month == finish_duration.month:
                    mass_duration.append((finish_duration.day, days_on_month, now_month, now_year, benefits[i - 1]))
                else:
                    mass_duration.append((days_on_month, days_on_month, now_month, now_year, benefits[i - 1]))

                now_month = now_month + 1
                if now_month == 13:
                    now_year += 1
                    now_month = 1

        unemployment_benefits = formatted_unemployment_benefits(mass_duration)
        mass_duration_with_format = formatted_mass_duration(mass_duration)

        start_date = f'{start_duration.day} {MONTH_rp[start_duration.month - 1]} {start_duration.year} года'
        finish_date = f'{finish_duration.day} {MONTH_rp[finish_duration.month - 1]} {finish_duration.year} года'

        doc.add_paragraph(f'{i}. За период с {start_date} по {finish_date} {FIO} начислено и выплачено пособие по'
                          f' безработице в размере {unemployment_benefits} рубля, из расчета:')
        doc.add_paragraph()
        doc.add_paragraph(' + '.join(mass_duration_with_format) + f' = {unemployment_benefits} рубля, где:')
        doc.add_paragraph()

        for j, val in enumerate(mass_duration):
            doc.add_paragraph(f'{val[4]} – размер назначенного пособия по безработице в месяц;')
            doc.add_paragraph(f'{val[1]} – количество дней в {MONTH_pp[val[2] - 1]} {val[3]} года;')

            if len(mass_duration) == 1:
                start, finish = start_date, finish_date
            elif j == 0:
                start, finish = start_date, f'{val[1]} {MONTH_rp[val[2] - 1]} {val[3]} года;'
            elif j == len(mass_duration) - 1:
                start, finish = f'1 {MONTH_rp[val[2] - 1]} {val[3]} года', f'{finish_date};'
            else:
                start, finish = f'1 {MONTH_rp[val[2] - 1]} {val[3]} года ', f'31 {MONTH_pp[val[2] - 1]} {val[3]};' # комп границ
            doc.add_paragraph(f'{val[0]} – количество календарных дней в период с {start} по {finish};')

        amount_ben = f'{unemployment_benefits} – размер пособия по безработице ' \
                     f'за период с {start_date} по {finish_date}.'
        doc.add_paragraph(amount_ben)
        doc.add_paragraph()

        all_amount_ben.append(amount_ben)
        all_unemployment_benefits.append(unemployment_benefits)

    create_finish_paragraph(doc, len(all_amount_ben), all_unemployment_benefits, all_amount_ben, delta_dates, FIO)


def create_finish_paragraph(doc, i, sum_ben, text_ben, delta_dates, fio):
    if len(delta_dates) == 1:
        start, finish = delta_dates[0][0], delta_dates[0][1]
    else:
        start, finish = delta_dates[0][0], delta_dates[-1][1]

    start = f'{start.day} {MONTH_rp[start.month - 1]} {start.year}'
    finish = f'{finish.day} {MONTH_rp[finish.month - 1]} {finish.year}'

    for_text = list(map(str, sum_ben))
    if len(sum_ben) == 1:
        p = doc.add_paragraph()
        p.add_run(
            f'{i + 1}. Таким образом, за период с {start} года по {finish} года {fio} начислено и выплачено пособие '
            f'по безработице в размере {sum(sum_ben)} рубля')
    else:
        p = doc.add_paragraph()
        p.add_run(f'{i + 1}. Таким образом, за период с {start} года по {finish} года {fio} начислено и '
                          f'выплачено пособие по безработице в размере {sum(sum_ben)} рубля из расчета:')
        p_frm = p.paragraph_format
        p_frm.first_line_indent = Mm(10)
        doc.add_paragraph()
        doc.add_paragraph(f'{" + ".join(for_text)} = {sum(sum_ben)} рубля, где:')
        doc.add_paragraph()
        for i, t in enumerate(text_ben):
            doc.add_paragraph(t)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('Представитель по доверенности                                            И.О. Фамилия')
    p_frm = p.paragraph_format
    p_frm.first_line_indent = Mm(0)
    doc.add_paragraph()


def create_all_document(doc, name, fio, benefits, delta_dates):
    create_first_paragraph(doc, fio, delta_dates)
    set_p_setting(doc)
    create_mid_paragraph(doc, fio, benefits, delta_dates)

    doc.save(name + '.docx')


def main():
    doc = create_doc()
    date = ['13.10.2020—12.01.2021']
    create_all_document(doc, 'тест', 'Иванову И.И.', [1800], string_date_to_dt(date))


if __name__ == "__main__":
    main()
