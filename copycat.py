#!/usr/bin/env python3
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tkinter import Tk
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from datetime import datetime
THRESHOLD = 0.7


def read_file(file_path, encodings=['utf-8', 'latin-1']):
    """Leer el contenido de un archivo usando múltiples codificaciones."""
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    print(f"Saltando archivo: {file_path}. No se puede decodificar usando ninguna de las codificaciones proporcionadas.")
    return None


def find_similar_files(folder, threshold=THRESHOLD):
    """Encontrar archivos similares en una carpeta y sus subcarpetas."""
    file_contents = {}
    similar_files = []

    for root, _, files in os.walk(folder):
        for filename in files:
            if filename[-4:] == "exec":
                continue
            file_path = os.path.join(root, filename)
            content = read_file(file_path)
            if content is not None:
                file_contents[file_path] = content

    # Ordenar los archivos por nombre
    sorted_file_paths = sorted(file_contents.keys())
    sorted_file_contents = [file_contents[path] for path in sorted_file_paths]

    # Calcular vectores TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(sorted_file_contents)

    # Calcular la similitud coseno entre todos los pares de documentos
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Iterar sobre la matriz de similitud para encontrar archivos similares
    for i in range(len(similarity_matrix)):
        for j in range(i + 1, len(similarity_matrix)):
            if similarity_matrix[i, j] >= threshold:
                file1 = sorted_file_paths[i]
                file2 = sorted_file_paths[j]
                similarity_score = similarity_matrix[i, j]
                similar_files.append((os.path.relpath(file1, folder), os.path.relpath(file2, folder), similarity_score))

    return similar_files, similarity_matrix, sorted_file_paths


if __name__ == "__main__":
    # Crear una ventana para seleccionar la carpeta
    Tk().withdraw()  # Ocultar la ventana principal de Tkinter
    folder = askdirectory(title="Selecciona una carpeta")

    if folder:
        similar_files, similarity_matrix, file_paths = find_similar_files(folder)
        if similar_files:
            # Crear un PDF para el reporte en orientación vertical (portrait)
            pdf = FPDF(orientation='P')

            # Añadir título
            pdf.add_page()
            pdf.set_font("Arial", size=18, style='B')
            pdf.cell(0, 160, "COPYCAT - Informe", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=16)
            pdf.cell(0, 10, datetime.now().strftime("%d/%m/%Y"), ln=True, align='C')
            pdf.ln(20)

            # Añadir tabla de IDs y nombres de archivos
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, "Relación entre IDs y nombres de archivos:", ln=True, align='C')
            pdf.ln(10)
            file_id_map = {f"{i:05d}": os.path.relpath(path, folder) for i, path in enumerate(file_paths)}
            for file_id, file_name in file_id_map.items():
                pdf.cell(0, 10, f"{file_id}: {file_name}", ln=True)

            # Añadir tabla con archivos similares
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, "Archivos similares encontrados:", ln=True, align='C')
            for file1, file2, similarity_score in similar_files:
                id1 = [k for k, v in file_id_map.items() if v == file1][0]
                id2 = [k for k, v in file_id_map.items() if v == file2][0]
                pdf.cell(0, 10, f"{id1} es similar a {id2} con un nivel de similaridad de {similarity_score:.2f}", ln=True)

            # Agregar la imagen de la matriz de similitud al PDF centrada en orientación horizontal (landscape)
            plt.figure(figsize=(10, 8))
            plt.imshow(similarity_matrix, interpolation='nearest', cmap='viridis')
            plt.colorbar()
            plt.xticks(np.arange(len(file_paths)), [f"{i:05d}" for i in range(len(file_paths))], rotation=30, ha='right')
            plt.yticks(np.arange(len(file_paths)), [f"{i:05d}" for i in range(len(file_paths))])
            plt.title('Matriz de Similitud entre Archivos')
            plt.savefig("similarity_matrix.png")
            plt.close()
            pdf.add_page(orientation='L')
            pdf.image("similarity_matrix.png", x=(pdf.w - 250) / 2, y=(pdf.h - 200) / 2, w=250, h=200)

            # Agregar la imagen de la gráfica de barras al PDF centrada en orientación horizontal (landscape)
            file_pairs = [f"{id1} - {id2}" for file1, file2, _ in similar_files for id1, id2 in [(k1, k2) for k1, v1 in file_id_map.items() if v1 == file1 for k2, v2 in file_id_map.items() if v2 == file2]]
            similarity_scores = [score for _, _, score in similar_files]
            plt.figure(figsize=(12, 10))
            plt.barh(file_pairs, similarity_scores, color='skyblue')
            plt.axvline(x=THRESHOLD, color='r', linestyle='--', label=f'Umbral de similaridad. No se muestran resultados con valor menor a {THRESHOLD}.')
            plt.xlabel('Nivel de Similaridad')
            plt.ylabel('Pares de Archivos')
            plt.title('Gráfica de Barras de Archivos Similares')
            plt.legend()
            plt.tight_layout()
            plt.savefig("similarity_bar_chart.png")
            plt.close()
            pdf.add_page(orientation='L')
            pdf.image("similarity_bar_chart.png", x=(pdf.w - 250) / 2, y=(pdf.h - 200) / 2, w=250, h=200)

            # Guardar el PDF con la fecha y hora actual
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            pdf.output(f"report_{current_time}.pdf")

            print(f"Reporte generado: report_{current_time}.pdf")
        else:
            print("No se encontraron archivos similares.")
    else:
        print("No se seleccionó ninguna carpeta.")
