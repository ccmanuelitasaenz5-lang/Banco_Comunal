#!/usr/bin/env python3
"""
SCRIPT DE RESETEO DE CONTRASEÑA - SEMILLERO COMUNAL
Permite resetear la contraseña de cualquier usuario sin necesidad de acceder al sistema
"""

import os
import sys
import sqlite3

# Intentar importar bcrypt
try:
    import bcrypt
    BCRYPT_DISPONIBLE = True
except ImportError:
    BCRYPT_DISPONIBLE = False
    print("⚠️  ADVERTENCIA: bcrypt no está instalado.")
    print("   Instálalo con: pip install bcrypt")
    print()

def hash_pw(pw):
    """Hashea una contraseña usando bcrypt"""
    if not BCRYPT_DISPONIBLE:
        print("❌ No se puede hashear sin bcrypt instalado.")
        return None
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_pw(pw, hashed):
    """Verifica una contraseña contra su hash"""
    if not BCRYPT_DISPONIBLE:
        return False
    try:
        return bcrypt.checkpw(pw.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def buscar_db():
    """Busca la base de datos en ubicaciones comunes"""
    ubicaciones_posibles = [
        'datos/semillero.db',
        'semillero.db',
        '../datos/semillero.db',
        './datos/semillero.db'
    ]
    
    for ubicacion in ubicaciones_posibles:
        if os.path.exists(ubicacion):
            return ubicacion
    
    return None

def listar_usuarios(db_path):
    """Lista todos los usuarios en la base de datos"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    usuarios = conn.execute('SELECT id, username, nombre_completo, rol, activo FROM usuarios').fetchall()
    conn.close()
    
    print("\n" + "="*80)
    print("  USUARIOS EN LA BASE DE DATOS")
    print("="*80)
    
    if not usuarios:
        print("  No hay usuarios registrados.")
    else:
        print(f"  {'ID':>3} | {'USUARIO':<20} | {'NOMBRE COMPLETO':<25} | {'ROL':<10} | ESTADO")
        print("  " + "-"*76)
        for u in usuarios:
            estado = "✓ Activo" if u['activo'] else "✗ Inactivo"
            print(f"  {u['id']:>3} | {u['username']:<20} | {u['nombre_completo'] or 'N/A':<25} | {u['rol']:<10} | {estado}")
    
    print("="*80 + "\n")

def verificar_password(db_path, username, password):
    """Verifica si una contraseña es correcta"""
    if not BCRYPT_DISPONIBLE:
        print("❌ No se puede verificar sin bcrypt instalado.")
        return False
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    u = conn.execute("SELECT password_hash FROM usuarios WHERE username=?", (username,)).fetchone()
    conn.close()
    
    if not u:
        print(f"❌ Usuario '{username}' no encontrado.")
        return False
    
    if check_pw(password, u['password_hash']):
        print(f"✅ Contraseña CORRECTA para usuario '{username}'")
        return True
    else:
        print(f"❌ Contraseña INCORRECTA para usuario '{username}'")
        return False

def resetear_password(db_path, username, nueva_password):
    """Resetea la contraseña de un usuario"""
    if not BCRYPT_DISPONIBLE:
        print("❌ No se puede resetear sin bcrypt instalado.")
        print("   Instala bcrypt primero: pip install bcrypt")
        return False
    
    conn = sqlite3.connect(db_path)
    
    # Verificar que el usuario existe
    u = conn.execute("SELECT id FROM usuarios WHERE username=?", (username,)).fetchone()
    if not u:
        print(f"❌ Usuario '{username}' no encontrado.")
        conn.close()
        return False
    
    # Generar nuevo hash
    nuevo_hash = hash_pw(nueva_password)
    if not nuevo_hash:
        conn.close()
        return False
    
    # Actualizar contraseña
    conn.execute("UPDATE usuarios SET password_hash=? WHERE username=?", (nuevo_hash, username))
    conn.commit()
    conn.close()
    
    print("\n" + "="*80)
    print("  ✅ CONTRASEÑA ACTUALIZADA EXITOSAMENTE")
    print("="*80)
    print(f"  Usuario:           {username}")
    print(f"  Nueva contraseña:  {nueva_password}")
    print("="*80 + "\n")
    
    return True

def reseteo_rapido(db_path):
    """Reseteo rápido del usuario principal a admin123"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    usuarios = conn.execute("SELECT username FROM usuarios WHERE activo=1 ORDER BY id LIMIT 1").fetchall()
    conn.close()
    
    if not usuarios:
        print("❌ No hay usuarios activos en la base de datos.")
        return False
    
    username = usuarios[0]['username']
    return resetear_password(db_path, username, 'admin123')

def menu_principal(db_path):
    """Menú interactivo"""
    while True:
        print("\n" + "="*80)
        print("  🔧 HERRAMIENTA DE RESETEO DE CONTRASEÑAS - SEMILLERO COMUNAL")
        print("="*80)
        print("  Base de datos: " + db_path)
        print("="*80)
        print("  1. Listar todos los usuarios")
        print("  2. Verificar contraseña de un usuario")
        print("  3. Resetear contraseña de un usuario")
        print("  4. Reseteo rápido (primer usuario → contraseña: admin123)")
        print("  0. Salir")
        print("="*80)
        
        try:
            opcion = input("\n  Selecciona una opción: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  👋 ¡Hasta pronto!\n")
            break
        
        if opcion == '1':
            listar_usuarios(db_path)
            
        elif opcion == '2':
            if not BCRYPT_DISPONIBLE:
                print("\n  ❌ Necesitas bcrypt instalado para verificar contraseñas.")
                print("     Instálalo con: pip install bcrypt\n")
                continue
            
            username = input("\n  Usuario: ").strip()
            password = input("  Contraseña a verificar: ")
            print()
            verificar_password(db_path, username, password)
            
        elif opcion == '3':
            if not BCRYPT_DISPONIBLE:
                print("\n  ❌ Necesitas bcrypt instalado para resetear contraseñas.")
                print("     Instálalo con: pip install bcrypt\n")
                continue
            
            listar_usuarios(db_path)
            username = input("  Usuario a resetear: ").strip()
            nueva_password = input("  Nueva contraseña: ").strip()
            
            if len(nueva_password) < 6:
                print("\n  ❌ La contraseña debe tener al menos 6 caracteres.\n")
            else:
                print()
                resetear_password(db_path, username, nueva_password)
            
        elif opcion == '4':
            if not BCRYPT_DISPONIBLE:
                print("\n  ❌ Necesitas bcrypt instalado para resetear contraseñas.")
                print("     Instálalo con: pip install bcrypt\n")
                continue
            
            print()
            reseteo_rapido(db_path)
            
        elif opcion == '0':
            print("\n  👋 ¡Hasta pronto!\n")
            break
        else:
            print("\n  ❌ Opción no válida.\n")

def main():
    """Función principal"""
    print("\n🌱 SEMILLERO COMUNAL - Reseteo de Contraseñas\n")
    
    # Buscar la base de datos
    db_path = buscar_db()
    
    if not db_path:
        print("❌ No se encontró la base de datos.")
        print("   Búsqueda realizada en:")
        print("   - datos/semillero.db")
        print("   - semillero.db")
        print("   - ../datos/semillero.db")
        print()
        db_path = input("Ingresa la ruta completa a semillero.db: ").strip()
        
        if not os.path.exists(db_path):
            print(f"\n❌ No se encuentra el archivo: {db_path}\n")
            sys.exit(1)
    
    print(f"✅ Base de datos encontrada: {db_path}\n")
    
    # Si se pasan argumentos por línea de comandos
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == 'listar':
            listar_usuarios(db_path)
        
        elif comando == 'verificar' and len(sys.argv) == 4:
            verificar_password(db_path, sys.argv[2], sys.argv[3])
        
        elif comando == 'resetear' and len(sys.argv) == 4:
            resetear_password(db_path, sys.argv[2], sys.argv[3])
        
        elif comando == 'rapido':
            reseteo_rapido(db_path)
        
        else:
            print("Uso:")
            print("  python resetear_password.py listar")
            print("  python resetear_password.py verificar <usuario> <contraseña>")
            print("  python resetear_password.py resetear <usuario> <nueva_contraseña>")
            print("  python resetear_password.py rapido")
    else:
        # Modo interactivo
        menu_principal(db_path)

if __name__ == '__main__':
    main()
