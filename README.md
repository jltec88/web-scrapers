# web-scrapers

Repositorio centralizado de distintos *scrapers* para extraer información de páginas web.

---

## 📖 Descripción

En este proyecto encontrarás varios scrapers especializados, cada uno en su propia rama, que te permiten:
- Extraer contenido estructurado (títulos, párrafos, etc.) de sitios web.
- Generar informes en PDF a partir del HTML raspado.
- Reutilizar código común (por ejemplo, el generador de PDF).

La rama `main` solo incluye este README con la guía general.

---

## 🌲 Estructura de ramas

- **main**  
  Contiene únicamente este `README.md`.  
- **feature/company-scraper**  
  Scraper para COMPANY: `company-scraper.py`.  
- **feature/otra-url-scraper**  
  (Próximo scraper…)  

---

## 🔧 Requisitos

- Python **3.8+**  
- Dependencias definidas en `requirements.txt`  
- Archivo de entorno `.env` con:
  ```dotenv
  LANDING_URL=<URL>
