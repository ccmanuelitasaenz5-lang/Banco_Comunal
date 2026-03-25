"""
SemilleroComunal v1.2 - Pruebas modulo autenticacion
Ejecutado por INSTALAR.bat en el paso de verificacion
"""
import sys, os, hashlib, sqlite3, tempfile, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

ERRORES = []
PASADOS = 0

def ok(msg):
    global PASADOS
    PASADOS += 1
    print(f"  [PASS] {msg}")

def fail(msg):
    ERRORES.append(msg)
    print(f"  [FAIL] {msg}")

# Importar funciones
try:
    from app import hash_pw, validar_password, validar_username
    ok("Importacion de funciones auth exitosa")
except Exception as e:
    print(f"  [FAIL] No se pudo importar app.py: {e}")
    print("\n  RESULTADO: 0/1 pruebas pasaron")
    sys.exit(1)

# hash_pw
h = hash_pw("mi_clave_123")
if len(h) == 64 and h == hashlib.sha256("mi_clave_123".encode()).hexdigest():
    ok("hash_pw genera SHA-256 correctamente")
else:
    fail("hash_pw no genera el hash esperado")

if hash_pw("abc") != hash_pw("ABC"):
    ok("hash_pw distingue mayusculas/minusculas")
else:
    fail("hash_pw no distingue mayusculas/minusculas")

# validar_password
for pw, esperado, desc in [
    ("",      True,  "rechaza contrasena vacia"),
    ("abc",   True,  "rechaza contrasena de 3 caracteres"),
    ("123456",False, "acepta contrasena de 6 caracteres"),
    ("segura123", False, "acepta contrasena de 8 caracteres"),
]:
    resultado = validar_password(pw) is not None
    if resultado == esperado:
        ok(f"validar_password {desc}")
    else:
        fail(f"validar_password {desc}")

# validar_username
for u, esperado, desc in [
    ("",              True,  "rechaza usuario vacio"),
    ("ab",            True,  "rechaza usuario de 2 caracteres"),
    ("con espacios",  True,  "rechaza usuario con espacios"),
    ("usuario$malo",  True,  "rechaza caracteres especiales"),
    ("enrique.01",    False, "acepta usuario con punto y numeros"),
    ("Admin_123",     False, "acepta usuario alfanumerico con guion bajo"),
]:
    resultado = validar_username(u) is not None
    if resultado == esperado:
        ok(f"validar_username {desc}")
    else:
        fail(f"validar_username {desc}")

# Base de datos
try:
    tmp = tempfile.mkdtemp()
    db  = sqlite3.connect(os.path.join(tmp, "test.db"))
    db.execute("""CREATE TABLE usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        rol TEXT DEFAULT 'admin',
        activo INTEGER DEFAULT 1)""")
    db.commit()

    pw_hash = hash_pw("prueba123")
    db.execute("INSERT INTO usuarios(username,password_hash) VALUES(?,?)", ("test_user", pw_hash))
    db.commit()
    ok("Insercion de usuario en BD")

    u = db.execute("SELECT * FROM usuarios WHERE username=?", ("test_user",)).fetchone()
    ok("Recuperacion de usuario de BD") if u else fail("No se encontro usuario insertado")

    ok("Login correcto: hash coincide") if u and u[2] == hash_pw("prueba123") else fail("Hash incorrecto en login")
    ok("Login incorrecto: hash no coincide") if u and u[2] != hash_pw("clave_mala") else fail("Hash acepto clave incorrecta")

    db.execute("UPDATE usuarios SET activo=0 WHERE username=?", ("test_user",))
    db.commit()
    u2 = db.execute("SELECT activo FROM usuarios WHERE username=?", ("test_user",)).fetchone()
    ok("Toggle desactivar usuario") if u2 and u2[0] == 0 else fail("Toggle desactivar fallo")

    db.execute("UPDATE usuarios SET activo=1 WHERE username=?", ("test_user",))
    db.commit()
    u3 = db.execute("SELECT activo FROM usuarios WHERE username=?", ("test_user",)).fetchone()
    ok("Toggle activar usuario") if u3 and u3[0] == 1 else fail("Toggle activar fallo")

    nueva = hash_pw("nueva456")
    db.execute("UPDATE usuarios SET password_hash=? WHERE username=?", (nueva, "test_user"))
    db.commit()
    u4 = db.execute("SELECT password_hash FROM usuarios WHERE username=?", ("test_user",)).fetchone()
    ok("Cambio de contrasena en BD") if u4 and u4[0] == hash_pw("nueva456") else fail("Cambio de contrasena fallo")

    try:
        db.execute("INSERT INTO usuarios(username,password_hash) VALUES(?,?)", ("test_user", pw_hash))
        db.commit()
        fail("BD acepto usuario duplicado")
    except sqlite3.IntegrityError:
        ok("BD rechaza usuario duplicado (UNIQUE)")

    db.close()
    shutil.rmtree(tmp)

except Exception as e:
    fail(f"Error en prueba de BD: {e}")

# Templates
for t in ["login.html", "recuperar.html", "setup.html", "dashboard.html"]:
    path = os.path.join(BASE, "templates", t)
    ok(f"Template presente: {t}") if os.path.exists(path) else fail(f"Template FALTANTE: {t}")

# Resumen
total = PASADOS + len(ERRORES)
print()
print("  -------------------------------------------------------")
print(f"  RESULTADO: {PASADOS}/{total} pruebas pasaron")
if ERRORES:
    print(f"  FALLOS ({len(ERRORES)}):")
    for e in ERRORES:
        print(f"    - {e}")
    sys.exit(1)
else:
    print("  TODAS LAS PRUEBAS PASARON - Modulo auth verificado OK")
    sys.exit(0)
