import sqlite3, bcrypt, os, sys

# RUTA EXACTA DE TU BASE DE DATOS
DB_PATH = r"D:\BancoComunal\datos\semillero.db"
NUEVA_PASSWORD = "123456"  # Contraseña temporal de emergencia

print("🔍 Buscando base de datos: semillero.db...")
print("-" * 50)

if not os.path.exists(DB_PATH):
    print("❌ ERROR: No se encuentra el archivo 'semillero.db' en la ruta esperada.")
    print(f"   Ruta buscada: {DB_PATH}")
    input("\nPresiona Enter para salir...")
    sys.exit(1)

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. LISTAR USUARIOS
    cursor.execute("SELECT username, rol, activo FROM usuarios")
    usuarios = cursor.fetchall()
    
    if not usuarios:
        print("⚠️ La base de datos no tiene usuarios registrados.")
        conn.close()
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    print(f"✅ Se encontraron {len(usuarios)} usuario(s) en 'semillero.db':")
    for u in usuarios:
        estado = "ACTIVO" if u[2] == 1 else "INACTIVO"
        print(f"   👤 Usuario: '{u[0]}' | Rol: {u[1]} | Estado: {estado}")
    
    # 2. SELECCIONAR OBJETIVO
    # Buscamos el primer administrador activo
    objetivo = None
    for u in usuarios:
        if u[2] == 1 and u[1] == 'admin':
            objetivo = u
            break
    
    # Si no hay admin activo, tomamos el primero activo
    if not objetivo:
        for u in usuarios:
            if u[2] == 1:
                objetivo = u
                break
    
    # Si todos están inactivos, tomamos el primero de la lista
    if not objetivo:
        objetivo = usuarios[0]

    usuario_a_resetear = objetivo[0]
    print("-" * 50)
    print(f"🔄 Preparando reseteo para el usuario: '{usuario_a_resetear}'...")

    # 3. GENERAR HASH SEGURO (BCRYPT)
    # Esto es crucial para que la app lo acepte
    hash_seguro = bcrypt.hashpw(NUEVA_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 4. ACTUALIZAR EN LA BASE DE DATOS
    cursor.execute("UPDATE usuarios SET password_hash = ? WHERE username = ?", (hash_seguro, usuario_a_resetear))
    conn.commit()
    
    if cursor.rowcount > 0:
        print("\n" + "=" * 50)
        print("🎉 ¡ÉXITO! CONTRASEÑA RESTABLECIDA")
        print("=" * 50)
        print(f"   Usuario: {usuario_a_resetear}")
        print(f"   NUEVA CONTRASEÑA: {NUEVA_PASSWORD}")
        print("\n   👉 INSTRUCCIONES:")
        print(f"   1. Cierra esta ventana.")
        print(f"   2. Abre tu app SemilleroComunal.")
        print(f"   3. Inicia sesión con usuario '{usuario_a_resetear}' y clave '{NUEVA_PASSWORD}'.")
        print(f"   4. Una vez dentro, ve a Configuración y cambia la clave por una segura.")
        print("=" * 50)
    else:
        print("⚠️ Ocurrió un error al actualizar (ninguna fila afectada).")
        
    conn.close()

except Exception as e:
    print(f"\n❌ ERROR GRAVE: {e}")
    import traceback
    traceback.print_exc()

input("\nPresiona Enter para salir...")