import streamlit as st
import pandas as pd
import json
import random

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN Y ESTADO DE LA SESIÓN
# -----------------------------------------------------------------------------
st.set_page_config(page_title="NutriFamily Planner", layout="wide", page_icon="🥗")

RDA_BASELINE = {
    "Adulto": {"calorias": 2000, "proteinas": 60, "carbos": 250, "grasas": 70, "hierro": 14, "calcio": 1000},
    "Niño (3-12)": {"calorias": 1500, "proteinas": 35, "carbos": 190, "grasas": 50, "hierro": 10, "calcio": 800},
    "Bebé (BLW)": {"calorias": 850, "proteinas": 20, "carbos": 100, "grasas": 35, "hierro": 11, "calcio": 260}
}

if 'profiles' not in st.session_state:
    st.session_state.profiles = []
if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {dia: {"Desayuno": None, "Comida": None, "Cena": None} for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]}

# -----------------------------------------------------------------------------
# GENERADOR DEL BANCO DE RECETAS
# -----------------------------------------------------------------------------
def generar_recetario():
    recetas = []
    
    # 5 DESAYUNOS
    desayunos_base = [
        ("Tostadas integrales con aguacate y huevo cocido", {"Pan integral": 60, "Aguacate": 50, "Huevo": 60, "Aceite de oliva": 5}),
        ("Porridge de avena con plátano y canela", {"Avena": 50, "Leche o Bebida Vegetal": 200, "Plátano": 100, "Canela": 2}),
        ("Yogur natural con frutos rojos y semillas de chía", {"Yogur natural": 150, "Frutos rojos": 80, "Semillas de chía": 10}),
        ("Pancakes de avena y plátano a la plancha", {"Avena": 40, "Plátano": 100, "Huevo": 60, "Leche": 50}),
        ("Batido verde proteico con espinacas y manzana", {"Espinacas frescas": 50, "Manzana": 100, "Bebida vegetal": 200, "Proteína en polvo o chía": 15})
    ]
    for i, (nombre, ing) in enumerate(desayunos_base, 1):
        recetas.append({
            "id": i, "nombre": f"Desayuno {i}: {nombre}", "categoria": "Desayunos",
            "ingredientes_base": ing,
            "nutrientes_base": {"calorias": 320 + (i*10), "proteinas": 12, "carbos": 45, "grasas": 10, "hierro": 3, "calcio": 180},
            "instrucciones": "Preparar los ingredientes al momento o triturar/cocinar según corresponda.",
            "adaptaciones": {"Estándar": "Opción rápida y nutritiva.", "Vegetariano/Vegano": "Usar alternativa vegetal sin lactosa/huevo.", "BLW": "Ofrecer la fruta en cortes de seguridad."},
            "batch_cooking": "Puedes dejar los ingredientes secos listos la noche anterior."
        })
        
    # 30 COMIDAS
    comidas_base = [
        "Lentejas estofadas con verduras", "Garbanzos con espinacas y comino", "Pollo al horno con patatas",
        "Salmón a la plancha con espárragos", "Pasta integral con boloñesa de lentejas", "Arroz integral con verduras y tofu",
        "Guiso de patatas con bacalao", "Ensalada de quinoa con garbanzos y pimientos", "Pavo a la plancha con boniato",
        "Merluza al vapor con zanahoria y guisantes", "Hamburguesa de alubias negras con verduras", "Cuscús con verduras asadas y garbanzos",
        "Risotto de setas y champiñones", "Fajitas de pollo y pimientos salteados", "Alubias blancas estofadas con calabaza",
        "Lomos de atún con pisto de verduras", "Estofado de ternera con verduras de raíz", "Noodles de arroz con verduras y cacahuete",
        "Crema de calabacín con pollo desmenuzado", "Pastel de carne y puré de patata", " Albóndigas de pavo en salsa de tomate",
        "Paella de verduras de temporada", "Ternera salteada con brócoli y sésamo", "Lasaña vegetal con capas de calabacín",
        "Garbanzos al curry con leche de coco", "Tofu marinado con salteado de judías verdes", "Sepia a la plancha con ensalada verde",
        "Canelones de espinacas y requesón", "Conejo guisado con alcachofas", "Lentejas rojas al curry suave"
    ]
    for i, nom in enumerate(comidas_base, 6):
        recetas.append({
            "id": i, "nombre": f"Almuerzo {i-5}: {nom}", "categoria": "Comidas",
            "ingredientes_base": {f"Ingrediente principal ({nom.split()[0]})": 130, "Verduras variadas": 150, "Aceite de Oliva": 12},
            "nutrientes_base": {"calorias": 520 + (i*2), "proteinas": 28, "carbos": 55, "grasas": 16, "hierro": 5, "calcio": 90},
            "instrucciones": "Cocinar la base principal y saltear las verduras a fuego medio.",
            "adaptaciones": {"Estándar": "Receta completa.", "Vegetariano/Vegano": "Sustituir la proteína animal por legumbres o tofu.", "BLW": "Adaptar textura y tamaño de corte."},
            "batch_cooking": "Dejar la base cocida en un recipiente hermético en el frigorífico."
        })

    # 20 CENAS
    cenas_base = [
        "Crema de calabaza con semillas de calabaza", "Tortilla de espinacas y ensalada de tomate", "Pescado blanco al papillote con verduras",
        "Revuelto de setas y gambas", "Hamburguesa de salmón casera con ensalada", "Sopa de picadillo ligera con huevo duro",
        "Salteado de calabacín, pimiento y tofu", "Ensalada templada de gulas y setas", "Crema de verduras variadas y queso fresco",
        "Huevos escalfados sobre cama de verduras", "Sardinas a la plancha con picadillo de pimiento", "Pisto de verduras con huevo a la plancha",
        "Cogollos de lechuga con atún y frutos secos", "Brochetas de pavo y pimientos al horno", "Tacos de lechuga con relleno vegetal y aguacate",
        "Wok de verduras variadas con tiras de pollo", "Tartar de tomate y aguacate con tostadas", "Verduras asadas a la parrilla con hummus",
        "Wrap integral de queso fresco y espinacas", "Crema de espárragos verdes con virutas de jamón"
    ]
    for i, nom in enumerate(cenas_base, 36):
        recetas.append({
            "id": i, "nombre": f"Cena {i-35}: {nom}", "categoria": "Cenas",
            "ingredientes_base": {f"Base principal cena": 100, "Verduras ligeras": 160, "Aceite de Oliva": 10},
            "nutrientes_base": {"calorias": 360 + i, "proteinas": 22, "carbos": 22, "grasas": 14, "hierro": 3, "calcio": 85},
            "instrucciones": "Cocinado rápido al vapor, plancha o triturado fino para una cena ligera.",
            "adaptaciones": {"Estándar": "Sazonar al gusto.", "Vegetariano/Vegano": "Opción con proteína vegetal suave.", "BLW": "Servir en consistencia suave o bastones blandos."},
            "batch_cooking": "Tener las verduras troceadas en el congelador o recipientes de cristal."
        })
        
    return recetas

