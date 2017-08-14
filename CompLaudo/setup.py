from cx_Freeze import setup, Executable

base = "Win32GUI"


executables = [Executable("compLaudo.py", base=base)]

packages = ["CompLaudo"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "compLaudo",
    options = options,
    version = "0.0.3c3",
    description = 'executa o processamento do relatório de um Laudo',
    executables = executables
)