param(
    [string]$py_path = "C:\Users\91997\AppData\Local\Programs\Python\Python311",
    [string]$env_path = 'D:\Projects\rtsg\rstg_env'
)

$env:Path = $py_path + ";" + $env:Path

& $env_path\Scripts\Activate.ps1

python 'D:\Projects\rtsg\transcripter.py' -i mic 
python 'D:\Projects\rtsg\content_generator.py'
python 'D:\Projects\rtsg\JSON_generator.py'
python 'D:\Projects\rtsg\PPT_generator.py'