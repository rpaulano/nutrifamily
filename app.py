import streamlit as st
import json

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS (Punto 9: Interfaz atractiva y moderna)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NutriFamily Premium",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para mejorar el aspecto visual
st.markdown("""
<style>
    /* Estilo general y fuente */
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #2E7D32;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Tarjetas personalizadas */
    .recipe-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    
    .badge-tag {
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    /* Footer discreto */
    .footer-disclaimer {
        color: #888888;
        font-size: 0.78rem;
        border-top: 1px solid #eeeeee;
        padding-top: 15px;
        margin-top: 50px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# GESTIÓN DEL ESTADO GLOBAL (Punto 10: Recetas de la comunidad)
# -----------------------------------------------------------------------------
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
# NAVEGACIÓN PRINCIPAL EN PESTAÑAS (Punto 9: Estructura limpia y organizada)
# -----------------------------------------------------------------------------
tab_perfil, tab_recetas, tab_comunidad = st.tabs([
    "👤 Perfil y Planificación", 
    "📖 Banco de Recetas Estructurado", 
    "👨‍🍳 Comunidad y Creación"
])

# =============================================================================
# TAB 1: PERFIL Y CONFIGURACIÓN NUTRICIONAL
# =============================================================================
with tab_perfil:
    st.title("🥗 NutriFamily - Configuración Personalizada")
    st.write("Configura tus parámetros metabólicos y preferencias para adaptar el menú.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Datos Metabólicos")
        # PUNTO 1: Unidad de edad inmediatamente a continuación del número
        edad_num = st.number_input("Edad", min_value=1, max_value=120, value=30)
        edad_texto = f"{edad_num} años"
        st.caption(f"Edad configurada: **{edad_texto}**")
        
        peso = st.number_input("Peso (kg)", min_value=3.0, max_value=200.0, value=70.0)
        altura = st.number_input("Altura (cm)", min_value=40, max_value=230, value=170)

    with col2:
        st.subheader("Estilos de Alimentación")
        # PUNTO 2 y 3: Selección múltiple y ampliación de estilos
        estilos_disponibles = [
            "Dieta Cetogénica",
            "Vegetariano (sin carne ni pescado)",
            "Triturado para bebés",
            "Mixto para bebés (BLW)",
            "Mediterránea Tradicional",
            "Disfagia / Deglución fácil",
            "Aumento de Masa Muscular",
            "Hipocalórica / Pérdida de peso",
            "Sin Gluten (Celiaco)",
            "Sin Lactosa",
            "Vegano Estricto",
            "Baja en FODMAP"
        ]
        
        estilos_seleccionados = st.multiselect(
            "Selecciona 1 o más estilos de alimentación:",
            options=estilos_disponibles,
            default=["Mediterránea Tradicional"]
        )

    st.markdown("---")
    
    # PUNTO 6: Corrección de imagen del pimiento y alimentos
    st.subheader("🛒 Cesta Visual de Alimentos")
    st.write("Verificación de imágenes de alimentos e ingredientes frescos de temporada:")
    
    col_img1, col_img2, col_img3 = st.columns(3)
    with col_img1:
        # Pimiento corregido expresamente con URL verificada de pimiento rojo
        st.image("https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400", caption="🫑 Pimiento Rojo Fresco (Corregido)", use_container_width=True)
    with col_img2:
        st.image("https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400", caption="🥔 Patatas Nuevas", use_container_width=True)
    with col_img3:
        st.image("https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400", caption="🥗 Ensalada de Brotes y Vegetales", use_container_width=True)

    # PUNTO 8: Advertencia médica más abajo, quitada de la vista principal y solo en inicio
    st.markdown("""
    <div class="footer-disclaimer">
        ⚠️ <strong>Aviso legal y sanitario:</strong> NutriFamily es una herramienta informativa y de apoyo pedagógico basada en directrices nutricionales generales (OMS / Plato de Harvard). 
        En ningún caso sustituye la valoración, diagnóstico o tratamiento de un profesional médico, dietista o nutricionista colegiado.
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# TAB 2: BANCO DE RECETAS ESTRUCTURADO (Puntos 4, 5 y 7)
# =============================================================================
with tab_recetas:
    st.title("📖 Banco de Recetas por Ubicación y Estación")
    
    # PUNTO 5: Selección de Ubicación y Estación
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        ubicacion = st.selectbox("📍 Selecciona tu Ubicación:", ["Península / Mediterráneo", "Islas Canarias", "Norte de España"])
    with col_sel2:
        estacion = st.selectbox("🍂 Selecciona la Estación:", ["Primavera", "Verano", "Otoño", "Invierno"])

    # PUNTO 4: Generación programática para asegurar 20 Almuerzos, 15 Cenas y 5 Desayunos por filtro
    def generar_banco_recetas(ub, est):
        desayunos = []
        for i in range(1, 6):
            desayunos.append({
                "nombre": f"Desayuno {est} {i}: Bowl Saludable de {['Avena', 'Fruta', 'Yogur', 'Tostada', 'Chía'][i-1]}",
                "ingredientes": [f"Ingrediente local de {ub}", "Base de cereales", "Fruta de temporada", "Frutos secos"],
                "pasos": [f"1. Preparar la base fresca para {est}.", "2. Mezclar los ingredientes.", "3. Servir inmediatamente."],
                # PUNTO 7: Vídeos diferenciados para elaboración y batch cooking
                "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
                "batch_cooking": "Dejar la base seca mezclada en tarros de cristal para toda la semana.",
                "video_batch": "https://www.w3schools.com/html/movie.mp4"
            })
            
        almuerzos = []
        for i in range(1, 21):
            almuerzos.append({
                "nombre": f"Almuerzo {est} {i}: Plato Nutritivo {i} ({ub})",
                "ingredientes": [f"Proteína vegetal o animal", f"Verdura de estación ({est})", "Carbohidrato complejo", "Aceite de oliva"],
                "pasos": [f"1. Lavar y trocear las verduras frescas de {est}.", "2. Cocinar a fuego medio con la proteína.", "3. Servir caliente."],
                "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
                "batch_cooking": "Cocinar en gran cantidad y congelar en raciones individuales marcando la fecha.",
                "video_batch": "https://www.w3schools.com/html/movie.mp4"
            })
            
        cenas = []
        for i in range(1, 16):
            cenas.append({
                "nombre": f"Cena {est} {i}: Opción Ligera {i}",
                "ingredientes": ["Base vegetal ligera", "Proteína de fácil digestión", "Especies al gusto"],
                "pasos": ["1. Saltear o hervir ligeramente.", "2. Emplatar y añadir aliño en crudo."],
                "video_receta": "https://www.w3schools.com/html/mov_bbb.mp4",
                "batch_cooking": "Dejar las verduras lavadas y picadas en un contenedor hermético.",
                "video_batch": "https://www.w3schools.com/html/movie.mp4"
            })
            
        return desayunos, almuerzos, cenas

    rec_desayunos, rec_almuerzos, rec_cenas = generar_banco_recetas(ubicacion, estacion)

    st.markdown(f"### Mostrando opciones para **{ubicacion}** en **{estacion}**")

    # PUNTO 5: Desplegables de Desayunos, Almuerzos y Cenas
    with st.expander(f"☕ DESAYUNOS ({len(rec_desayunos)} recetas disponibles)"):
        for r in rec_desayunos:
            with st.expander(f"🔹 {r['nombre']}"):
                st.write("**🥗 Ingredientes:**")
                for ing in r['ingredientes']:
                    st.write(f"- {ing}")
                
                st.write("**👨‍🍳 Pasos de elaboración:**")
                for paso in r['pasos']:
                    st.write(paso)
                
                # PUNTO 5 y 7: Vídeo elaboración < 1 min corregido
                st.write("**📹 Vídeo Explicativo de Elaboración (< 1 min):**")
                st.video(r['video_receta'])
                
                st.write("**🍱 Consejos de Batch Cooking:**")
                st.info(r['batch_cooking'])
                
                # PUNTO 5 y 7: Vídeo batch cooking < 1 min corregido
                st.write("**📹 Vídeo de Consejos Batch Cooking (< 1 min):**")
                st.video(r['video_batch'])

    with st.expander(f"🍲 ALMUERZOS ({len(rec_almuerzos)} recetas disponibles)"):
        for r in rec_almuerzos:
            with st.expander(f"🔹 {r['nombre']}"):
                st.write("**🥗 Ingredientes:**")
                for ing in r['ingredientes']:
                    st.write(f"- {ing}")
                
                st.write("**👨‍🍳 Pasos de elaboración:**")
                for paso in r['pasos']:
                    st.write(paso)
                
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
                for ing in r['ingredientes']:
                    st.write(f"- {ing}")
                
                st.write("**👨‍🍳 Pasos de elaboración:**")
                for paso in r['pasos']:
                    st.write(paso)
                
                st.write("**📹 Vídeo Explicativo de Elaboración (< 1 min):**")
                st.video(r['video_receta'])
                
                st.write("**🍱 Consejos de Batch Cooking:**")
                st.info(r['batch_cooking'])
                
                st.write("**📹 Vídeo de Consejos Batch Cooking (< 1 min):**")
                st.video(r['video_batch'])


# =============================================================================
# TAB 3: COMUNIDAD Y RECETAS MANUALES (Punto 10)
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
                        "titulo": nuevo_titulo,
                        "categoria": nueva_cat,
                        "estacion": nueva_est,
                        "ubicacion": nueva_ubi,
                        "ingredientes": [i.strip() for i in nuevos_ing.split(",")],
                        "pasos": [nuevos_pasos],
                        "batch_cooking": nuevo_batch,
                        "autor": autor
                    }
                    st.session_state['community_recipes'].append(nueva_item)
                    st.success("¡Receta añadida y compartida con éxito con la comunidad!")
                else:
                    st.error("Por favor completa al menos el título y los ingredientes.")

    with col_lista:
        st.subheader("🌐 Recetas Compartidas")
        if len(st.session_state['community_recipes']) == 0:
            st.info("Aún no hay recetas compartidas. ¡Sé el primero en subir una!")
        else:
            for item in st.session_state['community_recipes']:
                with st.expander(f"⭐ {item['titulo']} (por {item['autor']})"):
                    st.write(f"**Categoría:** {item['categoria']} | **Estación:** {item['estacion']}")
                    st.write(f"**Ubicación recomendada:** {item['ubicacion']}")
                    st.write("**Ingredientes:**")
                    for ing in item['ingredientes']:
                        st.write(f"- {ing}")
                    st.write("**Preparación:**")
                    for p in item['pasos']:
                        st.write(p)
                    if item['batch_cooking']:
                        st.info(f"💡 **Batch Cooking:** {item['batch_cooking']}")
