# 🔧 SOLUCIÓN DE PROBLEMAS - SEMILLERO COMUNAL

## 🚨 PROBLEMA ACTUAL: No puedes ingresar al sistema

### Usuario actual en la base de datos:
- **Usuario**: `enmaduro`
- **Nombre**: Enrique Maduro
- **Estado**: Activo

---

## ✅ SOLUCIÓN RÁPIDA (3 pasos)

### PASO 1: Instalar bcrypt
Abre la terminal o CMD y ejecuta:
```bash
pip install bcrypt
```

### PASO 2: Ejecutar el script de reseteo
Copia el archivo `resetear_password.py` a la carpeta de tu proyecto (donde está `app.py`) y ejecuta:

```bash
python resetear_password.py rapido
```

Esto reseteará la contraseña del primer usuario a `admin123`.

### PASO 3: Ingresar al sistema
Abre la aplicación y ingresa con:
- **Usuario**: `enmaduro`
- **Contraseña**: `admin123`

---

## 🔍 SOLUCIÓN ALTERNATIVA (Sin script)

Si prefieres hacerlo manualmente:

### Opción A: Resetear solo la contraseña

1. Abre Python y ejecuta:
```python
import bcrypt
import sqlite3

def hash_pw(pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Conectar a la base de datos
conn = sqlite3.connect('datos/semillero.db')

# Generar hash para 'admin123'
nuevo_hash = hash_pw('admin123')

# Actualizar el usuario
conn.execute("UPDATE usuarios SET password_hash=? WHERE username='enmaduro'", (nuevo_hash,))
conn.commit()
conn.close()

print("✅ Contraseña reseteada a: admin123")
```

### Opción B: Resetear toda la aplicación (⚠️ PERDERÁS TODOS LOS DATOS)

1. Cierra la aplicación
2. Elimina o renombra el archivo `datos/semillero.db`
3. Reinicia la aplicación
4. Configurarás el sistema desde cero

---

## 🐛 BUG CORREGIDO EN app.py

### Problema encontrado:
El módulo de setup tenía un error SQL que causaba un bucle infinito:

**Código original (INCORRECTO)**:
```python
c.execute("""INSERT OR REPLACE INTO usuarios
   (username,password_hash,pregunta_seguridad,respuesta_hash,nombre_completo,rol)
   VALUES(?,?,?,?,?,'admin')""",  # ❌ Solo 5 placeholders pero 6 columnas
    (usuario, password_hash, pregunta, respuesta_hash, nombre_completo)  # ❌ Solo 5 valores
)
```

**Código corregido (CORRECTO)**:
```python
c.execute("""INSERT OR REPLACE INTO usuarios
   (username,password_hash,pregunta_seguridad,respuesta_hash,nombre_completo,rol)
   VALUES(?,?,?,?,?,?)""",  # ✅ 6 placeholders
    (usuario, password_hash, pregunta, respuesta_hash, nombre_completo, 'admin')  # ✅ 6 valores
)
```

### Para aplicar la corrección:

1. Respalda tu `app.py` actual:
```bash
copy app.py app_backup.py
```

2. Reemplaza tu `app.py` con el archivo corregido `app.py` que te proporcioné

3. Reinicia la aplicación

---

## 📁 ARCHIVOS PROPORCIONADOS

### 1. `app.py` (CORREGIDO)
- ✅ Bug del setup corregido
- ✅ Validación de usuario después de crearlo
- ✅ Logging de intentos de login fallidos
- ✅ Listo para usar

### 2. `resetear_password.py`
Script independiente para:
- Listar usuarios
- Verificar contraseñas
- Resetear contraseñas
- Reseteo rápido con un comando

**Uso:**
```bash
# Modo interactivo (menú)
python resetear_password.py

# Modo comandos
python resetear_password.py listar
python resetear_password.py resetear enmaduro admin123
python resetear_password.py rapido
```

### 3. `DIAGNOSTICO.md`
Análisis técnico del problema encontrado.

### 4. `SOLUCIONES.md`
Documento completo con todas las soluciones y mejoras.

---

## 🎯 PASOS RECOMENDADOS (En orden)

1. ✅ **Resetear contraseña** usando el script o método manual
2. ✅ **Ingresar al sistema** con la nueva contraseña
3. ✅ **Reemplazar app.py** con la versión corregida
4. ✅ **Cambiar tu contraseña** desde el sistema usando una que recuerdes
5. ✅ **Continuar con las mejoras** que solicitaste (módulos de contrato, estadísticas, etc.)

---

## 🆘 SI AÚN TIENES PROBLEMAS

### Problema: No puedo instalar bcrypt
```bash
# En Windows
pip install bcrypt

# Si falla, intenta:
python -m pip install bcrypt

# O con permisos de administrador
pip install bcrypt --user
```

### Problema: El script no encuentra la base de datos
El script busca en:
- `datos/semillero.db`
- `semillero.db`
- `../datos/semillero.db`

Si no la encuentra, te pedirá que ingreses la ruta manualmente.

### Problema: Sigo sin poder ingresar después del reseteo
1. Verifica que el archivo `datos/semillero.db` se haya actualizado (fecha de modificación)
2. Asegúrate de estar usando el usuario correcto: `enmaduro` (sin espacios)
3. La contraseña es exactamente: `admin123` (sin espacios, todo minúscula)
4. Revisa los logs en `datos/app.log` para ver errores específicos

---

## 📞 INFORMACIÓN DE SOPORTE

### Versión de Python requerida
- Python 3.7 o superior

### Dependencias necesarias
```bash
pip install flask bcrypt faker python-docx reportlab python-pptx pillow
```

### Archivos del proyecto
```
SemilleroComunal/
├── app.py                      (Archivo principal - ¡ACTUALÍZALO!)
├── resetear_password.py        (Script de reseteo - ¡NUEVO!)
├── datos/
│   ├── semillero.db           (Base de datos)
│   ├── .secret_key            (Clave secreta)
│   └── app.log                (Logs de errores)
├── templates/                  (HTML)
├── static/                     (CSS, JS, imágenes)
└── ABRIR_SEMILLERO.bat        (Lanzador)
```

---

## 🚀 PRÓXIMOS PASOS

Una vez resuelto el acceso, implementaremos:

### 1. Módulo de Contrato Mejorado
- ✨ Upload de modelo propio o uso de plantilla base
- 📸 OCR para cédula y RIF
- ✔️ Validación de vigencia de RIF
- 👥 Formulario para voceros/voceras del Banco Comunal
- 🗑️ Eliminación de referencias a "Comuna Productiva Presidente Obrero"

### 2. Módulo de Estadísticas e Informes
- 📊 Dashboard con gráficos
- 📄 Informes PDF profesionales
- 📽️ Presentaciones PowerPoint
- 📈 Análisis de cartera y pagos

### 3. Ubicación Manual en Mapa
- 🗺️ Interfaz para colocar direcciones de beneficiarios
- 📍 Marcadores personalizados
- 🔍 Búsqueda de ubicaciones

### 4. Instalación Simplificada
- 🖱️ Un solo clic para iniciar
- 🎨 Icono en escritorio
- ⚙️ Configuración automática

---

**¡Estamos listos para resolver tu problema y mejorar el sistema!**

¿Por dónde quieres empezar?
