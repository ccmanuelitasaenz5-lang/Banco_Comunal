import sqlite3, bcrypt, os

# Configuración
DB_PATH = r"D:\BancoComunal\datos\semillero.db"
NUEVA_PASSWORD = "tu_nueva_clave"  # <--- CAMBIA ESTO POR TU CONTRASEÑA DESEADA
USUARIO = "admin" # O el nombre de usuario que usas

if not os.path.exists(DB_PATH):
    print("❌ Error: No se encuentra la base de datos en", DB_PATH)
    input("Presiona Enter para salir...")
    exit()

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Generar hash seguro con bcrypt
    hash_seguro = bcrypt.hashpw(NUEVA_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Actualizar en la BD
    cursor.execute("UPDATE usuarios SET password_hash = ? WHERE username = ?", (hash_seguro, USUARIO))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"✅ ¡ÉXITO! La contraseña para el usuario '{USUARIO}' ha sido actualizada.")
        print(f"   Nueva contraseña: {NUEVA_PASSWORD}")
        print("   Ahora puedes cerrar este script e iniciar sesión en la app.")
    else:
        print(f"⚠️ No se encontró el usuario '{USUARIO}'. Verifica el nombre.")
        
    conn.close()
except Exception as e:
    print(f"❌ Error grave: {e}")

input("\nPresiona Enter para salir...")