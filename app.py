import streamlit as st
import pandas as pd
import json
import random

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NutriFamily Premium",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #2E7D32; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .footer-disclaimer {
        color: #888888; font-size: 0.78rem; border-top: 1px solid #eeeeee;
        padding-top: 15px; margin-top: 50px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ESTADO DE LA SESIÓN (Restaurado: Cuentas Compartidas y Múltiples Perfiles)
# -----------------------------------------------------------------------------
if 'cuenta_id' not in st.session_state:
    st.session_state.cuenta_id = "FAMILIA-DEMO-2026"
if 'profiles' not in st.session_state:
    st.session_state.profiles = []
if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {dia: {"Desayuno": None, "Comida": None, "Cena": None} for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]}
if 'checklist_compra' not in st.session_state:
    st.session_state.checklist_compra = {}
if 'community_recipes' not in st.session_state:
    st.session_state['community_recipes'] = [
        {
            "titulo": "Crema Suave de Calabacín y Quesitos",
            "categoria": "Cenas",
            "estacion": "Primavera",
            "ubicacion": "Península / Mediterráneo",
            "ingredientes": ["2 calabacines grandes", "1 patata", "4 quesitos", "Aceite de oliva", "Sal"],
            "pasos": ["Cocer calabacín y patata 15 min.", "Añadir quesitos y batir bien hasta dejar fino."],
            "batch_cooking": "Aguanta 4 días en cristal. Triturar de nuevo al calentar.",
            "autor": "María G."
        }
    ]

# -----------------------------------------------------------------------------
# BARRA LATERAL: VINCULAR USUARIOS Y CUENTA COMPARTIDA
# -----------------------------------------------------------------------------
st.sidebar.title("👥 Mi Cuenta Compartida")
codigo_sync = st.sidebar.text_input("Código de Familia / Cuenta", value=st.session_state.cuenta_id)
if st.sidebar.button("🔄 Sincronizar Cambios"):
    st.session_state.cuenta_id = codigo_sync
    st.sidebar.success(f"Conectado a la cuenta compartida: {codigo_sync}")

st.sidebar.markdown("---")

# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES PARA COMPRA Y CATEGORIZACIÓN
# -----------------------------------------------------------------------------
def clasificar_ingrediente(ingrediente):
    ing = ingrediente.lower()
    if any(k in ing for k in ["manzana", "plátano", "fruta", "frutos rojos", "aguacate", "espinaca", "verdura", "pimiento", "zanahoria", "calabacín", "tomate", "lechuga", "patata", "boniato", "alcachofa", "setas", "brócoli", "guisante"]):
        return "🥬 Frutería y Verdulería"
    elif any(k in ing for k in ["pollo", "pavo", "ternera", "pescado", "salmon", "salmón", "atún", "bacalao", "merluza", "huevo", "tofu", "seitan", "heura", "gambas", "sepia", "jamón"]):
        return "🥩 Frescos y Proteínas"
    elif any(k in ing for k in ["leche", "yogur", "queso", "mantequilla", "requesón", "bebida vegetal"]):
        return "🥛 Lácteos y Alternativas"
    elif any(k in ing for k in ["avena", "pan", "arroz", "pasta", "lenteja", "garbanzo", "alubia", "quinoa", "cuscús", "noodles", "harina"]):
        return "🌾 Despensa y Cereales"
    else:
        return "🧂 Aceites, Especias y Varios"

def generar_lista_compra_dict():
    num_integrantes = max(1, len(st.session_state.profiles))
    lista_compra = {}
    for dia, comidas in st.session_state.menu_semanal.items():
        for tipo in ["Desayuno", "Comida", "Cena"]:
            plato = comidas[tipo]
            if plato:
                for ing in plato.get("ingredientes", []):
                    # Extraer o asignar cantidad base estimada por comensal
                    lista_compra[ing] = lista_compra.get(ing, 0) + (100 * num_integrantes)
    return lista_compra

# -----------------------------------------------------------------------------
# NAVEGACIÓN EN PESTAÑAS
# -----------------------------------------------------------------------------
tab_perfil, tab_recetas, tab_compra, tab_comunidad = st.tabs([
    "👥 Perfiles y Familia", 
    "📖 Banco de Recetas", 
    "🛒 Lista de la Compra", 
    "👨‍🍳 Comunidad"
])

