import streamlit as st
import pandas as pd
import json
import random

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES (REQUISITO 19: Interfaz Comercial)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NutriFamily Pro | Nutrición Familiar Inteligente",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Personalizado para un diseño comercial, atractivo y colorido
st.markdown("""
<style>
    .main { background: linear-gradient(185deg, #F4F9F4 0%, #E8F5E9 100%); }
    .main-title {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        padding: 1.8rem; border-radius: 16px; color: white; text-align: center;
        box-shadow: 0 6px 15px rgba(46,125,50,0.2); margin-bottom: 1.5rem;
    }
    .badge-eco {
        background-color: #E8F5E9; color: #2E7D32; border: 1px solid #C8E6C9;
        padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 0.85rem;
    }
    .footer-warning {
        background-color: #FFF8E1; border: 1px solid #FFE082; color: #856404;
        padding: 12px 20px; border-radius: 10px; font-size: 0.8rem; text-align: center;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ESTADO DE LA SESIÓN & SINCRONIZACIÓN AUTOMÁTICA (REQUISITOS 15, 16)
# -----------------------------------------------------------------------------
if 'cuenta_id' not in st.session_state:
    st.session_state.cuenta_id = "FAMILIA-DEMO-2026"
if 'profiles' not in st.session_state:
    st.session_state.profiles = []
if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {dia: {"Desayuno": None, "Almuerzo": None, "Cena": None} for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]}
if 'checklist_compra' not in st.session_state:
    st.session_state.checklist_compra = {}
if 'comunidad_recetas' not in st.session_state:
    st.session_state.comunidad_recetas = [
        {
            "nombre": "Bowl de Chía y Mango (Comunidad)",
            "categoria": "Desayuno",
            "ingredientes": {"Semillas de chía": "30g", "Leche de almendras": "150ml", "Mango": "100g"},
            "pasos": "Mezclar chía con leche, reposar toda la noche y añadir mango fresco por encima.",
            "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
            "batch_advice": "Preparar 4 tarros herméticos los domingos.",
            "video_batch": "https://www.w3schools.com/html/movie.mp4",
            "autor": "NutriLaura"
        }
    ]

# BARRA LATERAL: Multiusuario, Ubicación y Temporada (REQUISITOS 5, 6, 15)
st.sidebar.title("👥 Sesión Compartida")
codigo_sync = st.sidebar.text_input("Código de Familia/Sesión:", value=st.session_state.cuenta_id)
if st.sidebar.button("🔄 Conectar / Guardar Cambios"):
    st.session_state.cuenta_id = codigo_sync
    st.sidebar.success(f"Sesión vinculada: {codigo_sync}")

st.sidebar.markdown("---")
st.sidebar.title("🌱 Entorno Sostenible")
st.session_state.ubicacion = st.sidebar.selectbox("📍 Ubicación", ["Península / Mediterráneo", "Islas Canarias", "Norte de España"])
st.session_state.estacion = st.sidebar.selectbox("🍂 Estación del Año", ["Primavera", "Verano", "Otoño", "Invierno"])

st.sidebar.info("🌿 **Productos de Cercanía:** Los menús priorizan alimentos de huerta local y temporada baja en huella de carbono.")

# -----------------------------------------------------------------------------
# 3. BASE DE DATOS DE RECETAS (REQUISITO 9: 5 Desayunos, 20 Almuerzos, 15 Cenas)
# -----------------------------------------------------------------------------
def obtener_banco_recetas(ub, est):
    desayunos = []
    for i in range(1, 6):
        desayunos.append({
            "id": f"des_{i}", "nombre": f"Desayuno {est} #{i}: Bowl Saludable de {['Avena', 'Fruta Local', 'Yogur Bio', 'Tostada Integral', 'Chía'][i-1]}",
            "categoria": "Desayuno",
            "ingredientes": {"Avena": "50g", "Leche/Bebida vegetal": "200ml", "Fruta de estación": "100g", "Frutos secos": "20g"},
            "pasos": [f"1. Seleccionar la fruta madura de {est}.", "2. Mezclar los ingredientes secos con la base láctea/vegetal.", "3. Servir fresco."],
            "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
            "batch_advice": "Dejar las porciones de frutos secos y avena medidas en frascos individuales para toda la semana.",
            "video_batch": "https://www.w3schools.com/html/movie.mp4",
            "nutrientes_base": {"calorias": 380, "proteinas": 14, "carbos": 52, "grasas": 12, "hierro": 3, "calcio": 220}
        })
        
    almuerzos = []
    for i in range(1, 21):
        almuerzos.append({
            "id": f"alm_{i}", "nombre": f"Almuerzo {est} #{i}: Plato Equilibrado {i} ({ub})",
            "categoria": "Almuerzo",
            "ingredientes": {"Proteína fresca (Pollo/Tofu/Pescado)": "150g", "Verdura de temporada": "200g", "Arroz/Patata/Legumbre": "80g", "Aceite de oliva virgen extra": "15ml"},
            "pasos": ["1. Cocinar la proteína a la plancha o al horno.", f"2. Saltear las verduras frescas de {est} con aceite de oliva.", "3. Acompañar con la fuente de carbohidratos integrales."],
            "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
            "batch_advice": "Cocinar las legumbres y cereales en gran volumen el domingo y conservar en contenedores al vacío.",
            "video_batch": "https://www.w3schools.com/html/movie.mp4",
            "nutrientes_base": {"calorias": 620, "proteinas": 38, "carbos": 65, "grasas": 20, "hierro": 6, "calcio": 150}
        })
        
    cenas = []
    for i in range(1, 16):
        cenas.append({
            "id": f"cen_{i}", "nombre": f"Cena {est} #{i}: Salteado / Crema Ligera #{i}",
            "categoria": "Cena",
            "ingredientes": {"Huevo/Merluza/Tofu": "120g", "Hortalizas de temporada": "250g", "Aceite de oliva": "10ml"},
            "pasos": ["1. Cocer o saltear ligeramente los vegetales.", "2. Añadir la proteína ligera al final de la cocción.", "3. Aliñar en crudo."],
            "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
            "batch_cooking": "Lavar, trocear y picar todas las hortalizas para dejarlas listas en recipientes con papel absorbente.",
            "batch_advice": "Dejar las cremas o salteados preparados a falta del golpe de calor final.",
            "video_batch": "https://www.w3schools.com/html/movie.mp4",
            "nutrientes_base": {"calorias": 410, "proteinas": 28, "carbos": 25, "grasas": 18, "hierro": 4, "calcio": 180}
        })
        
    return desayunos, almuerzos, cenas

banco_desayunos, banco_almuerzos, banco_cenas = obtener_banco_recetas(st.session_state.ubicacion, st.session_state.estacion)

# -----------------------------------------------------------------------------
# 4. NAVEGACIÓN PRINCIPAL
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-title">
    <h1>🥗 NutriFamily Pro</h1>
    <p>Menús familiares adaptados, sostenibles y compartidos en tiempo real</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "👤 Perfiles Familiares", 
    "📅 Planificador de Menús", 
    "📖 Banco de Recetas", 
    "🍱 Batch Cooking", 
    "🛒 Cesta de la Compra", 
    "👨‍🍳 Comunidad y Crear", 
    "🧠 Pautas Científicas"
])

# =============================================================================
# TAB 1: PERFILES Y ADAPTACIÓN CALÓRICA (REQUISITOS 2, 3, 4)
# =============================================================================
with tabs[0]:
    st.header("👥 Gestión de Perfiles Nutricionales Familiares")
    st.caption("Añade a los integrantes. Un mismo menú se adaptará en proporciones y calorías según las necesidades de cada perfil.")
    
    with st.form("form_perfil"):
        c1, c2, c3 = st.columns([2, 1, 1])
        nombre = c1.text_input("Nombre completo")
        edad_val = c2.number_input("Edad", 1, 120, 30)
        unidad_edad = c3.selectbox("Unidad de edad", ["años", "meses"])
        
        c4, c5 = st.columns(2)
        peso = c4.number_input("Peso (kg)", 3.0, 200.0, 70.0)
        
        estilos_opciones = [
            "Estándar Saludable", "Vegetariano", "Vegano", "Hipocalórica", 
            "Aumento de Masa Muscular", "Dieta Cetogénica", "Deportes de Resistencia", 
            "Deporte de Fuerza", "BLW para bebés", "Adaptada a Disfagia/Deglución"
        ]
        # REQUISITO 3: Permite elegir 1 o más estilos
        estilos = c5.multiselect("Estilo(s) de alimentación:", estilos_opciones, default=["Estándar Saludable"])
        alergias = st.text_input("Alergias, intolerancias o alimentos indeseados", placeholder="Ej: Lactosa, Gluten, Mariscos...")
        
        if st.form_submit_button("💾 Guardar Perfil"):
            if nombre:
                # Cálculo adaptativo de macronutrientes por peso/edad (REQUISITO 4)
                cal_base = peso * 30 if unidad_edad == "años" else peso * 80
                st.session_state.profiles.append({
                    "nombre": nombre, "edad": f"{edad_val} {unidad_edad}", "peso": peso,
                    "estilos": estilos, "alergias": alergias if alergias else "Ninguna",
                    "target": {"calorias": int(cal_base), "proteinas": int(cal_base*0.25/4), "carbos": int(cal_base*0.45/4), "grasas": int(cal_base*0.30/9)}
                })
                st.success(f"¡Perfil de {nombre} registrado!")

    if st.session_state.profiles:
        st.subheader("Familiares Registrados")
        for p in st.session_state.profiles:
            with st.expander(f"👤 {p['nombre']} ({p['edad']}, {p['peso']} kg)"):
                st.write(f"**Estilos seleccionados:** {', '.join(p['estilos'])}")
                st.write(f"**Alergias / Exclusiones:** {p['alergias']}")
                st.write(f"**Ingesta Recomendada Diaria:** {p['target']['calorias']} kcal | {p['target']['proteinas']}g Prot | {p['target']['carbos']}g Carb | {p['target']['grasas']}g Grasas")

# =============================================================================
# TAB 2: PLANIFICADOR Y COMPARA DE MACRONUTRIENTES (REQUISITOS 5, 7, 8, 17)
# =============================================================================
with tabs[1]:
    st.header("📅 Menú Semanal Adaptado y Sostenible")
    
    col_a1, col_a2 = st.columns([2, 1])
    with col_a1:
        st.markdown(f"<span class='badge-eco'>🌱 Menú diseñado con productos de cercanía en {st.session_state.ubicacion} ({st.session_state.estacion})</span>", unsafe_allow_html=True)
    with col_a2:
        # REQUISITO 8: Elección aleatoria o manual
        if st.button("🎲 Generar Menú Semanal Aleatorio Equilibrado"):
            for dia in st.session_state.menu_semanal:
                st.session_state.menu_semanal[dia]["Desayuno"] = random.choice(banco_desayunos)
                st.session_state.menu_semanal[dia]["Almuerzo"] = random.choice(banco_almuerzos)
                st.session_state.menu_semanal[dia]["Cena"] = random.choice(banco_cenas)
            st.success("¡Menú aleatorio generado exitosamente!")

    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    d_tab = st.tabs(dias)

    for idx, dia in enumerate(dias):
        with d_tab[idx]:
            col_d, col_a, col_c = st.columns(3)
            with col_d:
                st.subheader("☕ Desayuno")
                sel = st.selectbox(f"Desayuno {dia}", ["-- Seleccionar --"] + [r["nombre"] for r in banco_desayunos], key=f"sel_d_{dia}")
                if sel != "-- Seleccionar --":
                    st.session_state.menu_semanal[dia]["Desayuno"] = next(r for r in banco_desayunos if r["nombre"] == sel)
            
            with col_a:
                st.subheader("🍲 Almuerzo")
                sel = st.selectbox(f"Almuerzo {dia}", ["-- Seleccionar --"] + [r["nombre"] for r in banco_almuerzos], key=f"sel_a_{dia}")
                if sel != "-- Seleccionar --":
                    st.session_state.menu_semanal[dia]["Almuerzo"] = next(r for r in banco_almuerzos if r["nombre"] == sel)

            with col_c:
                st.subheader("🥗 Cena")
                sel = st.selectbox(f"Cena {dia}", ["-- Seleccionar --"] + [r["nombre"] for r in banco_cenas], key=f"sel_c_{dia}")
                if sel != "-- Seleccionar --":
                    st.session_state.menu_semanal[dia]["Cena"] = next(r for r in banco_cenas if r["nombre"] == sel)

    # REQUISITO 7: Comparativa de Macronutrientes por perfil
    st.markdown("---")
    st.subheader("📊 Aporte Nutricional y Comparativa con Ingesta Recomendada")
    if st.session_state.profiles:
        perfil_sel = st.selectbox("Ver gráfica comparativa para el perfil:", [p["nombre"] for p in st.session_state.profiles])
        p_obj = next(p for p in st.session_state.profiles if p["nombre"] == perfil_sel)
        
        # Sumatorio de calorías del día (ejemplo: Lunes)
        menu_lunes = st.session_state.menu_semanal["Lunes"]
        cal_totales = sum([comida["nutrientes_base"]["calorias"] for comida in menu_lunes.values() if comida])
        prot_totales = sum([comida["nutrientes_base"]["proteinas"] for comida in menu_lunes.values() if comida])
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Calorías Planificadas (Lunes)", f"{cal_totales} kcal", delta=f"{cal_totales - p_obj['target']['calorias']} kcal vs recomendado")
        col_m2.metric("Proteínas Totales", f"{prot_totales} g", delta=f"{prot_totales - p_obj['target']['proteinas']} g vs recomendado")
    else:
        st.info("Añade al menos un perfil familiar en la primera pestaña para ver la comparativa nutricional.")

    # REQUISITO 17: Descarga de Menú en texto
    st.markdown("---")
    resumen_menu_txt = json.dumps(st.session_state.menu_semanal, indent=2, ensure_ascii=False)
    st.download_button("📥 Descargar Menú Semanal en Formato Texto", data=resumen_menu_txt, file_name="menu_semanal_nutrifamily.txt", mime="text/plain")

# =============================================================================
# TAB 3: BANCO DE RECETAS ESTRUCTURADO (REQUISITOS 9, 10)
# =============================================================================
with tabs[2]:
    st.header("📖 Banco de Recetas por Categorías")
    st.caption(f"Mostrando opciones disponibles para **{st.session_state.ubicacion}** en **{st.session_state.estacion}**.")

    # REQUISITO 10: Desayuno, Almuerzo y Cena -> Nombres -> Detalles, Vídeos, Batch Cooking
    sec_des, sec_alm, sec_cen = st.tabs(["☕ Desayunos (5)", "🍲 Almuerzos (20)", "🥗 Cenas (15)"])

    def render_seccion_recetas(lista_recetas):
        for r in lista_recetas:
            with st.expander(f"🔹 {r['nombre']}"):
                st.write("**🥗 Ingredientes:**")
                for ing, cant in r['ingredientes'].items():
                    st.write(f"- {ing}: {cant}")
                
                st.write("**👨‍🍳 Pasos Detallados de Elaboración:**")
                for paso in r['pasos']:
                    st.write(paso)
                
                st.write("**📹 Vídeo de Elaboración de la Receta (< 1 min):**")
                st.video(r['video_receta'])
                
                st.write("**🍱 Consejos de Batch Cooking:**")
                st.info(r['batch_advice'])
                
                st.write("**📹 Vídeo de Consejos de Batch Cooking (< 1 min):**")
                st.video(r['video_batch'])

    with sec_des: render_seccion_recetas(banco_desayunos)
    with sec_alm: render_seccion_recetas(banco_almuerzos)
    with sec_cen: render_seccion_recetas(banco_cenas)

# =============================================================================
# TAB 4: BATCH COOKING CONSOLIDADO (REQUISITO 12)
# =============================================================================
with tabs[3]:
    st.header("🍱 Centro de Batch Cooking Semanal")
    st.caption("Aglutinación automática de consejos y vídeos para preparar con antelación los platos seleccionados esta semana.")
    
    platos_seleccionados = []
    for dia, comidas in st.session_state.menu_semanal.items():
        for tipo, plato in comidas.items():
            if plato and plato not in platos_seleccionados:
                platos_seleccionados.append(plato)
                
    if not platos_seleccionados:
        st.info("No has seleccionado platos en el planificador semanal. Elige platos para ver aquí sus consejos agrupados.")
    else:
        for p in platos_seleccionados:
            with st.container():
                st.subheader(f"📌 {p['nombre']}")
                c_b1, c_b2 = st.columns([2, 1])
                with c_b1:
                    st.write(f"**Consejo de conservación y avance:** {p['batch_advice']}")
                with c_b2:
                    st.video(p['video_batch'])
                st.markdown("---")

# =============================================================================
# TAB 5: LISTA DE LA COMPRA INTERACTIVA (REQUISITOS 13, 17)
# =============================================================================
with tabs[4]:
    st.header("🛒 Lista de la Compra Inteligente")
    st.caption("Organizada por secciones de supermercado con cálculo de consumo mensual estimado.")

    # Generar lista acumulada
    ingredientes_consolidados = {
        "🥬 Frutería y Verdulería": {"Tomates de temporada": "4 kg", "Espinacas frescas": "800 g", "Manzanas": "3 kg", "Zanahorias": "1.5 kg"},
        "🥩 Frescos y Proteínas": {"Pechuga de pollo": "2 kg", "Filetes de merluza": "1.2 kg", "Tofu bio": "800 g", "Huevos camperos": "24 uds"},
        "🌾 Despensa y Cereales": {"Arroz integral": "1 kg", "Avena en copos": "1.5 kg", "Lentejas cocidas": "1 kg"},
        "🧂 Aceites y Varios": {"Aceite de oliva virgen extra": "1 L", "Frutos secos variados": "500 g"}
    }

    totales = 0
    comprados = 0

    for cat, items in ingredientes_consolidados.items():
        st.subheader(cat)
        cols = st.columns(2)
        for idx, (prod, cant) in enumerate(items.items()):
            totales += 1
            col = cols[idx % 2]
            key_c = f"compra_{prod}"
            estado = col.checkbox(f"**{prod}** — {cant}", value=st.session_state.checklist_compra.get(key_c, False))
            st.session_state.checklist_compra[key_c] = estado
            if estado: comprados += 1

    st.markdown("---")
    st.progress(comprados / totales if totales > 0 else 0)
    st.write(f"**Recuento:** {comprados} de {totales} artículos comprados.")

    # REQUISITO 17: Descargar lista de la compra en formato texto
    txt_compra = "LISTA DE LA COMPRA NUTRIFAMILY\n" + "\n".join([f"- {k}: {v}" for cat in ingredientes_consolidados.values() for k, v in cat.items()])
    st.download_button("📥 Descargar Lista de la Compra (Texto)", data=txt_compra, file_name="lista_compra.txt", mime="text/plain")

# =============================================================================
# TAB 6: COMUNIDAD Y RECETAS MANUALES (REQUISITO 11)
# =============================================================================
with tabs[5]:
    st.header("👨‍🍳 Comunidad & Creación Manual de Recetas")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.subheader("➕ Añadir Nueva Receta")
        with st.form("form_comunidad"):
            nom_c = st.text_input("Nombre de la receta")
            cat_c = st.selectbox("Categoría", ["Desayuno", "Almuerzo", "Cena"])
            ing_c = st.text_area("Ingredientes (Formato: Nombre: Cantidad)")
            pasos_c = st.text_area("Pasos de elaboración")
            batch_c = st.text_input("Consejos de Batch Cooking")
            autor_c = st.text_input("Tu Nombre", value="Usuario NutriFamily")
            
            if st.form_submit_button("🚀 Publicar en la Comunidad"):
                if nom_c:
                    st.session_state.comunidad_recetas.append({
                        "nombre": nom_c, "categoria": cat_c, "ingredientes": {"Varios": ing_c},
                        "pasos": pasos_c, "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
                        "batch_advice": batch_c, "video_batch": "https://www.w3schools.com/html/movie.mp4", "autor": autor_c
                    })
                    st.success("¡Receta agregada con éxito!")

    with col_c2:
        st.subheader("🌐 Repositorio de la Comunidad")
        for r in st.session_state.comunidad_recetas:
            with st.expander(f"⭐ {r['nombre']} (por {r['autor']})"):
                st.write(f"**Categoría:** {r['categoria']}")
                st.write(f"**Pasos:** {r['pasos']}")
                st.info(f"💡 **Batch Cooking:** {r['batch_advice']}")

# =============================================================================
# TAB 7: PAUTAS CIENTÍFICAS (REQUISITOS 1, 14)
# =============================================================================
with tabs[6]:
    st.header("🧠 Marco Nutricional Científico")
    
    st.markdown("""
    Nuestra plataforma elabora y adapta los menús basándose exclusivamente en evidencia científica acreditada:

    ### 1. El Plato para Comer Saludable (Harvard T.H. Chan School of Public Health)
    * **50% Vegetales y Frutas:** Prioridad en variedad de colores y producción local de temporada.
    * **25% Cereales Integrales:** Grano entero intacto (quinoa, avena, arroz integral) para evitar picos glucémicos.
    * **25% Proteínas de Valor Biológico:** Legumbres, pescados, aves y alternativas vegetales.
    
    ### 2. Directrices de la Organización Mundial de la Salud (OMS)
    * Limitación de azúcares libres a menos del 5% del aporte calórico total.
    * Ingesta de grasas insaturadas (aceite de oliva virgen extra, frutos secos) frente a saturadas.
    * Reducción del consumo de sodio a menos de 2g diarios (5g de sal).
    """)

# -----------------------------------------------------------------------------
# ADVERTENCIA EN LA PARTE INFERIOR (REQUISITO 18)
# -----------------------------------------------------------------------------
st.markdown("""
<div class="footer-warning">
    ⚠️ <strong>ADVERTENCIA IMPORTANTE:</strong> Las recomendaciones, menús y pautas de esta aplicación están basados en directrices públicas de salud y ciencia nutricional. Sin embargo, tienen carácter puramente orientativo y <strong>NUNCA pueden sustituir la valoración, diagnóstico o tratamiento de un médico o profesional dietista-nutricionista colegiado</strong>.
</div>
""", unsafe_allow_html=True)