if 'recipes' not in st.session_state:
    st.session_state.recipes = generar_recetario()

# -----------------------------------------------------------------------------
# 2. FUNCIONES AUXILIARES
# -----------------------------------------------------------------------------
def obtener_rda(perfil):
    edad = perfil['edad']
    unidad = perfil['unidad_edad']
    if perfil['estilo'] == 'BLW para bebés' or (unidad == "Meses" and edad <= 24) or (unidad == "Años" and edad <= 2):
        return RDA_BASELINE["Bebé (BLW)"]
    elif unidad == "Años" and edad < 18:
        return RDA_BASELINE["Niño (3-12)"]
    else:
        return RDA_BASELINE["Adulto"]

def calcular_nutrientes_dia(dia, perfil):
    totales = {"calorias": 0, "proteinas": 0, "carbos": 0, "grasas": 0, "hierro": 0, "calcio": 0}
    unidad = perfil['unidad_edad']
    edad = perfil['edad']
    if unidad == "Meses" or (unidad == "Años" and edad <= 2): factor = 0.4
    elif unidad == "Años" and edad < 12: factor = 0.7
    else: factor = 1.0

    for comida in ["Desayuno", "Comida", "Cena"]:
        plato = st.session_state.menu_semanal[dia][comida]
        if plato:
            for k in totales:
                totales[k] += plato["nutrientes_base"][k] * factor
    return totales

