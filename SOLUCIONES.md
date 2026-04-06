# 🔧 SOLUCIONES PARA SEMILLERO COMUNAL

## ❌ PROBLEMAS IDENTIFICADOS

### 1. BUG CRÍTICO EN MÓDULO DE REGISTRO (líneas 260-268)
**Error encontrado**: Desajuste entre placeholders SQL y parámetros

**Código original (INCORRECTO)**:
```python
c.execute("""INSERT OR REPLACE INTO usuarios
   (username,password_hash,pregunta_seguridad,respuesta_hash,nombre_completo,rol)
   VALUES(?,?,?,?,?,'admin')""",  # ❌ Solo 5 placeholders (?) pero 6 columnas
    (d.get('usuario','').strip(),
     hash_pw(d.get('password','')),
     d.get('pregunta'),
     hash_pw(d.get('respuesta','').lower().strip()),
     d.get('nombre_completo','').strip())  # ❌ Solo 5 valores
)
```

**Código corregido (CORRECTO)**:
```python
c.execute("""INSERT OR REPLACE INTO usuarios
   (username,password_hash,pregunta_seguridad,respuesta_hash,nombre_completo,rol)
   VALUES(?,?,?,?,?,?)""",  # ✅ 6 placeholders
    (d.get('usuario','').strip(),
     hash_pw(d.get('password','')),
     d.get('pregunta'),
     hash_pw(d.get('respuesta','').lower().strip()),
     d.get('nombre_completo','').strip(),
     'admin')  # ✅ 6 valores
)
```

**Por qué causaba el bucle**:
1. El INSERT fallaba silenciosamente
2. La config se marcaba como 'configurado':'1'
3. Redirigía a login sin usuario creado
4. Login fallaba → redirigía a setup
5. Setup veía 'configurado' → redirigía a login
6. **BUCLE INFINITO** ♾️

---

## ✅ SOLUCIÓN INMEDIATA: Acceder al sistema

### Opción A: Usando el usuario existente `enmaduro`

El usuario ya existe en la base de datos, pero necesitas saber la contraseña original.

**Prueba estas contraseñas comunes:**
- `admin`
- `admin123`
- `123456`
- `enmaduro`
- `semillero`
- La que configuraste durante el setup

### Opción B: Resetear la base de datos

Si no recuerdas la contraseña, tienes dos opciones:

#### B1. Reseteo completo (perderás todos los datos)
1. Cierra la aplicación
2. Elimina o renombra el archivo `datos/semillero.db`
3. Reinicia la aplicación
4. Volverá a mostrarte el setup inicial

#### B2. Reseteo solo de contraseña (mantiene los datos)
Como no puedo generar el hash bcrypt sin la librería, necesitarás:

1. Instalar Python y bcrypt en tu computadora:
```bash
pip install bcrypt
```

2. Ejecutar este script Python:
```python
import bcrypt
import sqlite3

def hash_pw(pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Genera el hash para la contraseña 'admin123'
nuevo_hash = hash_pw('admin123')

# Actualiza la base de datos
conn = sqlite3.connect('datos/semillero.db')
conn.execute("UPDATE usuarios SET password_hash=? WHERE username='enmaduro'", (nuevo_hash,))
conn.commit()
conn.close()

print("✅ Contraseña reseteada a: admin123")
```

3. Luego ingresa con:
   - Usuario: `enmaduro`
   - Contraseña: `admin123`

---

## 🔨 CORRECCIONES PARA IMPLEMENTAR

### 1. Archivo app.py corregido

Reemplaza las líneas 260-268 con la versión corregida mostrada arriba.

Te voy a proporcionar el archivo completo corregido.

### 2. Mejoras adicionales de seguridad

Agregar validación después del INSERT:

```python
# Después de la línea 268
cursor_result = c.execute("SELECT id FROM usuarios WHERE username=?", 
                         (d.get('usuario','').strip(),)).fetchone()

if not cursor_result:
    # Si el usuario no se creó, no marcar como configurado
    conn.rollback()
    conn.close()
    return render_template('setup.html', errores={'general': 'Error al crear usuario. Intenta de nuevo.'})
```

### 3. Mejorar recuperación de contraseña

Agregar mensajes más claros cuando falla:

```python
# En la línea 313, cambiar:
error = 'Usuario o contraseña incorrectos.'

# Por:
error = 'Usuario o contraseña incorrectos. ¿Olvidaste tu contraseña? <a href="/recuperar">Recupérala aquí</a>.'
```

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

- [ ] 1. Respaldar `app.py` original
- [ ] 2. Aplicar corrección en líneas 260-268
- [ ] 3. Agregar validación post-INSERT (opcional pero recomendado)
- [ ] 4. Resetear contraseña o base de datos
- [ ] 5. Probar login con usuario conocido
- [ ] 6. Probar crear nuevo usuario desde setup
- [ ] 7. Probar recuperación de contraseña

---

## 🚀 PRÓXIMOS PASOS (Mejoras solicitadas)

Una vez solucionado el problema de acceso, implementaremos:

1. **Módulo de Contrato mejorado**
   - Upload de modelo propio
   - OCR para cédula y RIF
   - Validación de vigencia de RIF
   - Formulario para voceros/voceras

2. **Módulo de Estadísticas e Informes**
   - Reportes PDF mejorados
   - Presentaciones PPTX
   - Dashboard de estadísticas

3. **Ubicación manual en mapa**
   - Interfaz para colocar direcciones manualmente

4. **Instalación simplificada**
   - Script único de inicio
   - Icono en escritorio

---

## 📞 SOPORTE

Si después de aplicar estas correcciones sigues teniendo problemas:

1. Verifica que tienes la versión correcta de Python (3.7+)
2. Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`
3. Revisa los logs en `datos/app.log`
4. Comparte el mensaje de error específico que recibes

---

**Última actualización**: $(date)
**Versión del documento**: 1.0
