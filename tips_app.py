# tips_app.py
# ============================================================
#  DASHBOARD DIDÁCTICO — Dataset "tips" (propinas en un restaurante)
#  Ejecutar en local:  streamlit run tips_app.py
#  Publicar:           subir este repo a GitHub y desplegarlo en
#                      Streamlit Community Cloud (ver README.md)
#
#  Este script es una PLANTILLA para aprender Streamlit + Plotly.
#  Cada sección explica QUÉ hace y POR QUÉ, para que puedas
#  reutilizar el mismo patrón con tus propios datos.
#
#  Idea clave de Streamlit: el script se ejecuta de ARRIBA A ABAJO
#  cada vez que el usuario interactúa con un widget (un slider, un
#  selectbox, etc.). Por eso vas a ver que todo el "flujo" del
#  dashboard es simplemente código Python normal, leído de arriba
#  hacia abajo.
# ============================================================

import pandas as pd
import plotly.express as px
import streamlit as st

# ── 1. CONFIGURACIÓN DE LA PÁGINA ────────────────────────────
# st.set_page_config() debe ser la PRIMERA instrucción de Streamlit
# en el script. Define el título de la pestaña del navegador, el
# ícono y si el contenido usa todo el ancho ("wide") o queda
# centrado ("centered").
st.set_page_config(
    page_title="Tips Dashboard",
    page_icon="🍽️",
    layout="wide",
)

# ── 2. PALETA DE COLORES Y ESTILO COMPARTIDO ─────────────────
# Definir los colores como constantes evita repetir códigos hex
# y asegura que la misma categoría (ej. "Sí"/"No") tenga siempre
# el mismo color en TODOS los gráficos del dashboard.
COLOR_SI_NO = {"Sí": "#1D9E75", "No": "#D85A30"}
COLOR_SEXO  = {"Mujer": "#7F77DD", "Hombre": "#378ADD"}
COLOR_DIA   = {"Jue": "#378ADD", "Vie": "#7F77DD", "Sáb": "#BA7517", "Dom": "#D85A30"}
ORDEN_DIAS  = ["Jue", "Vie", "Sáb", "Dom"]

# Diccionario reutilizable con el estilo visual de Plotly: fondo,
# tipografía, márgenes y posición de la leyenda. Se "desempaqueta"
# con ** en cada fig.update_layout(**LAYOUT, ...).
LAYOUT = dict(
    plot_bgcolor="white", paper_bgcolor="white",
    font=dict(family="Inter,Arial,sans-serif", size=12),
    margin=dict(t=40, b=40, l=50, r=20),
    legend=dict(orientation="h", y=-0.2),
)

# ── 3. CARGAR Y PREPARAR LOS DATOS ───────────────────────────
# @st.cache_data le dice a Streamlit: "ejecuta esta función UNA
# SOLA VEZ y guarda (cachea) el resultado en memoria". Como el
# script se vuelve a ejecutar completo cada vez que se mueve un
# filtro, sin esta línea recargaríamos y transformaríamos el
# dataset una y otra vez — innecesario y lento.
@st.cache_data
def cargar_datos():
    # px.data.tips() trae el dataset clásico de propinas ya
    # incluido en Plotly: no requiere descargar ni subir archivos.
    df = px.data.tips()

    # Traducimos/renombramos valores para que el dashboard se vea
    # en español. Esto es opcional, pero ayuda a la legibilidad
    # y es un buen ejemplo de "limpieza de datos" con .map().
    df["Fumador"] = df["smoker"].map({"Yes": "Sí", "No": "No"})
    df["Sexo"]    = df["sex"].map({"Female": "Mujer", "Male": "Hombre"})
    df["Día"]     = df["day"].map({"Thur": "Jue", "Fri": "Vie", "Sat": "Sáb", "Sun": "Dom"})
    df["Momento"] = df["time"].map({"Lunch": "Almuerzo", "Dinner": "Cena"})

    # Columna calculada: porcentaje de propina sobre la cuenta.
    # Esto es pandas normal — nada especial de Streamlit aquí.
    df["% propina"] = (df["tip"] / df["total_bill"] * 100).round(1)

    return df

