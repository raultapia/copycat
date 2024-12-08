<h1 align="center">COPYCAT</h1>
<p align="center">
<b>C</b>omparación <b>O</b>rganizada de <b>P</b>atrones <b>Y</b> <b>C</b>ódigo mediante <b>A</b>nálisis de <b>T</b>exto
</p>

## Descripción

COPYCAT es una herramienta diseñada para encontrar archivos similares en una carpeta y sus subcarpetas mediante el análisis de texto. Utiliza la similitud coseno y la vectorización TF-IDF para comparar el contenido de los archivos y generar un informe en PDF con los resultados.

## Dependencias

Dependencias necesarias:

- `datetime`: Incluida en la biblioteca estándar de Python.
- `fpdf`: Para instalar, use `pip install fpdf`.
- `matplotlib`: Para instalar, use `pip install matplotlib`.
- `numpy`: Para instalar, use `pip install numpy`.
- `os`: Incluida en la biblioteca estándar de Python.
- `scikit-learn`: Para instalar, use `pip install scikit-learn`.
- `tkinter`: Incluida en la biblioteca estándar de Python.

## Instalación

Para instalar las dependencias necesarias, puede usar el siguiente comando:

```sh
pip install fpdf matplotlib numpy scikit-learn
```

## Uso

1. Ejecute el script `copycat.py`:

   ```sh
   python3 copycat.py
   ```

2. Se abrirá una ventana para seleccionar la carpeta que desea analizar. Seleccione la carpeta y haga clic en "Ok".

3. El script analizará los archivos en la carpeta seleccionada y generará un informe en PDF con los resultados. El informe incluirá:

   - Una tabla con la relación entre IDs y nombres de archivos (se utilizan IDs para poder compartir resultados atendiendo a principios de privacidad y protección de datos).
   - Una tabla con los archivos similares encontrados y su nivel de similaridad.
   - Una matriz de similitud entre archivos.
   - Una gráfica de barras de los archivos similares.

4. El PDF se guardará en el directorio actual con un nombre basado en la fecha y hora actual: `report_YYYYMMDDhhmmss.pdf`.

## Contribuciones

Las contribuciones son bienvenidas. Si desea contribuir, por favor haga un fork del repositorio y envíe un pull request con sus cambios.

## Licencia

COPYCAT está licenciado bajo la Licencia MIT. Consulte el archivo `LICENSE` para obtener más detalles.

## Contacto

Si tiene alguna pregunta o sugerencia, no dude en ponerse en contacto con nosotros a través del correo electrónico `raultapia@us.es`.
