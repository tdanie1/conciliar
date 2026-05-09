import streamlit as st
import pandas as pd

st.title("Conciliación Bancaria")

# Subida de archivos
empresa_file = st.file_uploader("Sube archivo de Empresa/ERP", type=["csv", "xlsx"])
banco_file = st.file_uploader("Sube archivo de Banco", type=["csv", "xlsx"])

def cargar_archivo(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if empresa_file and banco_file:
    df_empresa = cargar_archivo(empresa_file)
    df_banco = cargar_archivo(banco_file)

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

        # Conciliación: unir por Fecha, Monto y Descripción
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

        # Exportar resultados
        diferencias["Observación"] = diferencias["Origen"].apply(
            lambda x: "Revisar registro en ERP" if x=="Empresa" else "Verificar extracto bancario"
        )

        csv = diferencias.to_csv(index=False).encode("utf-8")
        excel = diferencias.to_excel("diferencias.xlsx", index=False)

        st.download_button("Descargar diferencias en CSV", csv, "diferencias.csv", "text/csv")
        st.download_button("Descargar diferencias en Excel", open("diferencias.xlsx","rb").read(), "diferencias.xlsx")