def generar_aleatorio():
    recetas_des = [r for r in st.session_state.recipes if r["categoria"] == "Desayunos"]
    recetas_com = [r for r in st.session_state.recipes if r["categoria"] == "Comidas"]
    recetas_cen = [r for r in st.session_state.recipes if r["categoria"] == "Cenas"]
    for dia in st.session_state.menu_semanal:
        st.session_state.menu_semanal[dia]["Desayuno"] = random.choice(recetas_des)
        st.session_state.menu_semanal[dia]["Comida"] = random.choice(recetas_com)
        st.session_state.menu_semanal[dia]["Cena"] = random.choice(recetas_cen)

def generar_lista_compra_dict():
    num_integrantes = max(1, len(st.session_state.profiles))
    lista_compra = {}
    for dia, comidas in st.session_state.menu_semanal.items():
        for tipo in ["Desayuno", "Comida", "Cena"]:
            plato = comidas[tipo]
            if plato:
                for ing, cant in plato["ingredientes_base"].items():
                    lista_compra[ing] = lista_compra.get(ing, 0) + (cant * num_integrantes)
    return lista_compra

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

# -----------------------------------------------------------------------------
# 3. INTERFAZ DE USUARIO (BARRA LATERAL)
# -----------------------------------------------------------------------------
st.sidebar.title("🥗 NutriFamily")
menu_opcion = st.sidebar.radio("Navegación", [
    "👥 Perfiles Familiares", 
    "📅 Planificador de Menú", 
    "📊 Resumen Nutricional", 
    "📖 Banco de Recetas", 
    "🛒 Lista de la Compra", 
    "👨‍🍳 Batch Cooking",
    "💾 Guardar / Exportar Texto"
])