# =============================================================================
# TAB 1: GESTIÓN DE VARIOS PERFILES FAMILIARES
# =============================================================================
with tab_perfil:
    st.title("👥 Gestión de Perfiles Familiares")
    st.write("Añade los perfiles de tu familia para adaptar las cantidades de las recetas.")
    
    with st.form("nuevo_perfil_familiar"):
        c1, c2, c3 = st.columns([2, 1, 1])
        nombre = c1.text_input("Nombre del familiar")
        edad_num = c2.number_input("Edad", min_value=1, max_value=120, value=30)
        unidad_edad = c3.selectbox("Unidad", ["Años", "Meses"])
        edad_texto = f"{edad_num} {unidad_edad.lower()}"
        
        peso = st.number_input("Peso (kg)", min_value=3.0, max_value=200.0, value=70.0)
        
        estilos_disponibles = [
            "Mediterránea Tradicional", "Dieta Cetogénica", "Vegetariano (sin carne ni pescado)",
            "Triturado para bebés", "Mixto para bebés (BLW)", "Disfagia / Deglución fácil",
            "Aumento de Masa Muscular", "Hipocalórica / Pérdida de peso", "Sin Gluten (Celiaco)",
            "Sin Lactosa", "Vegano Estricto", "Baja en FODMAP"
        ]
        
        estilos_sel = st.multiselect("Selecciona 1 o más estilos de alimentación:", estilos_disponibles, default=["Mediterránea Tradicional"])
        alergias = st.text_input("Alergias o Intolerancias", placeholder="Ej: Gluten, Lactosa...")
        
        if st.form_submit_button("➕ Añadir Perfil a la Cuenta") and nombre:
            st.session_state.profiles.append({
                "nombre": nombre, "edad": edad_texto, "peso": peso,
                "estilos": estilos_sel, "alergias": alergias if alergias else "Ninguna"
            })
            st.success(f"Perfil de {nombre} ({edad_texto}) añadido correctamente.")

    if st.session_state.profiles:
        st.subheader("Familiares Registrados")
        df_profiles = pd.DataFrame([
            {
                "Nombre": p["nombre"],
                "Edad": p["edad"],
                "Peso (kg)": p["peso"],
                "Estilos": ", ".join(p["estilos"]),
                "Alergias": p["alergias"]
            } for p in st.session_state.profiles
        ])
        st.dataframe(df_profiles, use_container_width=True)

    st.markdown("---")
    st.subheader("🛒 Galería de Alimentos Frescos de Temporada")
    col_img1, col_img2, col_img3 = st.columns(3)
    with col_img1:
        st.image("https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400", caption="🫑 Pimiento Rojo Fresco", use_container_width=True)
    with col_img2:
        st.image("https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400", caption="🥔 Patatas Nuevas", use_container_width=True)
    with col_img3:
        st.image("https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400", caption="🥗 Ensalada de Brotes y Vegetales", use_container_width=True)

    st.markdown("""
    <div class="footer-disclaimer">
        ⚠️ <strong>Aviso legal y sanitario:</strong> NutriFamily es una herramienta informativa y de apoyo pedagógico basada en directrices nutricionales generales (OMS / Plato de Harvard). 
        En ningún caso sustituye la valoración, diagnóstico o tratamiento de un profesional médico, dietista o nutricionista colegiado.
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# TAB 2: BANCO DE RECETAS ESTRUCTURADO Y VÍDEOS
# =============================================================================
with tab_recetas:
    st.title("📖 Banco de Recetas por Ubicación y Estación")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        ubicacion = st.selectbox("📍 Selecciona tu Ubicación:", ["Península / Mediterráneo", "Islas Canarias", "Norte de España"])
    with col_sel2:
        estacion = st.selectbox("🍂 Selecciona la Estación:", ["Primavera", "Verano", "Otoño", "Invierno"])

    def generar_banco_recetas(ub, est):
        desayunos = []
        for i in range(1, 6):
            desayunos.append({
                "nombre": f"Desayuno {est} {i}: Bowl Saludable de {['Avena', 'Fruta', 'Yogur', 'Tostada', 'Chía'][i-1]}",
                "ingredientes": [f"Ingrediente local de {ub}", "Avena", "Manzana", "Frutos secos"],
                "pasos": [f"1. Preparar la base fresca para {est}.", "2. Mezclar los ingredientes.", "3. Servir inmediatamente."],
                "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
                "batch_cooking": "Dejar la base seca mezclada en tarros de cristal para toda la semana.",
                "video_batch": "https://www.w3schools.com/html/movie.mp4"
            })
            
        almuerzos = []
        for i in range(1, 21):
            almuerzos.append({
                "nombre": f"Almuerzo {est} {i}: Plato Nutritivo {i} ({ub})",
                "ingredientes": ["Pollo", f"Zanahoria de estación ({est})", "Arroz integral", "Aceite de oliva"],
                "pasos": [f"1. Lavar y trocear las verduras frescas de {est}.", "2. Cocinar a fuego medio con la proteína.", "3. Servir caliente."],
                "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
                "batch_cooking": "Cocinar en gran cantidad y congelar en raciones individuales marcando la fecha.",
                "video_batch": "https://www.w3schools.com/html/movie.mp4"
            })
            
        cenas = []
        for i in range(1, 16):
            cenas.append({
                "nombre": f"Cena {est} {i}: Opción Ligera {i}",
                "ingredientes": ["Espinacas", "Merluza", "Pimiento", "Aceite de oliva"],
                "pasos": ["1. Saltear o hervir ligeramente.", "2. Emplatar y añadir aliño en crudo."],
                "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
                "batch_cooking": "Dejar las verduras lavadas y picadas en un contenedor hermético.",
                "video_batch": "https://www.w3schools.com/html/movie.mp4"
            })
            
        return desayunos, almuerzos, cenas

    rec_desayunos, rec_almuerzos, rec_cenas = generar_banco_recetas(ubicacion, estacion)

    # Asignar menú de ejemplo automáticamente para poder calcular la lista de la compra
    for dia in st.session_state.menu_semanal:
        st.session_state.menu_semanal[dia]["Desayuno"] = rec_desayunos[0]
        st.session_state.menu_semanal[dia]["Comida"] = rec_almuerzos[0]
        st.session_state.menu_semanal[dia]["Cena"] = rec_cenas[0]

    st.markdown(f"### Mostrando opciones para **{ubicacion}** en **{estacion}**")

    with st.expander(f"☕ DESAYUNOS ({len(rec_desayunos)} recetas disponibles)"):
        for r in rec_desayunos:
            with st.expander(f"🔹 {r['nombre']}"):
                st.write("**🥗 Ingredientes:**")
                for ing in r['ingredientes']: st.write(f"- {ing}")
                st.write("**👨‍🍳 Pasos de elaboración:**")
                for paso in r['pasos']: st.write(paso)
                st.write("**📹 Vídeo Explicativo de Elaboración (< 1 min):**")
                st.video(r['video_receta'])
                st.write("**🍱 Consejos de Batch Cooking:**")
                st.info(r['batch_cooking'])
                st.write("**📹 Vídeo de Consejos Batch Cooking (< 1 min):**")
                st.video(r['video_batch'])

    with st.expander(f"🍲 ALMUERZOS ({len(rec_almuerzos)} recetas disponibles)"):
        for r in rec_almuerzos:
            with st.expander(f"🔹 {r['nombre']}"):
                st.write("**🥗 Ingredientes:**")
                for ing in r['ingredientes']: st.write(f"- {ing}")
                st.write("**👨‍🍳 Pasos de elaboración:**")
                for paso in r['pasos']: st.write(paso)
                st.write("**📹 Vídeo Explicativo de Elaboración (< 1 min):**")
                st.video(r['video_receta'])
                st.write("**🍱 Consejos de Batch Cooking:**")
                st.info(r['batch_cooking'])
                st.write("**📹 Vídeo de Consejos Batch Cooking (< 1 min):**")
                st.video(r['video_batch'])

    with st.expander(f"🌙 CENAS ({len(rec_cenas)} recetas disponibles)"):
        for r in rec_cenas:
            with st.expander(f"🔹 {r['nombre']}"):
                st.write("**🥗 Ingredientes:**")
                for ing in r['ingredientes']: st.write(f"- {ing}")
                st.write("**👨‍🍳 Pasos de elaboración:**")
                for paso in r['pasos']: st.write(paso)
                st.write("**📹 Vídeo Explicativo de Elaboración (< 1 min):**")
                st.video(r['video_receta'])
                st.write("**🍱 Consejos de Batch Cooking:**")
                st.info(r['batch_cooking'])
                st.write("**📹 Vídeo de Consejos Batch Cooking (< 1 min):**")
                st.video(r['video_batch'])


# =============================================================================
# TAB 3: LISTA DE LA COMPRA INTERACTIVA Y CATEGORIZADA (Diseño Anterior)
# =============================================================================
with tab_compra:
    st.title("🛒 Lista de la Compra Interactiva y Categorizada")
    
    lista_compra_raw = generar_lista_compra_dict()

    if not lista_compra_raw:
        st.info("Planifica tu menú en el banco de recetas para generar la lista de la compra automáticamente.")
    else:
        secciones = {
            "🥬 Frutería y Verdulería": {},
            "🥩 Frescos y Proteínas": {},
            "🥛 Lácteos y Alternativas": {},
            "🌾 Despensa y Cereales": {},
            "🧂 Aceites, Especias y Varios": {}
        }

        for ing, cant in lista_compra_raw.items():
            cat = clasificar_ingrediente(ing)
            secciones[cat][ing] = cant

        total_items = len(lista_compra_raw)
        marcados = 0

        for ing in lista_compra_raw.keys():
            if st.session_state.get(f"chk_{ing}", False):
                marcados += 1

        progreso = marcados / total_items if total_items > 0 else 0
        st.markdown(f"**Progreso de la compra:** {marcados} de {total_items} productos comprados")
        st.progress(progreso)

        st.markdown("---")

        for sec, items in secciones.items():
            if items:
                st.subheader(sec)
                cols = st.columns(2)
                for idx, (ing, cant) in enumerate(items.items()):
                    col = cols[idx % 2]
                    key_chk = f"chk_{ing}"
                    comprado = col.checkbox(
                        f"**{ing}**: {int(cant)} g/ml", 
                        key=key_chk
                    )
                st.markdown("")


# =============================================================================
# TAB 4: COMUNIDAD Y RECETAS MANUALES
# =============================================================================
with tab_comunidad:
    st.title("👨‍🍳 Recetas de la Comunidad NutriFamily")
    
    col_crear, col_lista = st.columns([1, 1])
    
    with col_crear:
        st.subheader("➕ Crear nueva receta manualmente")
        with st.form("form_nueva_receta"):
            nuevo_titulo = st.text_input("Título de la Receta")
            nueva_cat = st.selectbox("Categoría", ["Desayunos", "Almuerzos", "Cenas"])
            nueva_est = st.selectbox("Estación", ["Primavera", "Verano", "Otoño", "Invierno"])
            nueva_ubi = st.selectbox("Ubicación recomendada", ["Península / Mediterráneo", "Islas Canarias", "Norte de España"])
            nuevos_ing = st.text_area("Ingredientes (separados por comas)")
            nuevos_pasos = st.text_area("Pasos de preparación")
            nuevo_batch = st.text_input("Consejo de Batch Cooking")
            autor = st.text_input("Tu Nombre / Apodo", value="Usuario NutriFamily")
            
            submit_receta = st.form_submit_button("Compartir con la Comunidad")
            
            if submit_receta:
                if nuevo_titulo and nuevos_ing:
                    nueva_item = {
                        "titulo": nuevo_titulo, "categoria": nueva_cat,
                        "estacion": nueva_est, "ubicacion": nueva_ubi,
                        "ingredientes": [i.strip() for i in nuevos_ing.split(",")],
                        "pasos": [nuevos_pasos], "batch_cooking": nuevo_batch, "autor": autor
                    }
                    st.session_state['community_recipes'].append(nueva_item)
                    st.success("¡Receta añadida y compartida con éxito!")
                else:
                    st.error("Por favor completa el título y los ingredientes.")

    with col_lista:
        st.subheader("🌐 Recetas Compartidas")
        for item in st.session_state['community_recipes']:
            with st.expander(f"⭐ {item['titulo']} (por {item['autor']})"):
                st.write(f"**Categoría:** {item['categoria']} | **Estación:** {item['estacion']}")
                st.write(f"**Ubicación:** {item['ubicacion']}")
                st.write("**Ingredientes:**")
                for ing in item['ingredientes']: st.write(f"- {ing}")
                st.write("**Preparación:**")
                for p in item['pasos']: st.write(p)
                if item['batch_cooking']: st.info(f"💡 **Batch Cooking:** {item['batch_cooking']}")