df = cargar_datos()

# ── 4. SIDEBAR — FILTROS GLOBALES ────────────────────────────
# Todo lo que esté dentro de "with st.sidebar:" aparece en el
# panel lateral izquierdo. Cada widget (multiselect, radio, slider)
# DEVUELVE el valor elegido por el usuario, que guardamos en una
# variable normal de Python para usarla más abajo.
with st.sidebar:
    st.title("🍽️ Tips")
    st.caption("Filtros globales — afectan todos los gráficos")

    # multiselect → el usuario puede elegir VARIAS opciones a la vez
    dias = st.multiselect(
        "Día",
        options=ORDEN_DIAS,
        default=ORDEN_DIAS,
    )

    # radio → el usuario elige UNA sola opción
    momento = st.radio(
        "Momento",
        options=["Todos", "Almuerzo", "Cena"],
    )

    # slider de rango → devuelve una tupla (mínimo, máximo)
    tam_min, tam_max = st.slider(
        "Tamaño del grupo (personas)",
        min_value=int(df["size"].min()),
        max_value=int(df["size"].max()),
        value=(int(df["size"].min()), int(df["size"].max())),
    )

    st.divider()
    st.caption(f"Dataset completo: {len(df)} cuentas")

# ── 5. APLICAR LOS FILTROS (pandas puro) ─────────────────────
# Construimos una "máscara" booleana (una serie de True/False)
# combinando condiciones con & (Y lógico). Luego usamos esa
# máscara para quedarnos solo con las filas que la cumplen.
# Esta parte es 100% pandas — no tiene nada de Streamlit.
mask = (
    df["Día"].isin(dias) &
    df["size"].between(tam_min, tam_max)
)
if momento != "Todos":
    mask &= df["Momento"] == momento

dff = df[mask]  # dff = "dataframe filtrado"

# ── 6. ENCABEZADO ─────────────────────────────────────────────
st.title("Propinas en el restaurante")
st.caption(f"Mostrando {len(dff):,} de {len(df):,} cuentas con los filtros aplicados")

# Si el usuario filtra de forma que no queda ninguna fila, avisamos
# y detenemos la ejecución con st.stop(). Así evitamos errores al
# intentar graficar (o calcular promedios de) un DataFrame vacío.
if dff.empty:
    st.warning("No hay datos para los filtros seleccionados. Ajusta el panel lateral.")
    st.stop()

# ── 7. KPIs (TARJETAS DE MÉTRICAS) ───────────────────────────
# st.columns(n) crea n columnas de igual ancho una al lado de la
# otra. st.metric() muestra un número grande con una etiqueta
# arriba y, opcionalmente, una variación ("delta") debajo.
k1, k2, k3, k4 = st.columns(4)

cuentas       = len(dff)
propina_media = dff["tip"].mean()
pct_media     = dff["% propina"].mean()
pct_global    = df["% propina"].mean()  # referencia SIN filtros

k1.metric("Cuentas", f"{cuentas:,}")
k2.metric("Propina promedio", f"${propina_media:,.2f}")
k3.metric("Cuenta promedio", f"${dff['total_bill'].mean():,.2f}")
k4.metric("% propina promedio", f"{pct_media:.1f}%",
          delta=f"{pct_media - pct_global:+.1f} pts vs global")

st.divider()

