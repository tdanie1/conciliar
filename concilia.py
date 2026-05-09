""" -- DESDE AQUI AL PRINCIPIO import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Conciliación Bancaria")

# Función para cargar archivo CSV o Excel
def cargar_archivo(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# Normalización de columnas
def normalizar_columnas(df):
    df = df.rename(columns=lambda x: x.strip().lower())
    mapping = {
        "fecha": "Fecha",
        "descripcion": "Descripción",
        "detalle": "Descripción",
        "concepto": "Descripción",
        "monto": "Monto",
        "valor": "Monto",
        "importe": "Monto"
    }
    df = df.rename(columns={col: mapping[col] for col in df.columns if col in mapping})
    return df

# Conversión de tipos
def limpiar_datos(df):
    if "Fecha" in df.columns:
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    if "Monto" in df.columns:
        df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce")
    return df

# Subida de archivos
empresa_file = st.file_uploader("Sube archivo de Empresa/ERP", type=["csv", "xlsx"])
banco_file = st.file_uploader("Sube archivo de Banco", type=["csv", "xlsx"])

if empresa_file and banco_file:
    df_empresa = cargar_archivo(empresa_file)
    df_banco = cargar_archivo(banco_file)

    # Normalizar y limpiar
    df_empresa = limpiar_datos(normalizar_columnas(df_empresa))
    df_banco = limpiar_datos(normalizar_columnas(df_banco))

    # Validación de campos obligatorios
    campos_obligatorios = ["Fecha", "Descripción", "Monto"]
    errores = {}

    for nombre, df in [("Empresa", df_empresa), ("Banco", df_banco)]:
        faltantes = df[df[campos_obligatorios].isnull().any(axis=1)]
        if not faltantes.empty:
            errores[nombre] = faltantes

    if errores:
        st.error("⚠️ Se encontraron transacciones incompletas")
        for origen, faltantes in errores.items():
            st.write(f"Transacciones incompletas en {origen}:")
            st.dataframe(faltantes)
    else:
        st.success("✅ Archivos validados correctamente")

        # Conciliación
        df_empresa["Origen"] = "Empresa"
        df_banco["Origen"] = "Banco"

        df_conciliado = pd.concat([df_empresa, df_banco])
        diferencias = df_conciliado.drop_duplicates(subset=["Fecha","Descripción","Monto"], keep=False)

        # Totales
        total_empresa = df_empresa["Monto"].sum()
        total_banco = df_banco["Monto"].sum()
        diferencia_total = total_empresa - total_banco

        st.subheader("Resumen de conciliación")
        resumen = pd.DataFrame({
            "Concepto": ["Total movimientos empresa", "Total movimientos banco", "Diferencias detectadas"],
            "Total": [f"{total_empresa:,.2f}", f"{total_banco:,.2f}", f"{diferencia_total:,.2f}"]
        })
        # st.table(resumen) CORRECCIÓN
        st.table(resumen.style.format({"Total": "{:,.2f}"}).set_properties(**{"text-align": "right"}))

        st.subheader("Detalle de diferencias")
        # Formatear fecha para mostrar solo YYYY-MM-DD
        diferencias["Fecha"] = diferencias["Fecha"].dt.strftime("%Y-%m-%d")
        # Formatear monto con dos decimales
        diferencias["Monto"] = diferencias["Monto"].apply(lambda x: f"{x:,.2f}")
        # st.dataframe(diferencias) CORRECCIÓN
        st.dataframe(
            diferencias.style.format({"Monto": "{:,.2f}"}).set_properties(**{"text-align": "right"})
        )


        # Observaciones
        diferencias["Observación"] = diferencias["Origen"].apply(
            lambda x: "Revisar registro en ERP" if x=="Empresa" else "Verificar extracto bancario"
        )

        # Exportar CSV
        csv = diferencias.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar diferencias en CSV", csv, "diferencias.csv", "text/csv")

        # Exportar Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            diferencias.to_excel(writer, index=False, sheet_name="Diferencias")
        excel_data = output.getvalue()

        st.download_button("Descargar diferencias en Excel", excel_data, "diferencias.xlsx")
        -- HASTA ACA AL FINAL """
# VERSION ANTERIOR (ORIGINAL)
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Conciliación Bancaria")

# Función para cargar archivo CSV o Excel
def cargar_archivo(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# Normalización de columnas
def normalizar_columnas(df):
    df = df.rename(columns=lambda x: x.strip().lower())
    mapping = {
        "fecha": "Fecha",
        "descripcion": "Descripción",
        "detalle": "Descripción",
        "concepto": "Descripción",
        "monto": "Monto",
        "valor": "Monto",
        "importe": "Monto"
    }
    df = df.rename(columns={col: mapping[col] for col in df.columns if col in mapping})
    return df

# Conversión de tipos
def limpiar_datos(df):
    if "Fecha" in df.columns:
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    if "Monto" in df.columns:
        df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce")
    return df

# Subida de archivos
empresa_file = st.file_uploader("Sube archivo de Empresa/ERP", type=["csv", "xlsx"])
banco_file = st.file_uploader("Sube archivo de Banco", type=["csv", "xlsx"])

if empresa_file and banco_file:
    df_empresa = cargar_archivo(empresa_file)
    df_banco = cargar_archivo(banco_file)

    # Normalizar y limpiar
    df_empresa = limpiar_datos(normalizar_columnas(df_empresa))
    df_banco = limpiar_datos(normalizar_columnas(df_banco))

    # Validación de campos obligatorios
    campos_obligatorios = ["Fecha", "Descripción", "Monto"]
    errores = {}

    for nombre, df in [("Empresa", df_empresa), ("Banco", df_banco)]:
        faltantes = df[df[campos_obligatorios].isnull().any(axis=1)]
        if not faltantes.empty:
            errores[nombre] = faltantes

    if errores:
        st.error("⚠️ Se encontraron transacciones incompletas")
        for origen, faltantes in errores.items():
            st.write(f"Transacciones incompletas en {origen}:")
            st.dataframe(faltantes)
    else:
        st.success("✅ Archivos validados correctamente")

        # Conciliación
        df_empresa["Origen"] = "Empresa"
        df_banco["Origen"] = "Banco"

        df_conciliado = pd.concat([df_empresa, df_banco])
        diferencias = df_conciliado.drop_duplicates(subset=["Fecha","Descripción","Monto"], keep=False)

        # Totales
        total_empresa = df_empresa["Monto"].sum()
        total_banco = df_banco["Monto"].sum()
        diferencia_total = total_empresa - total_banco

        st.subheader("Resumen de conciliación")
        resumen = pd.DataFrame({
            "Concepto": ["Total movimientos empresa", "Total movimientos banco", "Diferencias detectadas"],
            "Total": [total_empresa, total_banco, diferencia_total]
        })
        st.table(resumen)

        st.subheader("Detalle de diferencias")
        st.dataframe(diferencias)

        # Observaciones
        diferencias["Observación"] = diferencias["Origen"].apply(
            lambda x: "Revisar registro en ERP" if x=="Empresa" else "Verificar extracto bancario"
        )

        # Exportar CSV
        csv = diferencias.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar diferencias en CSV", csv, "diferencias.csv", "text/csv")

        # Exportar Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            diferencias.to_excel(writer, index=False, sheet_name="Diferencias")
        excel_data = output.getvalue()

        st.download_button("Descargar diferencias en Excel", excel_data, "diferencias.xlsx")


