# Deployment en Render.com - Guía Paso a Paso

Render.com es la opción más simple: todo (Frontend + Backend) en una sola plataforma.

---

## Ventajas de Render

✅ **Simplicidad**: Frontend y Backend en el mismo lugar  
✅ **Base de datos integrada**: PostgreSQL/MySQL gratis  
✅ **Deploy automático desde GitHub**: Solo conecta el repo  
✅ **HTTPS automático**  
✅ **Buen plan gratuito** (con limitación de hibernación)  

---

## Limitación importante

> ⚠️ Los servicios en plan gratuito se hibernan (duermen) después de 15 minutos sin recibir solicitudes. La primera solicitud tardará 30 segundos en "despertar" el servicio.

Si esto es problema, puedes usar [Uptime Robot](https://uptimerobot.com/) (gratuito) para mantener el servicio activo.

---

## Requisitos previos

1. ✅ Proyecto en GitHub (ver [01-GUIA-GIT-GITHUB.md](01-GUIA-GIT-GITHUB.md))
2. ✅ Variables de entorno configuradas (ver `.env.example`)

---

## Paso 1: Preparar el proyecto

### 1.1) Asegurar que tienes estructura correcta

```
proyecto-si783-2026-i-u2-enmascaradodatos/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── Procfile (o startup command)
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
└── ...
```

### 1.2) Backend: Verificar Procfile

En `backend/Procfile`:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Si no existe, créalo con ese contenido.

### 1.3) Backend: requirements.txt

```bash
cd backend
pip freeze > requirements.txt
```

Asegurate que contenga:
```
fastapi>=0.95.0
uvicorn[standard]>=0.21.0
pydantic>=1.10.0
python-dotenv>=0.21.0
motor>=3.1.0
# ... resto de dependencias
```

### 1.4) Frontend: package.json

Verifica que tienes el script de build:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}
```

### 1.5) Frontend: .env.production (opcional)

Si necesitas valores diferentes en producción:

```
VITE_API_URL=https://tu-backend.onrender.com
```

---

## Paso 2: Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Haz click en **Sign Up**
3. Inicia sesión con GitHub (recomendado)
4. Autoriza que Render acceda a tu cuenta de GitHub

---

## Paso 3: Desplegar Backend

### 3.1) Crear nuevo servicio

1. En el dashboard de Render, haz click en **New +**
2. Elige **Web Service**
3. Conecta tu repositorio de GitHub

### 3.2) Configurar el servicio Backend

```
Name: enmask-backend
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Importante**: El "Start Command" se ejecutará desde la raíz del proyecto. Si tu `backend/` está en una subcarpeta:

```
Start Command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

O mejor, usa Root Path:

```
Root Path: /backend
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3.3) Agregar variables de entorno

En la sección **Environment**, agrega:

```
API_V1_STR=/api/v1
PROJECT_NAME=Enmask SDM Platform
SECRET_KEY=una_clave_larga_y_segura_con_caracteres_aleatorios
ADMIN_EMAILS=tu_email@ejemplo.com
REPOSITORY_BACKEND=mongodb
MONGODB_META_URI=mongodb+srv://usuario:password@cluster.mongodb.net/database?retryWrites=true&w=majority
METADATA_DATABASE=enmask_meta
BACKEND_CORS_ORIGINS=https://tu-frontend.onrender.com
LOG_LEVEL=INFO
```

### 3.4) Crear el servicio

Haz click en **Create Web Service**

Render empezará a desplegar. Espera a que termine (puede tardar 5-10 minutos).

Una vez terminado, verás una URL como: `https://enmask-backend.onrender.com`

**Copia esta URL** - la necesitarás para el frontend.

---

## Paso 4: Desplegar Frontend

### 4.1) Crear nuevo servicio

1. En Render, **New +** → **Static Site**
2. Conecta el mismo repositorio

### 4.2) Configurar el servicio Frontend

```
Name: enmask-frontend
Build Command: cd frontend && npm install && npm run build
Publish Directory: frontend/dist
```

### 4.3) Agregar variables de entorno

En **Environment**:

```
VITE_API_URL=https://enmask-backend.onrender.com
```

(Reemplaza con la URL de tu backend de Render)

### 4.4) Crear el sitio estático

Haz click en **Create Static Site**

Una vez terminado, verás una URL como: `https://enmask-frontend.onrender.com`

---

## Paso 5: Verificar que funciona

1. Abre `https://enmask-frontend.onrender.com` en el navegador
2. Intenta realizar una acción que llame al backend
3. Si ves errores en consola (DevTools), revisa:
   - La URL del backend en las variables de entorno
   - Los logs del backend en Render

---

## Paso 6: Configurar Auto-Deploy (Opcional)

Por defecto, Render automáticamente re-deploya cuando haces `git push`.

Si quieres deshabilitarlo:
- En el servicio → Settings → Disable Auto-Deploy

---

## Monitorear y Troubleshoot

### Ver logs del backend

En el servicio Backend → **Logs** → verás todo lo que el servidor imprime.

### Servicios se hibernan

Para mantenerlos activos, usa [Uptime Robot](https://uptimerobot.com/):

1. Ve a uptimerobot.com → Create Monitor
2. Monitorea `https://enmask-frontend.onrender.com`
3. Intervalo: cada 5 minutos (gratis)

Esto "despierta" el servicio cada 5 minutos.

### Error: "Cannot find module"

Causas comunes:
- Archivo `requirements.txt` no actualizado
- Ruta incorrecta en "Root Path"

Solución:
```bash
cd backend
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

Render re-deployará automáticamente.

### Variables de entorno no reconocidas

1. Verifica que esté en **Environment Variables** (no en Dockerfile)
2. Re-deploya: en el servicio → **Manual Deploy** → redeploy
3. Espera a que termine

---

## Próximos pasos

1. **Configura dominio personalizado** (opcional)
   - En el servicio → **Settings** → **Custom Domain**

2. **Configura monitoring** (recomendado)
   - Ver [05-MONITOREO-LOGS.md](05-MONITOREO-LOGS.md)

3. **Configura backups de la base de datos**
   - Para produción, considera MongoDB Atlas en lugar de SQLite

---

## Comparación: Render vs Railway vs Fly.io

| Aspecto | Render | Railway | Fly.io |
|---------|--------|---------|--------|
| Facilidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Costo | Gratis (hiberna) | $5/mes | Gratis |
| BD integrada | ✅ | ✅ | ✅ |
| HTTPS | ✅ | ✅ | ✅ |
| Escalabilidad | Media | Media | Alta |

**Para empezar**: Render es la más fácil.
