Como Iniciar todo este entorno
Todo esto se realiza en la carpeta raiz exactamente en esta ubicación en la terminal
PS C:\Users\cornu\OneDrive\Escritorio\MangaLords>

Recordsr que:
Antes de realizar cualquiera de estas cosas debes revisar ya segurarte que tengas python instalado en tu pc

Pasos a seguir:

1) Crear entorno virtual de Python (myvenv)
    python -m venv myvenv

2) Activar este entorno virtual creado en el paso anterior
    .\myvenv\Scripts\activate

3) Instalación de dependencias
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

4) Levantar el servidor
    python manage.py runserver

-------------------------------------------------------------------

Comando extra

Si sucede algun error con el entorno virtual se puede eliminar y volver a Crear
    Remove-Item -Recurse -Force .\myvenv
    
con ese comando lo borras y vuelves a hacer todos los pasos anteriores.