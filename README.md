# 🍽️ Tips Dashboard — Streamlit + Plotly

Dashboard didáctico construido con **Streamlit** y **Plotly** sobre el dataset clásico `tips` (propinas en un restaurante). Es una plantilla para aprender a convertir gráficos de un notebook en una app interactiva y publicarla en la web.

**App en vivo:** https://tips-dashboard-danilo.streamlit.app

## Qué incluye

- Filtros globales en el panel lateral (día, momento, tamaño del grupo)
- 4 tarjetas de KPIs con comparación contra el promedio global
- 5 gráficos interactivos: torta, barras por paneles, histograma, boxplot y dispersión con línea de tendencia
- Tabla desplegable con los datos filtrados

## Estructura del repositorio

```
tips-dashboard/
├── tips_app.py                    # La app de Streamlit
├── requirements.txt               # Librerías que instala Streamlit Cloud
├── tips_dashboard_tutorial.ipynb  # Tutorial paso a paso (notebook)
├── GUIA_ESTUDIANTES.pdf           # Guía para replicar y publicar la app
├── .streamlit/
│   └── config.toml                # Tema visual de la app
├── .gitignore
└── README.md
```

## 1. Ejecutar en tu computadora

```bash
pip install -r requirements.txt
streamlit run tips_app.py
```

Se abre en `http://localhost:8501`.

## 2. Subir a GitHub

**Desde la web:** crea un repositorio nuevo en [github.com](https://github.com) (público), elige **uploading an existing file**, arrastra todos los archivos de esta carpeta (o usa **Add file → Upload files**) y confirma con **Commit changes**.

> La carpeta `.streamlit` y el archivo `.gitignore` empiezan con punto y en Mac están ocultos en Finder: muéstralos con `Cmd + Shift + .` antes de arrastrar.

**Con git:**

```bash
git init
git add .
git commit -m "Dashboard de propinas con Streamlit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/tips-dashboard.git
git push -u origin main
```

## 3. Publicar en Streamlit Community Cloud

1. Entra a [share.streamlit.io](https://share.streamlit.io), haz clic en **Continue to sign-in** y luego en **Continue with GitHub**. Autoriza el acceso a tus repositorios.
2. En tu espacio de trabajo haz clic en **Create app** (arriba a la derecha) y, en **Deploy a public app from GitHub**, elige **Deploy now**.
3. Completa el formulario:
   - **Repository:** `TU_USUARIO/tips-dashboard`
   - **Branch:** `main`
   - **Main file path:** `tips_app.py`
   - **App URL (opcional):** un nombre a tu gusto
4. Confirma con **Deploy** y espera unos minutos.

Cada cambio que subas a GitHub actualiza la app publicada automáticamente.

## Problemas frecuentes

| Síntoma | Causa habitual |
|---|---|
| `ModuleNotFoundError` en la app publicada | Falta la librería en `requirements.txt` |
| "Main module does not exist" | El *Main file path* no coincide con `tips_app.py` |
| La app "se durmió" | Las apps sin visitas se suspenden; se reactivan con el botón que aparece al abrirlas |

## Ejercicios

Al final de `tips_app.py` y del notebook hay ejercicios para extender la app: un filtro nuevo, un KPI adicional, cambiar un tipo de gráfico y conectar tu propio CSV.