# -----------------------------------------------------------------------------
# SECCIÓN 1: PERFILES FAMILIARES
# -----------------------------------------------------------------------------
if menu_opcion == "👥 Perfiles Familiares":
    st.header("👥 Gestión de Perfiles Familiares")
    st.markdown("Añade a los miembros de la familia.")
    
    with st.form("nuevo_perfil"):
        c1, c2, c3 = st.columns([2, 1, 1])
        nombre = c1.text_input("Nombre del familiar")
        edad = c2.number_input("Edad", min_value=1, max_value=120, value=30)
        unidad_edad = c3.radio("Unidad", ["Años", "Meses"], horizontal=True)
        
        c4, c5 = st.columns([1, 2])
        estilo = c4.selectbox("Estilo", ["Estándar", "Vegetariano", "Vegano", "BLW para bebés"])
        alergias = c5.text_input("Alergias o intolerancias específicas (separar por comas)", placeholder="Ej: gluten, melocotón, frutos rojos, alcachofa...")
        
        if st.form_submit_button("Añadir Perfil") and nombre:
            lista_alergias = [a.strip().capitalize() for a in alergias.split(",")] if alergias else ["Ninguna"]
            st.session_state.profiles.append({
                "nombre": nombre, "edad": edad, "unidad_edad": unidad_edad, 
                "estilo": estilo, "alergias": ", ".join(lista_alergias)
            })
            st.success(f"Perfil de {nombre} guardado exitosamente.")

    if st.session_state.profiles:
        st.dataframe(pd.DataFrame(st.session_state.profiles), use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN 2: PLANIFICADOR DE MENÚ SEMANAL
# -----------------------------------------------------------------------------
elif menu_opcion == "📅 Planificador de Menú":
    st.header("📅 Planificador Semanal Equilibrado")
    
    st.button("🎲 Generar Menú Aleatorio", on_click=generar_aleatorio, type="primary")

    if not st.session_state.profiles:
        st.warning("⚠️ Crea al menos un perfil familiar para ver la cobertura nutricional.")
    else:
        perfil_visor = st.selectbox("🎯 Mostrar adaptación y cobertura nutricional para:", [p["nombre"] for p in st.session_state.profiles])
        perfil_actual = next(p for p in st.session_state.profiles if p["nombre"] == perfil_visor)
        rda = obtener_rda(perfil_actual)

    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    tabs = st.tabs(dias)

    recetas_des = ["-- Seleccionar --"] + [r["nombre"] for r in st.session_state.recipes if r["categoria"] == "Desayunos"]
    recetas_com = ["-- Seleccionar --"] + [r["nombre"] for r in st.session_state.recipes if r["categoria"] == "Comidas"]
    recetas_cen = ["-- Seleccionar --"] + [r["nombre"] for r in st.session_state.recipes if r["categoria"] == "Cenas"]

    for i, dia in enumerate(dias):
        with tabs[i]:
            col_menu, col_nutri = st.columns([2, 1])
            
            with col_menu:
                idx_des = recetas_des.index(st.session_state.menu_semanal[dia]["Desayuno"]["nombre"]) if st.session_state.menu_semanal[dia]["Desayuno"] else 0
                idx_com = recetas_com.index(st.session_state.menu_semanal[dia]["Comida"]["nombre"]) if st.session_state.menu_semanal[dia]["Comida"] else 0
                idx_cen = recetas_cen.index(st.session_state.menu_semanal[dia]["Cena"]["nombre"]) if st.session_state.menu_semanal[dia]["Cena"] else 0
                
                s_des = st.selectbox(f"☕ Desayuno - {dia}", recetas_des, index=idx_des, key=f"d_{dia}")
                s_com = st.selectbox(f"🍲 Comida - {dia}", recetas_com, index=idx_com, key=f"c_{dia}")
                s_cen = st.selectbox(f"🥗 Cena - {dia}", recetas_cen, index=idx_cen, key=f"cn_{dia}")

                if s_des != "-- Seleccionar --": st.session_state.menu_semanal[dia]["Desayuno"] = next(r for r in st.session_state.recipes if r["nombre"] == s_des)
                if s_com != "-- Seleccionar --": st.session_state.menu_semanal[dia]["Comida"] = next(r for r in st.session_state.recipes if r["nombre"] == s_com)
                if s_cen != "-- Seleccionar --": st.session_state.menu_semanal[dia]["Cena"] = next(r for r in st.session_state.recipes if r["nombre"] == s_cen)

            with col_nutri:
                st.markdown(f"**Progreso Diario de {perfil_visor if st.session_state.profiles else 'Usuario'}**")
                if st.session_state.profiles:
                    totales = calcular_nutrientes_dia(dia, perfil_actual)
                    for nut, nombre_mostrar in [("calorias", "Calorías (kcal)"), ("proteinas", "Proteínas (g)"), ("carbos", "Carbohidratos (g)")]:
                        valor = totales[nut]
                        objetivo = rda[nut]
                        pct = min(100, int((valor / objetivo) * 100))
                        st.caption(f"{nombre_mostrar}: {int(valor)} / {objetivo}")
                        st.progress(pct / 100.0)
                else:
                    st.info("Añade un perfil para ver el progreso diario.")

# -----------------------------------------------------------------------------
# SECCIÓN 3: CONTADOR Y COMPARATIVA NUTRICIONAL
# -----------------------------------------------------------------------------
elif menu_opcion == "📊 Resumen Nutricional":
    st.header("📊 Comparativa Semanal Intuitiva")
    
    if not st.session_state.profiles:
        st.warning("Agrega perfiles familiares primero.")
    else:
        perfil_sel = st.selectbox("Seleccionar Familiar", [p["nombre"] for p in st.session_state.profiles])
        perfil = next(p for p in st.session_state.profiles if p["nombre"] == perfil_sel)
        rda = obtener_rda(perfil)
        
        totales = {"calorias": 0, "proteinas": 0, "carbos": 0, "grasas": 0, "hierro": 0, "calcio": 0}
        dias_con_menu = 0
        
        for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]:
            t_dia = calcular_nutrientes_dia(dia, perfil)
            if t_dia["calorias"] > 0:
                dias_con_menu += 1
                for k in totales: totales[k] += t_dia[k]

        dias_activos = max(1, dias_con_menu)
        st.markdown(f"### Cumplimiento Medio Diario (basado en {dias_con_menu} días programados)")
        
        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]
        metricas = [
            ("Calorías", "calorias", "kcal"), ("Proteínas", "proteinas", "g"), ("Carbohidratos", "carbos", "g"), 
            ("Grasas", "grasas", "g"), ("Hierro", "hierro", "mg"), ("Calcio", "calcio", "mg")
        ]
        
        for i, (nombre, clave, unidad) in enumerate(metricas):
            promedio = totales[clave] / dias_activos
            objetivo = rda[clave]
            pct = min(100, int((promedio / objetivo) * 100))
            with cols[i % 3]:
                st.metric(f"{nombre} ({unidad})", f"{int(promedio)}", f"Obj: {objetivo}")
                st.progress(pct / 100.0)
                st.write("")

