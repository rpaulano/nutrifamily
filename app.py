import streamlit as st
import pandas as pd
import json
import random

# -----------------------------------------------------------------------------
# 1. ESTILOS VISUALES (Inspiración UI: BLW Ideas & Premium Health Apps)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NutriFamily | Menús Familiares Inteligentes",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    
    .main {
        background-color: #FAFAFA;
    }
    
    .header-card {
        background: linear-gradient(135deg, #FF8A65 0%, #FFB74D 100%);
        padding: 2rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(255, 138, 101, 0.25);
        margin-bottom: 2rem;
    }
    
    .profile-card {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 1.2rem;
        border-left: 6px solid #4CAF50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    .badge-tag {
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    
    .footer-warning {
        background-color: #FFF3E0;
        border: 2px solid #FFE0B2;
        color: #E65100;
        padding: 16px;
        border-radius: 16px;
        font-size: 0.85rem;
        text-align: center;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ESTADO DE LA SESIÓN Y SINCRONIZACIÓN
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
            "nombre": "🥞 Tortitas de Plátano y Avena (Sin Azúcar)",
            "categoria": "Desayuno",
            "ingredientes": {"Plátano maduro": "1 ud", "Copos de avena": "40g", "Huevo": "1 ud", "Canela": "1 pizca"},
            "pasos": "Triturar todo en batidora y cocinar pequeñas porciones en sartén antiadherente a fuego medio.",
            "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
            "batch_advice": "Se pueden congelar separadas por papel vegetal y calentar en tostadora.",
            "video_batch": "https://www.w3schools.com/html/movie.mp4",
            "autor": "NutriMama_BLW"
        }
    ]

# BARRA LATERAL
st.sidebar.title("👥 Sesión Familiar")
codigo_sync = st.sidebar.text_input("Código de Sesión Compartida:", value=st.session_state.cuenta_id)
if st.sidebar.button("🔄 Guardar / Sincronizar"):
    st.session_state.cuenta_id = codigo_sync
    st.sidebar.success(f"Conectado a: {codigo_sync}")

st.sidebar.markdown("---")
st.sidebar.title("🌿 Filtros de Cercanía")
st.session_state.ubicacion = st.sidebar.selectbox("📍 Ubicación", ["Península / Mediterráneo", "Islas Canarias", "Norte de España"])
st.session_state.estacion = st.sidebar.selectbox("🍂 Estación del Año", ["Primavera", "Verano", "Otoño", "Invierno"])

# -----------------------------------------------------------------------------
# 3. BANCO DE RECETAS CON NOMBRES REALES Y DETALLADOS
# -----------------------------------------------------------------------------
def obtener_banco_recetas(ub, est):
    desayunos = [
        {"id": "d1", "nombre": "🥣 Porridge de Avena con Arándanos y Almendras", "categoria": "Desayuno", "ingredientes": {"Copos de avena": "50g", "Bebida vegetal / Leche": "200ml", "Arándanos frescos": "40g", "Almendra laminada": "15g"}, "pasos": ["Cocer la avena con la leche 5 min.", "Servir con frutos rojos y almendras."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Dejar la mezcla seca guardada en tarros de cristal.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 360, "proteinas": 12, "carbos": 50, "grasas": 11, "hierro": 3.2, "calcio": 180}},
        {"id": "d2", "nombre": "🥑 Tostada Integral con Aguacate y Huevo Escalfado", "categoria": "Desayuno", "ingredientes": {"Pan 100% integral": "2 rebanadas", "Aguacate": "0.5 ud", "Huevo": "1 ud", "Semillas de sésamo": "5g"}, "pasos": ["Tostar el pan.", "Chafar el aguacate y montar con el huevo cocido 3 min."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Tener los huevos cocidos en nevera.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 410, "proteinas": 16, "carbos": 35, "grasas": 21, "hierro": 2.8, "calcio": 90}},
        {"id": "d3", "nombre": "🥞 Tortitas de Banana y Chía con Yogur Griego", "categoria": "Desayuno", "ingredientes": {"Plátano": "1 ud", "Avena": "30g", "Semillas de chía": "10g", "Yogur griego": "100g"}, "pasos": ["Mezclar ingredientes y hacer a la sartén.", "Acompañar con yogur."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Congelar hechas y calentar al instante.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 380, "proteinas": 14, "carbos": 58, "grasas": 10, "hierro": 2.1, "calcio": 210}},
        {"id": "d4", "nombre": "🍌 Smoothie Bowl de Plátano, Espinacas y Cacao", "categoria": "Desayuno", "ingredientes": {"Plátano congelado": "1 ud", "Espinaca baby fresca": "30g", "Cacao puro": "10g", "Leche de almendras": "150ml"}, "pasos": ["Triturar a alta potencia hasta consistencia cremoso.", "Servir con toppings."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Dejar bolsas de fruta congelada porcionadas.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 310, "proteinas": 9, "carbos": 54, "grasas": 6, "hierro": 3.5, "calcio": 240}},
        {"id": "d5", "nombre": "🥪 Mollete de Tomate Rallado, Aceite AOVE y Pavo", "categoria": "Desayuno", "ingredientes": {"Mollete integral": "1 ud", "Tomate de huerta": "1 ud", "Aceite de oliva virgen extra": "10ml", "Pechuga de pavo artesana": "40g"}, "pasos": ["Rallar el tomate fresco.", "Montar sobre el pan tostado con el aceite en crudo."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Rallar tomate para 2-3 días en frasco hermético.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 350, "proteinas": 18, "carbos": 42, "grasas": 12, "hierro": 2.0, "calcio": 60}}
    ]
    
    almuerzos = [
        {"id": "a1", "nombre": "Salmon al Horno con Patatas y Espárragos Verdes", "categoria": "Almuerzo", "ingredientes": {"Lomo de salmón fresco": "150g", "Patata nueva": "150g", "Espárragos trigueros": "100g", "AOVE": "10ml"}, "pasos": ["Hornear todo a 180°C durante 20 min."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Asar las patatas previamente en el batch cooking dominical.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 580, "proteinas": 36, "carbos": 40, "grasas": 26, "hierro": 2.5, "calcio": 80}},
        {"id": "a2", "nombre": "Lentejas Pardinas Estofadas con Verduras de la Huerta", "categoria": "Almuerzo", "ingredientes": {"Lenteja pardina": "80g", "Zanahoria": "50g", "Pimiento verde": "40g", "Calabaza": "60g", "Laurel": "1 hoja"}, "pasos": ["Cocer a fuego lento 40 min con las verduras picadas."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "El guiso mejora de sabor al día siguiente en nevera.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 510, "proteinas": 28, "carbos": 75, "grasas": 8, "hierro": 7.5, "calcio": 110}},
        {"id": "a3", "nombre": "Pechuga de Pollo a la Plancha con Quinoa y Calabacín", "categoria": "Almuerzo", "ingredientes": {"Pechuga de pollo": "150g", "Quinoa real": "70g", "Calabacín": "120g", "Limón": "0.5 ud"}, "pasos": ["Cocer quinoa. Marcar pollo y calabacín a la plancha."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Conservar la quinoa cocida al vacío hasta 5 días.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 490, "proteinas": 42, "carbos": 48, "grasas": 12, "hierro": 3.8, "calcio": 65}},
        {"id": "a4", "nombre": "Arroz Integral Salteado con Tofu y Brócoli al Vapor", "categoria": "Almuerzo", "ingredientes": {"Arroz integral": "70g", "Tofu firme": "120g", "Brócoli": "150g", "Salsa de soja baja en sal": "10ml"}, "pasos": ["Saltear tofu en dados con el arroz y el brócoli."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Prensar y marinar el tofu con antelación.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 460, "proteinas": 24, "carbos": 62, "grasas": 14, "hierro": 4.9, "calcio": 220}},
        {"id": "a5", "nombre": "Garbanzos Salteados con Espinacas y Pimentón de la Vera", "categoria": "Almuerzo", "ingredientes": {"Garbanzos cocidos": "200g", "Espinacas frescas": "150g", "Ajo": "2 dientes", "Pimentón dulce": "5g"}, "pasos": ["Dorar ajos, añadir espinacas y rehogar garbanzos."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Usar garbanzos cocidos en conserva aclarados.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 440, "proteinas": 22, "carbos": 58, "grasas": 11, "hierro": 6.2, "calcio": 190}}
    ]
    # Completar relleno de muestra
    for i in range(6, 21):
        almuerzos.append({
            "id": f"a{i}", "nombre": f"Plato Mediterráneo #{i}: Proteína de Temporada con Verduras Asadas",
            "categoria": "Almuerzo", "ingredientes": {"Proteína principal": "140g", "Vegetales locales": "180g", "Cereal integral": "60g"},
            "pasos": ["Cocinar al vapor o plancha y aliñar con aceite de oliva."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
            "batch_advice": "Porcionar en tuppers de cristal.", "video_batch": "https://www.w3schools.com/html/movie.mp4",
            "nutrientes_base": {"calorias": 500, "proteinas": 30, "carbos": 50, "grasas": 15, "hierro": 3.0, "calcio": 100}
        })
        
    cenas = [
        {"id": "c1", "nombre": "🥣 Crema Suave de Calabaza y Quesitos con Pipas", "categoria": "Cena", "ingredientes": {"Calabaza": "200g", "Patata": "50g", "Quesitos ligeros": "2 uds", "Pipas de calabaza": "10g"}, "pasos": ["Cocer vegetales 15 min y batir con quesitos."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Guardar en frasco de cristal en nevera hasta 4 días.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 290, "proteinas": 9, "carbos": 34, "grasas": 12, "hierro": 2.1, "calcio": 160}},
        {"id": "c2", "nombre": "🐟 Merluza a la Plancha con Ensalada de Tomate y Aguacate", "categoria": "Cena", "ingredientes": {"Lomo de merluza": "150g", "Tomate": "150g", "Aguacate": "40g", "Orégano": "1 pizca"}, "pasos": ["Marcar la merluza a fuego fuerte 3 min por lado."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Tener la ensalada lavada y trocear tomate al momento.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 340, "proteinas": 28, "carbos": 12, "grasas": 18, "hierro": 1.5, "calcio": 50}},
        {"id": "c3", "nombre": "🍳 Tortilla Francesa de Espárragos Verdes y Ensalada", "categoria": "Cena", "ingredientes": {"Huevos camperos": "2 uds", "Espárragos trigueros": "80g", "Canónigos": "40g"}, "pasos": ["Saltear espárragos y cuajar la tortilla."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4", "batch_advice": "Dejar los espárragos salteados previamente.", "video_batch": "https://www.w3schools.com/html/movie.mp4", "nutrientes_base": {"calorias": 310, "proteinas": 18, "carbos": 6, "grasas": 22, "hierro": 2.7, "calcio": 95}}
    ]
    for i in range(4, 16):
        cenas.append({
            "id": f"c{i}", "nombre": f"Cena Ligera #{i}: Salteado de Hortalizas con Huevo / Tofu",
            "categoria": "Cena", "ingredientes": {"Verduras de temporada": "200g", "Proteína ligera": "100g", "AOVE": "8ml"},
            "pasos": ["Cocinar a fuego rápido en wok o sartén."], "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
            "batch_advice": "Dejar verdura cortada en bolsas cerradas.", "video_batch": "https://www.w3schools.com/html/movie.mp4",
            "nutrientes_base": {"calorias": 300, "proteinas": 20, "carbos": 15, "grasas": 14, "hierro": 2.0, "calcio": 80}
        })

    return desayunos, almuerzos, cenas

banco_desayunos, banco_almuerzos, banco_cenas = obtener_banco_recetas(st.session_state.ubicacion, st.session_state.estacion)

# -----------------------------------------------------------------------------
# 4. ENCABEZADO Y PESTAÑAS PRINCIPALES
# -----------------------------------------------------------------------------
st.markdown("""
<div class="header-card">
    <h1 style='color: white; margin:0;'>🥑 NutriFamily Pro</h1>
    <p style='margin:0; font-size:1.1rem;'>Planes nutricionales adaptados para cada miembro de la familia</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "👶 Perfiles Nutricionales", 
    "📅 Planificador Semanal", 
    "📖 Banco de Recetas", 
    "🍱 Batch Cooking", 
    "🛒 Cesta de la Compra", 
    "👨‍🍳 Comunidad", 
    "🧠 Base Científica"
])

# =============================================================================
# TAB 1: PERFILES CON VALORES NUTRICIONALES ESPECÍFICOS Y DIFERENCIADOS
# =============================================================================
with tabs[0]:
    st.subheader("👨‍👩‍👧‍👦 Perfiles de la Familia y Necesidades Específicas")
    
    with st.form("form_nuevo_perfil"):
        col1, col2, col3 = st.columns([2, 1, 1])
        nombre = col1.text_input("Nombre")
        edad = col2.number_input("Edad", 1, 120, 28)
        unidad_edad = col3.selectbox("Unidad", ["años", "meses"])
        
        col4, col5 = st.columns(2)
        peso = col4.number_input("Peso (kg)", 3.0, 150.0, 65.0)
        estilos = col5.multiselect("Estilo(s) de Alimentación:", [
            "Estándar Saludable", "Vegetariano", "Vegano", "BLW (Bebés)", 
            "Aumento Muscular", "Hipocalórica", "Ceto", "Deporte Resistencia"
        ], default=["Estándar Saludable"])
        
        alergias = st.text_input("Alergias o exclusiones", placeholder="Ej: Gluten, Lactosa, Frutos secos")
        
        if st.form_submit_button("➕ Registrar Perfil"):
            if nombre:
                # CÁLCULO ESPECÍFICO DIFERENCIADO POR PERFIL
                factor_edad = 0.8 if unidad_edad == "meses" else (1.2 if edad > 18 else 1.0)
                factor_meta = 1.3 if "Aumento Muscular" in estilos else (0.85 if "Hipocalórica" in estilos else 1.0)
                
                cal_target = int(peso * 32 * factor_edad * factor_meta)
                prot_target = int((cal_target * 0.25) / 4)
                carb_target = int((cal_target * 0.45) / 4)
                gras_target = int((cal_target * 0.30) / 9)
                hierro_target = round(8 + (peso * 0.1), 1)
                calcio_target = int(500 + (peso * 8))

                st.session_state.profiles.append({
                    "nombre": nombre, "edad": f"{edad} {unidad_edad}", "peso": peso,
                    "estilos": estilos, "alergias": alergias if alergias else "Ninguna",
                    "targets": {
                        "calorias": cal_target, "proteinas": prot_target,
                        "carbos": carb_target, "grasas": gras_target,
                        "hierro": hierro_target, "calcio": calcio_target
                    }
                })
                st.success(f"Perfil de {nombre} registrado con requerimientos personalizados.")

    if st.session_state.profiles:
        st.markdown("### 📋 Requerimientos Específicos Calculados por Persona")
        cols_p = st.columns(len(st.session_state.profiles))
        for idx, p in enumerate(st.session_state.profiles):
            with cols_p[idx % len(cols_p)]:
                st.markdown(f"""
                <div class="profile-card">
                    <h3>👤 {p['nombre']}</h3>
                    <p><b>Edad/Peso:</b> {p['edad']} | {p['peso']} kg</p>
                    <p><b>Estilos:</b> <span class="badge-tag">{', '.join(p['estilos'])}</span></p>
                    <hr>
                    <p><b>⚡ Calorías:</b> {p['targets']['calorias']} kcal/día</p>
                    <p><b>🥩 Proteínas:</b> {p['targets']['proteinas']} g</p>
                    <p><b>🌾 Carbohidratos:</b> {p['targets']['carbos']} g</p>
                    <p><b>🥑 Grasas:</b> {p['targets']['grasas']} g</p>
                    <p><b>🩸 Hierro:</b> {p['targets']['hierro']} mg</p>
                    <p><b>🦴 Calcio:</b> {p['targets']['calcio']} mg</p>
                </div>
                """, unsafe_allow_html=True)

# =============================================================================
# TAB 2: PLANIFICADOR Y GENERACIÓN ALEATORIA DIRECTA
# =============================================================================
with tabs[1]:
    st.subheader("📅 Planificador Semanal Interactivo")
    
    col_bot1, col_bot2 = st.columns([2, 1])
    with col_bot1:
        st.info(f"🌿 Productos de Cercanía Seleccionados: **{st.session_state.ubicacion}** | **{st.session_state.estacion}**")
    with col_bot2:
        # SELECCIÓN ALEATORIA QUE SE REFLEJA AUTOMÁTICAMENTE
        if st.button("🎲 Cargar Menú Aleatorio Completo"):
            for dia in st.session_state.menu_semanal:
                st.session_state.menu_semanal[dia]["Desayuno"] = random.choice(banco_desayunos)
                st.session_state.menu_semanal[dia]["Almuerzo"] = random.choice(banco_almuerzos)
                st.session_state.menu_semanal[dia]["Cena"] = random.choice(banco_cenas)
            st.success("¡Menú aleatorio generado y asignado al planificador!")

    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    tabs_dias = st.tabs(dias_semana)

    for idx_d, dia in enumerate(dias_semana):
        with tabs_dias[idx_d]:
            c_d, c_a, c_c = st.columns(3)
            
            # Valores por defecto basados en st.session_state
            actual_d = st.session_state.menu_semanal[dia]["Desayuno"]
            actual_a = st.session_state.menu_semanal[dia]["Almuerzo"]
            actual_c = st.session_state.menu_semanal[dia]["Cena"]
            
            nombres_d = [r["nombre"] for r in banco_desayunos]
            nombres_a = [r["nombre"] for r in banco_almuerzos]
            nombres_c = [r["nombre"] for r in banco_cenas]

            with c_d:
                st.markdown("#### ☕ Desayuno")
                idx_sel_d = nombres_d.index(actual_d["nombre"]) if actual_d in banco_desayunos else 0
                sel_d = st.selectbox(f"Seleccionar Desayuno ({dia})", nombres_d, index=idx_sel_d, key=f"s_d_{dia}")
                st.session_state.menu_semanal[dia]["Desayuno"] = next(r for r in banco_desayunos if r["nombre"] == sel_d)

            with c_a:
                st.markdown("#### 🍲 Almuerzo")
                idx_sel_a = nombres_a.index(actual_a["nombre"]) if actual_a in banco_almuerzos else 0
                sel_a = st.selectbox(f"Seleccionar Almuerzo ({dia})", nombres_a, index=idx_sel_a, key=f"s_a_{dia}")
                st.session_state.menu_semanal[dia]["Almuerzo"] = next(r for r in banco_almuerzos if r["nombre"] == sel_a)

            with c_c:
                st.markdown("#### 🥗 Cena")
                idx_sel_c = nombres_c.index(actual_c["nombre"]) if actual_c in banco_cenas else 0
                sel_c = st.selectbox(f"Seleccionar Cena ({dia})", nombres_c, index=idx_sel_c, key=f"s_c_{dia}")
                st.session_state.menu_semanal[dia]["Cena"] = next(r for r in banco_cenas if r["nombre"] == sel_c)

    # ADAPTACIÓN AUTOMÁTICA DE PORCIONES SEGÚN PERFIL
    st.markdown("---")
    st.subheader("🔍 Desglose Adaptado por Integrante de la Familia (Día: Lunes)")
    if st.session_state.profiles:
        for p in st.session_state.profiles:
            st.markdown(f"**🍽️ Adaptación del Menú para {p['nombre']} ({p['targets']['calorias']} kcal objetivo):**")
            ratio = p['targets']['calorias'] / 2000.0
            
            menu_l = st.session_state.menu_semanal["Lunes"]
            for tiempo, plato in menu_l.items():
                if plato:
                    st.write(f"- **{tiempo}:** {plato['nombre']}")
                    ing_adaptados = [f"{ing}: {round(float(cant.replace('g','').replace('ml','').replace('ud','1')) * ratio, 1)}g" for ing, cant in plato['ingredientes'].items()]
                    st.caption(f"  *Cantidades adaptadas:* {', '.join(ing_adaptados)}")

# =============================================================================
# TAB 3: BANCO DE RECETAS ORGANIZADO
# =============================================================================
with tabs[2]:
    st.subheader("📖 Banco Oficial de Recetas")
    tab_rec_d, tab_rec_a, tab_rec_c = st.tabs(["☕ Desayunos (5)", "🍲 Almuerzos (20)", "🥗 Cenas (15)"])

    def mostrar_lista_recetas(lista):
        for r in lista:
            with st.expander(f"📌 {r['nombre']}"):
                st.write("**🛒 Ingredientes Detallados:**")
                for ing, cant in r['ingredientes'].items():
                    st.write(f"- {ing}: **{cant}**")
                
                st.write("**👨‍🍳 Pasos de Elaboración:**")
                for p in r['pasos']: st.write(p)
                
                st.write("**📹 Vídeo de la Receta (< 1 min):**")
                st.video(r['video_receta'])
                
                st.write("**🍱 Consejo de Batch Cooking:**")
                st.info(r['batch_advice'])
                
                st.write("**📹 Vídeo Consejos Batch Cooking (< 1 min):**")
                st.video(r['video_batch'])

    with tab_rec_d: mostrar_lista_recetas(banco_desayunos)
    with tab_rec_a: mostrar_lista_recetas(banco_almuerzos)
    with tab_rec_c: mostrar_lista_recetas(banco_cenas)

# =============================================================================
# TAB 4: BATCH COOKING
# =============================================================================
with tabs[3]:
    st.subheader("🍱 Resumen de Batch Cooking Semanal")
    platos_usados = []
    for d, comidas in st.session_state.menu_semanal.items():
        for c, plato in comidas.items():
            if plato and plato not in platos_usados:
                platos_usados.append(plato)
                
    for p in platos_usados:
        st.markdown(f"### {p['nombre']}")
        col_v1, col_v2 = st.columns([2, 1])
        with col_v1:
            st.write(f"👉 **Estrategia de conservación:** {p['batch_advice']}")
        with col_v2:
            st.video(p['video_batch'])
        st.markdown("---")

# =============================================================================
# TAB 5: LISTA DE LA COMPRA INTERACTIVA
# =============================================================================
with tabs[4]:
    st.subheader("🛒 Lista de la Compra Mensual Categorizada")
    
    secciones_super = {
        "🥬 Frutería y Verdulería": ["Arándanos frescos (300g)", "Tomates de huerta (2kg)", "Espinacas baby (500g)", "Calabaza (1kg)", "Aguacates (6 uds)"],
        "🥩 Frescos y Proteínas": ["Lomos de salmón (600g)", "Pechuga de pollo (1kg)", "Lomo de merluza (600g)", "Tofu firme (400g)", "Huevos camperos (24 uds)"],
        "🌾 Despensa y Cereales": ["Copos de avena (1kg)", "Pan 100% integral (2 barras)", "Quinoa real (500g)", "Garbanzos cocidos (800g)"],
        "🥛 Lácteos y Alternativas": ["Yogur griego (1kg)", "Bebida vegetal / Leche (4L)", "Quesitos ligeros (1 caja)"]
    }

    totales = sum(len(v) for v in secciones_super.values())
    marcados = 0

    for sec, items in secciones_super.items():
        st.markdown(f"#### {sec}")
        c1, c2 = st.columns(2)
        for idx, item in enumerate(items):
            col = c1 if idx % 2 == 0 else c2
            key_k = f"chk_super_{item}"
            val = col.checkbox(item, value=st.session_state.checklist_compra.get(key_k, False))
            st.session_state.checklist_compra[key_k] = val
            if val: marcados += 1

    st.progress(marcados / totales if totales > 0 else 0)
    st.write(f"**Progreso de compra:** {marcados} de {totales} productos comprados.")
    
    txt_export = "LISTA DE LA COMPRA:\n" + "\n".join([f"- {i}" for sub in secciones_super.values() for i in sub])
    st.download_button("📥 Descargar Lista de la Compra (.txt)", txt_export, file_name="lista_compra.txt")

# =============================================================================
# TAB 6: COMUNIDAD
# =============================================================================
with tabs[5]:
    st.subheader("👨‍🍳 Recetas de la Comunidad")
    for r in st.session_state.comunidad_recetas:
        with st.expander(f"⭐ {r['nombre']} (por {r['autor']})"):
            st.write(f"**Pasos:** {r['pasos']}")
            st.info(f"💡 **Batch Cooking:** {r['batch_advice']}")

# =============================================================================
# TAB 7: PAUTAS CIENTÍFICAS
# =============================================================================
with tabs[6]:
    st.subheader("🧠 Evidencia Científica e Institucional")
    st.write("Nuestros menús siguen las pautas del **Plato de Harvard**, la **OMS** y la **EFSA** para garantizar un reparto adecuado de nutrientes de cercanía.")

# -----------------------------------------------------------------------------
# ADVERTENCIA SANITARIA
# -----------------------------------------------------------------------------
st.markdown("""
<div class="footer-warning">
    ⚠️ <strong>AVISO LEGAL Y SANITARIO:</strong> Esta aplicación ofrece orientación nutricional basada en pautas científicas generales. No constituye un diagnóstico médico ni sustituye la consulta con un dietista-nutricionista colegiado.
</div>
""", unsafe_allow_html=True)
