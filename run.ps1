param(
    [string]$py_path = "C:\Users\91997\AppData\Local\Programs\Python\Python311",
    [string]$env_path = 'D:\Projects\rtsg\rstg_env',
    [int]$slide = 1,
    [string]$topic = 'Heap'
)

$env:Path = $py_path + ";" + $env:Path

& $env_path\Scripts\Activate.ps1

python 'D:\Projects\rtsg\transcripter.py' -i mic -s $slide -tp $topic
python 'D:\Projects\rtsg\content_generator.py' -W ignore
python 'D:\Projects\rtsg\JSON_generator.py'
python 'D:\Projects\rtsg\PPT_generator.py'