# -----------------------------------------------------------------------------
# SECCIÓN 4: BANCO DE RECETAS
# -----------------------------------------------------------------------------
elif menu_opcion == "📖 Banco de Recetas":
    st.header("📖 Banco de Recetas y Alta Manual")
    
    tab_ver, tab_crear = st.tabs(["🔍 Consultar Banco", "➕ Añadir Nueva Receta Manualmente"])
    
    with tab_ver:
        filtro = st.radio("Filtrar por categoría:", ["Todas", "Desayunos", "Comidas", "Cenas"], horizontal=True)
        for r in st.session_state.recipes:
            if filtro == "Todas" or r["categoria"] == filtro:
                with st.expander(f"🍽️ {r['nombre']} ({r['categoria']})"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Ingredientes Base (por ración):**")
                        for ing, cant in r['ingredientes_base'].items(): st.write(f"- {ing}: {cant}g/ml")
                        st.markdown("**Instrucciones:**")
                        st.info(r['instrucciones'])
                    with c2:
                        st.markdown("**Adaptaciones:**")
                        st.write(f"🌱 **Vegano/Vegetariano:** {r['adaptaciones']['Vegetariano/Vegano']}")
                        st.write(f"👶 **BLW:** {r['adaptaciones']['BLW']}")
                        st.write(f"👨‍👩‍👧 **Estándar:** {r['adaptaciones']['Estándar']}")

    with tab_crear:
        st.subheader("Formulario de Alta de Receta")
        with st.form("form_nueva_receta"):
            n_nombre = st.text_input("Nombre de la receta")
            n_cat = st.selectbox("Categoría", ["Desayunos", "Comidas", "Cenas"])
            n_inst = st.text_area("Instrucciones paso a paso")
            
            st.markdown("**Ingredientes principales (nombre: cantidad en gramos/ml)**")
            c_ing1, c_cant1 = st.columns(2)
            ing1 = c_ing1.text_input("Ingrediente 1", "Ej: Pechuga de pollo")
            cant1 = c_cant1.number_input("Cantidad 1 (g/ml)", value=150)
            
            c_ing2, c_cant2 = st.columns(2)
            ing2 = c_ing2.text_input("Ingrediente 2", "Ej: Arroz integral")
            cant2 = c_cant2.number_input("Cantidad 2 (g/ml)", value=80)
            
            st.markdown("**Información Nutricional Aproximada**")
            n_cal = st.number_input("Calorías (kcal)", value=400)
            n_prot = st.number_input("Proteínas (g)", value=20)
            n_carb = st.number_input("Carbohidratos (g)", value=45)
            n_gras = st.number_input("Grasas (g)", value=12)

            st.markdown("**Adaptaciones a Estilos**")
            n_blw = st.text_input("Adaptación BLW", "Cortar en formato bastón de seguridad sin sal.")
            n_veg = st.text_input("Adaptación Vegana/Vegetariana", "Sustituir por tofu o legumbres.")

            if st.form_submit_button("💾 Guardar Receta en el Banco"):
                if n_nombre:
                    nueva_receta = {
                        "id": len(st.session_state.recipes) + 1,
                        "nombre": f"{n_cat[:-1]} personalizada: {n_nombre}",
                        "categoria": n_cat,
                        "ingredientes_base": {ing1: cant1, ing2: cant2},
                        "nutrientes_base": {"calorias": n_cal, "proteinas": n_prot, "carbos": n_carb, "grasas": n_gras, "hierro": 3, "calcio": 50},
                        "instrucciones": n_inst,
                        "adaptaciones": {"Estándar": "Receta manual.", "Vegetariano/Vegano": n_veg, "BLW": n_blw},
                        "batch_cooking": "Guardar en recipiente hermético en la nevera."
                    }
                    st.session_state.recipes.append(nueva_receta)
                    st.success(f"¡Receta '{n_nombre}' añadida con éxito al banco!")

# -----------------------------------------------------------------------------
# SECCIÓN 5: LISTA DE LA COMPRA INTERACTIVA Y CATEGORIZADA
# -----------------------------------------------------------------------------
elif menu_opcion == "🛒 Lista de la Compra":
    st.header("🛒 Lista de la Compra Interactiva")
    
    lista_compra_raw = generar_lista_compra_dict()

    if not lista_compra_raw:
        st.info("Planifica tu menú semanal en el planificador para generar la lista de la compra automáticamente.")
    else:
        # Clasificar por secciones
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

        # Contadores para la barra de progreso
        total_items = len(lista_compra_raw)
        marcados = 0

        # Calcular cuántos elementos están marcados
        for ing in lista_compra_raw.keys():
            if st.session_state.get(f"chk_{ing}", False):
                marcados += 1

        progreso = marcados / total_items if total_items > 0 else 0
        st.markdown(f"**Progreso de la compra:** {marcados} de {total_items} productos comprados")
        st.progress(progreso)

        st.markdown("---")

        # Desplegar secciones
        for sec, items in secciones.items():
            if items:
                st.subheader(sec)
                cols = st.columns(2)
                for idx, (ing, cant) in enumerate(items.items()):
                    col = cols[idx % 2]
                    key_chk = f"chk_{ing}"
                    # Checkbox interactivo
                    comprado = col.checkbox(
                        f"**{ing}**: {int(cant)} g/ml", 
                        key=key_chk
                    )
                st.markdown("")

# -----------------------------------------------------------------------------
# SECCIÓN 6: RECOMENDACIONES DE BATCH COOKING
# -----------------------------------------------------------------------------
elif menu_opcion == "👨‍🍳 Batch Cooking":
    st.header("👨‍🍳 Optimización de Batch Cooking Semanal")
    
    vistos = set()
    for dia, comidas in st.session_state.menu_semanal.items():
        for tipo in ["Desayuno", "Comida", "Cena"]:
            p = comidas[tipo]
            if p and p["id"] not in vistos:
                st.markdown(f"**{p['nombre']}**")
                st.success(p.get("batch_cooking", "Cocinar en el momento."))
                vistos.add(p["id"])
    if not vistos:
        st.info("Elige platos en el planificador para ver el plan de batch cooking.")

# -----------------------------------------------------------------------------
# SECCIÓN 7: PERSISTENCIA Y DESCARGA EN TEXTO
# -----------------------------------------------------------------------------
elif menu_opcion == "💾 Guardar / Exportar Texto":
    st.header("💾 Guardar y Exportar Menú / Lista de la Compra")
    
    st.subheader("1. Descargar Menú Semanal y Lista de la Compra en Formato Texto (.txt)")
    
    texto_menu = "=========================================\n"
    texto_menu += "         MENÚ SEMANAL FAMILIAR           \n"
    texto_menu += "=========================================\n\n"
    
    for dia, comidas in st.session_state.menu_semanal.items():
        texto_menu += f"--- {dia.upper()} ---\n"
        for tipo in ["Desayuno", "Comida", "Cena"]:
            plato = comidas[tipo]
            nom = plato['nombre'] if plato else "No asignado"
            texto_menu += f"  - {tipo}: {nom}\n"
        texto_menu += "\n"
        
    texto_menu += "=========================================\n"
    texto_menu += "          LISTA DE LA COMPRA             \n"
    texto_menu += "=========================================\n\n"
    
    lista_c = generar_lista_compra_dict()
    if lista_c:
        for ing, cant in lista_c.items():
            texto_menu += f" • {ing}: {int(cant)} g/ml\n"
    else:
        texto_menu += " (Lista vacía. Selecciona platos en el planificador).\n"

    st.text_area("Vista previa del archivo de texto:", texto_menu, height=250)
    
    c_dn1, c_dn2 = st.columns(2)
    c_dn1.download_button("📄 Descargar Menú y Lista (.txt)", texto_menu, file_name="menu_y_compra_semanal.txt", mime="text/plain")

    datos_exportar = {"profiles": st.session_state.profiles, "menu_semanal": st.session_state.menu_semanal}
    json_str = json.dumps(datos_exportar, indent=4)
    c_dn2.download_button("📦 Descargar Copia de Seguridad (JSON)", json_str, file_name="nutrifamily_backup.json", mime="application/json")