# ── 8. FILA 1 — DOS GRÁFICOS LADO A LADO ─────────────────────
# st.columns([1, 2]) crea dos columnas donde la segunda es el
# doble de ancha que la primera. Cada "with col:" indica qué va
# dentro de esa columna.
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("¿Quiénes son fumadores?")
    # value_counts() cuenta cuántas veces aparece cada valor de
    # la columna — pandas puro, igual que en un notebook normal.
    conteo = dff["Fumador"].value_counts().reset_index()
    conteo.columns = ["Fumador", "Cuentas"]

    fig = px.pie(
        conteo, names="Fumador", values="Cuentas", hole=0.55,
        color="Fumador", color_discrete_map=COLOR_SI_NO,
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(**LAYOUT, showlegend=False)
    # st.plotly_chart() es el "puente" entre una figura de Plotly
    # y la página de Streamlit. width="stretch" hace que
    # el gráfico ocupe todo el ancho de su columna.
    st.plotly_chart(fig, width="stretch")

with col2:
    st.subheader("Cuentas por día y momento")
    # groupby + size() cuenta filas por combinación de columnas
    # (otra operación 100% pandas).
    g = (dff.groupby(["Día", "Momento", "Fumador"])
            .size().reset_index(name="Cuentas"))

    fig = px.bar(
        g, x="Día", y="Cuentas", color="Fumador",
        facet_col="Momento", barmode="stack",
        color_discrete_map=COLOR_SI_NO,
        category_orders={"Día": ORDEN_DIAS},
    )
    fig.update_layout(**LAYOUT)
    # Los "facets" de Plotly etiquetan cada panel como "Momento=Cena".
    # Esta línea se queda solo con la palabra después del "=".
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig, width="stretch")

# ── 9. FILA 2 — DOS GRÁFICOS MÁS ─────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Distribución del % de propina")
    fig = px.histogram(
        dff, x="% propina", color="Sexo", nbins=20,
        opacity=0.75, barmode="overlay",
        color_discrete_map=COLOR_SEXO,
    )
    fig.update_layout(**LAYOUT)
    st.plotly_chart(fig, width="stretch")

with col4:
    st.subheader("Cuenta total por día")
    fig = px.box(
        dff, x="Día", y="total_bill", color="Día",
        color_discrete_map=COLOR_DIA,
        category_orders={"Día": ORDEN_DIAS},
        labels={"total_bill": "Cuenta total ($)"},
    )
    fig.update_layout(**LAYOUT, showlegend=False)
    st.plotly_chart(fig, width="stretch")

# ── 10. FILA 3 — GRÁFICO INTERACTIVO CON SELECTBOX LOCAL ─────
# Este selectbox NO está en el sidebar: solo afecta a este gráfico.
# Es un buen ejemplo de la diferencia entre un "filtro global"
# (sidebar, afecta todo) y un "control local" (afecta solo una
# sección de la página).
st.subheader("Relación entre cuenta total y propina")

agrupar_por = st.selectbox(
    "Colorear por",
    ["Sexo", "Fumador", "Momento", "Día"],
    key="sel_color",  # 'key' único: obligatorio si hay varios selectbox
)

fig = px.scatter(
    dff, x="total_bill", y="tip", color=agrupar_por,
    trendline="ols",  # línea de tendencia (requiere el paquete statsmodels)
    labels={"total_bill": "Cuenta total ($)", "tip": "Propina ($)"},
)
fig.update_layout(**LAYOUT)
st.plotly_chart(fig, width="stretch")

# ── 11. TABLA DE DATOS (DESPLEGABLE) ─────────────────────────
# st.expander crea una sección colapsable: útil para no saturar
# la pantalla con la tabla completa todo el tiempo.
with st.expander("Ver datos filtrados"):
    columnas = ["Día", "Momento", "size", "total_bill", "tip", "% propina", "Sexo", "Fumador"]
    st.dataframe(
        dff[columnas].rename(columns={"size": "Personas"}),
        width="stretch",
        hide_index=True,
    )

# ════════════════════════════════════════════════════════════
# 🧪 EJERCICIOS PARA PRACTICAR
# (Bórralos cuando termines — son solo ideas para extender la app)
#
#  1. Agrega un widget st.checkbox("Solo cuentas grandes (size >= 4)")
#     y combínalo con la máscara de filtros (sección 5).
#
#  2. Agrega una quinta columna de KPI con la propina MÁXIMA
#     (dff["tip"].max()).
#
#  3. Cambia el gráfico de la sección 9 (col4) de px.box a
#     px.violin y compara cómo se ve la distribución.
#
#  4. Agrega un nuevo st.selectbox en la sección 10 para elegir
#     también la variable del eje X (por ejemplo, "size" en vez
#     de "total_bill").
# ════════════════════════════════════════════════════════════
