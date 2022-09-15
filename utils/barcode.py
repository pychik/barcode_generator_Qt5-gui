from os import listdir, remove, path, makedirs
from barcode import Code128
from barcode.writer import ImageWriter
from datetime import datetime

from config import Settings


class BarCoder:

    folder: str = Settings.GENERATED
    file: str = Settings.INNER_FILE
    options: dict = Settings.BC_OPTIONS

    def __init__(self, numbers: tuple, report_type: str = None):
        self.numbers = numbers
        self.report_type = report_type
        if not path.exists(self.folder):
            makedirs(self.folder)

    def create(self):
        writer = ImageWriter()
        try:
            for n in self.numbers:
                my_code = Code128(n, writer=writer)
                my_code.save(filename=f'{self.folder}{n}', options=self.options)

            return f"{len(self.numbers)} ШТРИХ-КОДА(ОВ) СГЕНЕРИРОВАНЫ И ПОМЕЩЕНЫ В ПАПКУ \"{self.folder}\"!<br>" \
                   f" Отчет добавлен в \"inner_report.txt\""
        except Exception as e:
            print(f"Exception error: {e}")
            return f"Exception error: {e}"

    def report(self):
        if self.numbers:
            with open(self.file, 'a') as f:
                data_obj = '\n' + '\n'.join(str(num) for num in self.numbers)
                final_str = f"{datetime.now().strftime('%Y.%m.%d %H:%M:%S')}{data_obj}"
                final_str += '\n\n'
                f.write(final_str)
