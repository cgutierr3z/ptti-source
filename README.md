# ptti-source
## PROYECTO PSYCHOLOGY TEST TI (PTTI)
Codigo fuente del proyecto para Laboratorio de Software del programa Ingenieria de Sistemas y Computacion de la Universidad Tecnologica de Pereira, Colombia. Segundo semestre de 2016.

###utp

## Projecto en ejecucion
 -. [http://cgutierr3z.pythonanywhere.com](http://cgutierr3z.pythonanywhere.com)

## Instalacion
 1. `git clone https://github.com/z3774/ptti-source`
 2. `cd ptti-source`
 3. `virtualenv env`
 4. `source env/bin/activate`
 5. `pip install -r requeriments.txt`
 6. `cp ptti_source/settings-template.py ptti_source/settings.py`
 7. `nano ptti_source/settings.py` Descomentar lineas 149 a 156, poner configuracion de servidor de email.
 7. `python manage.py migrate`
 8. `python init.py`
 9. `python manage.py createsuperuser`
 10. `python manage.py runserver`
 11. [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

# Licence
This software is published under the [GNU GENERAL PUBLIC LICENSE Version 3](LICENSE)
