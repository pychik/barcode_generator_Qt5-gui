from os import path, getcwd
folder = path.abspath(getcwd())


class Settings:
    GENERATED = f"{folder}/generated/"
    INNER_TEXT = "inner_text_file"
    INNER_FILE = f"{folder}/inner_report.txt"
    BC_OPTIONS = dict(module_width=0.3, module_height=10, quiet_zone=2, text_distance=3,
                      font_size=8, center_text=True)
    STATUS_INIT = "Zenner software"
    STATUS_GENERATING = "barcode_generating started"
