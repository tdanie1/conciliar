# Conciliación Bancaria con Streamlit

Aplicación en **Streamlit** para realizar conciliaciones bancarias entre los movimientos de la empresa (ERP/contabilidad) y el extracto bancario.  
Permite validar datos, identificar diferencias y generar reportes en **CSV** y **Excel**.

---

## 🚀 Funcionalidades
- Subida de dos archivos (Empresa y Banco) en formato **CSV** o **Excel**.
- Validación de datos obligatorios: **Fecha, Descripción, Monto**.
- Alertas de transacciones incompletas.
- Conciliación automática de movimientos.
- Resumen de totales y diferencias.
- Detalle de transacciones con discrepancias.
- Exportación de diferencias en **CSV** y **Excel** con observaciones.

---

## 📂 Archivos requeridos
Los archivos deben contener al menos las siguientes columnas:

- `Fecha` → Fecha de la transacción  
- `Descripción` → Detalle o concepto de la transacción  
- `Monto` → Valor de la transacción  

> La aplicación reconoce automáticamente nombres alternativos como `detalle`, `concepto`, `valor`, `importe`.

---

## ⚙️ Instalación local
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/conciliacion-bancaria.git
   cd conciliacion-bancaria
