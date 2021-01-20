class Patology:
    def __init__(self, patology_index):
        self.vmg = patology_index in [1, 2, 3, 4, 5, 6, 9]
        self.operated = patology_index in [2]
        self.sak = patology_index in [4, 7, 8, 9]
        self.vzk = patology_index in [0, 3, 4, 5, 8]
        self.sd = patology_index in [10, 13]
        self.ed = patology_index in [13]
        self.ish= patology_index in [5, 6, 11]
        self.tumor = patology_index in [12]
        self.ish_hard=0
        self.back_position=0

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



class Case():
    def __init__(self, patology_index=0,                    # [int]
                       neurological_deficit=1,              # [1, 2, 3, 4]
                       conscious_level=15,                  # [15, 14, 12, 9, 7, 5, 3]
                       time_passed=0,                       # [int]
                       hematoma_volume=0,                   # [int]
                       is_injury=None,                      # [True/False/None]
                       has_stroke_symptoms=True,            # [True/False]
                       chronic=None,                        # [[*]/None]
                       temporary_contraindications=None):   # [[*]/None]
        self.patology_index=patology_index
        self.neurological_deficit=neurological_deficit
        self.conscious_level=conscious_level
        self.time_passed = time_passed
        self.hematoma_volume=hematoma_volume
        self.is_injury=is_injury
        self.has_stroke_symptoms=has_stroke_symptoms
        self.chronic=chronic
        self.temporary_contraindications=temporary_contraindications

        self.recs=set()
        self.recs_if_agree=set()
        self.operation='Операция не показана. '

        self.patology=Patology(self.patology_index)

        if self.patology.sak:
            self.recs.add("КТ-ангиография интракраниальных сосудов с целью поиска/исключения источника кровоизлияния.")
            self.recs.add("Повторная консультация нейрохирурга.")
            self.recs.add("КТ головного мозга в динамике через 3 суток планово для исключения формирования арезорбтивной или окклюзионной гидроцефалии")
        if self.patology.vzk:
            self.recs.add("КТ головного мозга в динамике через 3 суток планово для исключения формирования арезорбтивной или окклюзионной гидроцефалии")
        if self.patology.vmg:
            if self.patology.operated:
                if self.chronic==[] and self.temporary_contraindications==[]:
                    self.operation = "Вероятность необходимости оперативного лечения высокая – решение вопроса об операции. При согласии на хирургическое лечение"
                elif (self.chronic == None or self.temporary_contraindications == None) and self.conscious_level > 8:
                    self.operation = "Вероятность необходимости оперативного лечения высокая. " \
                             "Необходимо выяснить информацию о противопоказаниях и хронических болезнях. В случае их отсутствия - решение вопроса об операции"
                    self.recs.add("При отказе от оперативного лечения – динамическое наблюдение, повторная консультация при стабилизации, положительной динамике соматического, неврологического статуса.")
                else:
                    self.operation = "Вероятность необходимости оперативного лечения высокая – решение вопроса об операции. Однако имеются противопоказания к оперативному лечению. Целесообразен выбор индивидуальной тактики по пациенту."
                    self.recs.add("При отказе от оперативного лечения – динамическое наблюдение, повторная консультация при стабилизации, положительной динамике соматического, неврологического статуса.")
                self.recs_if_agree.add("КТ-ангиография интракраниальных сосудов с целью поиска/исключения источника кровоизлияния.")
                self.recs_if_agree.add("Повторная консультация и решение вопроса о переводе пациента в профильное ЛПУ.")

            else:
                self.operation = "Вероятность целесообразности оперативного лечения низкая"
                self.recs.add("Консервативная терапия.")
                self.recs.add("КТ-ангиография интракраниальных сосудов с целью поиска/исключения источника кровоизлияния.")
                self.recs.add("Повторная консультация нейрохирурга при верификации источника кровоизлияния")
        if self.patology.ish:
            self.recs.add("КТ-ангиография экстракраниальных и интракраниальных сосудов с целью выяснения уровня тромбоза и оценки коллатералей.")
            self.recs.add("КТ-перфузия с целью оценки зоны олигемии/некроза/пенумбры")
            self.recs.add("Повторная консультация нейрохирурга. Решение вопроса о выполнении тромбинтимэктомии, ЭИКМА, ТЭ, КЭЭ, ТЛТ.")
            if self.time_passed==0:
                self.operation = "Вероятность выполнения тромбоэкстракциии зависит от времени с момента инсульта. "
                self.recs.add("Целесообразность тромболизиса и тромбэкстракции зависит от времени с момента инсульта. ")
            elif self.time_passed<3.5:
                self.operation = "В данный момент операция не показана. "
                self.recs.add("Вероятность выполнения тромболизиса и тромбэкстракции высокая")
            elif 3.5<=self.time_passed<=12:
                self.operation = "Рекомендуется процедура тромбоэкстракции. "
                self.recs.add("Вероятность выполнения тромболизиса низкая, есть вероятность решения вопроса в пользу тромбэкстракции")
            else:
                self.operation = "Вероятность выполнения тромбоэкстракции низкая. "
                self.recs.add("Вероятность выполнения тромболизиса и тромбэкстракции низкая")
            if self.patology.ish_hard and self.conscious_level<13:
                self.operation = "Высока вероятность необходимости выполнения декомпрессивной трепанации черепа. Решение вопроса об оперативном лечении."
        if self.patology.tumor:
            self.recs.add("МРТ головного мозга с в/в контрастным усилением для исключения объемного процесса")
            self.recs.add("Повторная консультация для решения вопроса об оперативном лечении.")
            self.recs.add("Консультация онколога.")
            self.recs.add("Онкопоиск: сбор онкоанамнеза, УЗИ брюшной полости КТ легких, УЗИ почек.")
            if self.conscious_level==9:
                self.operation = "Решение вопроса о выполнении оперативного лечения в неотложном порядке до выполнения МРТ головного мозга."

        self.recs.add("Динамическое наблюдение неврологического статуса")
        self.recs.add("При отрицательной динамике – повторное КТ головного мозга, повторная консультация нейрохирурга.")


case=Case(patology_index=2)
op, rec, rec_if = case.operation, case.recs, case.recs_if_agree
print(color.GREEN + "Показания об операции: " + color.END)
print(op)
print(color.GREEN + "\nРекомендации: " + color.END)
for i in rec:
    print(i)
if rec_if:
    print(color.GREEN + "\nПри согласии на хирургическое лечение:" + color.END)
    for i in rec_if:
        print(i)



