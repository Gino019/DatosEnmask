# Guía: Git + GitHub - Primer Paso para Desplegar

Este documento te guía a través de los pasos para subir tu proyecto a GitHub, requisito fundamental para desplegar en cualquier plataforma de hosting.

---

## 1) Verificar instalación de Git

```bash
git --version
```

Si no está instalado, descargarlo desde [git-scm.com](https://git-scm.com)

---

## 2) Inicializar repositorio Git en tu proyecto (si aún no lo has hecho)

```bash
cd C:\Users\W10\Desktop\proyecto-si783-2026-i-u2-enmascaradodatos

# Verificar si ya hay un repositorio git
git status

# Si NO hay repositorio, inicializarlo:
git init
```

---

## 3) Configurar usuario Git (si es la primera vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"

# Verificar que se configuró correctamente
git config --global user.name
git config --global user.email
```

---

## 4) Crear `.gitignore` en la raíz del proyecto

Si no existe, crear un archivo llamado `.gitignore` con el siguiente contenido:

```
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.env
.env.local
.env.*.local
*.egg-info/
dist/
build/

# Node
node_modules/
dist/
build/
.next/
out/
.nuxt/
.cache/
.vuepress/dist/
.serverless/
.fusebox/
.dynamodb/
.tern-port
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
.dockerignore

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3
dump.rdb
```

Guardar como `.gitignore` en la raíz del proyecto.

---

## 5) Agregar todos los archivos y hacer commit inicial

```bash
# Ver qué archivos van a ser agregados
git add . --dry-run

# Agregar todos los archivos
git add .

# Ver el status
git status

# Hacer el primer commit
git commit -m "Initial commit: Enmask SDM Platform"
```

---

## 6) Crear repositorio en GitHub

1. Ve a [github.com](https://github.com) e inicia sesión (crea cuenta si no tienes)
2. Haz click en el `+` en la esquina superior derecha → **New repository**
3. Nombre: `proyecto-si783-2026-i-u2-enmascaradodatos` (o similar)
4. **NO inicialices con README** (ya tienes uno local)
5. Haz click en **Create repository**

---

## 7) Conectar repositorio local con GitHub

GitHub te mostrará los comandos. En tu terminal (en la raíz del proyecto):

```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/TU_USUARIO/proyecto-si783-2026-i-u2-enmascaradodatos.git

# Renombrar la rama principal a 'main' (si está en 'master')
git branch -M main

# Subir los archivos a GitHub
git push -u origin main
```

---

## 8) Verificar que se subió correctamente

Entra a tu repositorio en GitHub y confirma que ves todos los archivos.

---

## 9) Copiar URL del repositorio

En GitHub, botón verde **Code** → copiar la URL HTTPS o SSH:

```
https://github.com/TU_USUARIO/proyecto-si783-2026-i-u2-enmascaradodatos.git
```

Esta URL la usarás para conectar con Vercel, Railway, Render, etc.

---

## 10) Cambios futuros

Cada vez que hagas cambios locales:

```bash
git add .
git commit -m "Descripción del cambio"
git push
```

Los cambios se sincronizarán automáticamente en GitHub y triggearán despliegues en Vercel/Railway.

---

## Troubleshooting

### Error: "fatal: not a git repository"
```bash
cd C:\Users\W10\Desktop\proyecto-si783-2026-i-u2-enmascaradodatos
git init
```

### Error: "Permission denied (publickey)"
Necesitas configurar SSH. O usa HTTPS con token en lugar de contraseña:
- Ve a GitHub → Settings → Developer settings → Personal access tokens
- Copia el token y úsalo como contraseña en `git push`

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/repo.git
```

---

## Próximos pasos

Una vez tengas el repositorio en GitHub, elige una opción de deploy:
- **Vercel + Railway** (recomendado para aplicaciones con frontend + backend)
- **Render.com** (simple, todo en un lugar)
- **Fly.io** (bueno para aplicaciones escalables)
- **Docker en VPS** (más control, requiere más configuración)

Consulta `02-DEPLOYMENT-OPCIONES.md` para elegir la mejor opción.
