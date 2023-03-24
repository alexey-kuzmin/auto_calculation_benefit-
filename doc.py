from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.oxml.shared import qn


def create_doc():
    doc = Document()    # создание документа
    return doc


def set_p_setting(doc):
    style = doc.styles['Normal']                                            # задаем стиль текста по умолчанию
    style.font.name = 'Times New Roman'                                     # название шрифта
    style.font.size = Pt(14)                                                # размер шрифта
    #style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY_LOW  # по ширине
    style.paragraph_format.alignment = 3                                    # по ширине
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE       # межстрочный
    style.paragraph_format.first_line_indent = Mm(10)                       # отступ первой строки
    style.paragraph_format.space_before = Mm(0)                             # отступ сверху в мм
    style.paragraph_format.space_after = Mm(0)                              # отступ снизу в мм

    styles_element = doc.styles.element
    rpr_default = styles_element.xpath('./w:docDefaults/w:rPrDefault/w:rPr')[0]
    lang_default = rpr_default.xpath('w:lang')[0]
    lang_default.set(qn('w:val'), 'ru-RU')


def main():
    doc = create_doc()

    set_p_setting(doc)



    a = 'dddddddddd ddddddddd aaaaaaaaaaa sssssssssss dddddddddddddddddddddd ssssssssssssssss aaaaaaaaaaaaaaaaaa ffffffffffffffffffffff dddddddddddddddddddddd ssssssssssssssssssss ggggggggggggggggggggggg'
    doc.add_paragraph(a, style='Normal')

    doc.save('testttt.docx')


if __name__ == '__main__':
    main()