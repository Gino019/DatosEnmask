# Roadmap de Deployment - Plan Completo

Este documento es tu guía paso a paso para deployar Enmask en producción.

---

## 📋 Tabla de Contenidos

1. [Checklist Pre-Deploy](#checklist-pre-deploy)
2. [Opción A: Vercel + Railway (Recomendado)](#opción-a-vercel--railway-recomendado)
3. [Opción B: Render.com (Más Simple)](#opción-b-rendercom-más-simple)
4. [Opción C: Fly.io (Más Escalable)](#opción-c-flyio-más-escalable)
5. [Opción D: Docker en VPS (Más Control)](#opción-d-docker-en-vps-más-control)

---

## ✅ Checklist Pre-Deploy

Antes de cualquier opción, completa esto:

### 1. Preparar el código

- [ ] ✅ Backend `requirements.txt` actualizado
  ```bash
  cd backend && pip freeze > requirements.txt
  ```

- [ ] ✅ Frontend `package.json` con scripts de build
  ```json
  "scripts": {
    "build": "tsc && vite build"
  }
  ```

- [ ] ✅ `.gitignore` con archivos sensibles

- [ ] ✅ `.env.example` en la raíz con todas las variables

### 2. Git + GitHub

- [ ] ✅ Proyecto bajo control Git
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  ```

- [ ] ✅ Repositorio en GitHub
  ```bash
  git remote add origin https://github.com/TU_USUARIO/repo.git
  git push -u origin main
  ```

→ **Guía completa**: [01-GUIA-GIT-GITHUB.md](01-GUIA-GIT-GITHUB.md)

### 3. Preparar variables de entorno

- [ ] ✅ MongoDB Atlas cuenta (gratuita)
  - Ve a [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
  - Crea cluster gratuito
  - Copia la URI de conexión

- [ ] ✅ Genera SECRET_KEY segura
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

- [ ] ✅ Prepara valores para:
  - `ADMIN_EMAILS`
  - `BACKEND_CORS_ORIGINS` (será tu URL de frontend)
  - `PROJECT_NAME`

---

## 🚀 Opción A: Vercel + Railway (⭐ RECOMENDADO)

### Ventajas
- Frontend en Vercel (excelente rendimiento)
- Backend en Railway (simple de usar)
- Muy popular en la industria
- Perfecto para aprender

### Tiempo estimado: 30 minutos

### Pasos

**Paso 1: Vercel (Frontend)**

1. Ve a [vercel.com](https://vercel.com)
2. Sign up con GitHub
3. Import Project
4. Selecciona tu repositorio
5. Configure:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Environment Variables**:
     ```
     VITE_API_URL=https://tu-backend.up.railway.app
     ```
6. Click Deploy

Tu frontend estará en: `https://tu-app.vercel.app`

**Paso 2: Railway (Backend)**

1. Ve a [railway.app](https://railway.app)
2. Sign up con GitHub
3. Create Project
4. Deploy from GitHub repo
5. Configure:
   - **Root Path**: `/backend` (o el path de tu backend)
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables (todas las de `.env.example`)
7. Click Deploy

Tu backend estará en: `https://tu-backend.up.railway.app`

**Paso 3: Actualizar CORS en Backend**

1. Ve a Railway → Backend → Variables
2. Actualiza `BACKEND_CORS_ORIGINS`:
   ```
   BACKEND_CORS_ORIGINS=https://tu-app.vercel.app
   ```
3. Redeploy

→ **Guía detallada**: [DEPLOY_VERCEL_RAILWAY_GUIA.md](DEPLOY_VERCEL_RAILWAY_GUIA.md)

---

## 🎯 Opción B: Render.com (Más Simple)

### Ventajas
- Todo en una plataforma
- Excelente para aprender
- Muy fácil de configurar

### Limitación
- Servicios se hibernan después de 15 minutos inactivos

### Tiempo estimado: 25 minutos

### Pasos

1. Ve a [render.com](https://render.com)
2. Sign up con GitHub
3. Crea Web Service para Backend
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Variables de entorno (ver `.env.example`)
4. Crea Static Site para Frontend
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`
   - VITE_API_URL = URL del backend

→ **Guía detallada**: [03-DEPLOYMENT-RENDER.md](03-DEPLOYMENT-RENDER.md)

---

## ⚡ Opción C: Fly.io (Más Escalable)

### Ventajas
- Infraestructura moderna
- Excelente performance
- Muy buen plan gratuito
- Ideal si quieres aprender DevOps

### Tiempo estimado: 40 minutos

### Pasos

1. Instala Fly CLI
2. `flyctl auth login`
3. `cd backend && flyctl launch` → Deploy backend
4. `cd ../frontend && flyctl launch` → Deploy frontend
5. Configura variables de entorno en `fly.toml`
6. `flyctl deploy` para cada servicio

→ **Guía detallada**: [04-DEPLOYMENT-FLY-IO.md](04-DEPLOYMENT-FLY-IO.md)

---

## 🖥️ Opción D: Docker en VPS (Más Control)

### Ventajas
- Control total
- Mejor rendimiento
- Muy económico (~$5/mes)
- Ideal para producción profesional

### Tiempo estimado: 1-2 horas (primera vez)

### Requisitos
- Dominio propio (opcional pero recomendado)
- VPS (DigitalOcean $5/mes)

### Pasos

1. Compra VPS en DigitalOcean/Hetzner
2. Conecta SSH y configura servidor
3. Instala Docker y Docker Compose
4. Clona tu repositorio
5. Configura `.env` con valores de producción
6. `docker-compose up -d`

→ **Guía detallada**: [DESPLIEGUE_DOCKER_INTERNET.md](DESPLIEGUE_DOCKER_INTERNET.md)

---

## 🛡️ Post-Deploy

Una vez deployado, configura:

### 1. Monitoreo

```bash
# Usar Uptime Robot para evitar hibernación
# Ve a uptimerobot.com y configura un monitor
# Ping cada 5 minutos a tu aplicación
```

### 2. Logs y Debugging

```bash
# Ver logs según tu plataforma:
# Vercel: Dashboard → Deployments → Logs
# Railway: Dashboard → Backend → Logs  
# Render: Dashboard → Service → Logs
# Fly.io: flyctl logs -a tu-app
```

→ **Guía completa**: [05-MONITOREO-LOGS.md](05-MONITOREO-LOGS.md)

### 3. Health Checks

Agrega un endpoint `/health` en tu backend para facilitar el monitoring.

---

## 📊 Matriz de decisión

¿Cuál opción elegir?

```
¿Es tu primer deploy?
  ├─ SÍ, quiero lo más simple
  │  └─ → Render.com (Opción B)
  │
  ├─ SÍ, pero prefiero 2 plataformas
  │  └─ → Vercel + Railway (Opción A)
  │
  └─ NO, quiero aprender DevOps
     └─ → Fly.io (Opción C) o Docker VPS (Opción D)

¿Tienes presupuesto?
  ├─ NO, quiero gratis totalmente
  │  └─ → Render, Fly.io o Vercel+Railway
  │
  └─ SÍ, ~$5-10/mes está bien
     └─ → Docker en VPS (mejor rendimiento)

¿Necesitas máximo rendimiento?
  ├─ NO, está bien con hibernación
  │  └─ → Render o Vercel+Railway
  │
  └─ SÍ, debe estar siempre rápido
     └─ → Fly.io o Docker en VPS
```

---

## 🔄 Workflow de Desarrollo

Una vez deployado, tu workflow es:

```bash
# 1. Hacer cambios locales
git add .
git commit -m "Feature: xyz"

# 2. Subir a GitHub
git push

# 3. El deploy es automático en:
# - Vercel: redeploya frontend
# - Railway: redeploya backend  
# - Render: redeploya ambos
# - Fly.io: necesitas `flyctl deploy`
# - VPS: necesitas manual o GitHub Actions
```

---

## 🆘 Troubleshooting Rápido

| Error | Causa | Solución |
|-------|-------|----------|
| 502 Bad Gateway | Backend offline | Ver logs, verificar variables |
| 503 Service Unavailable | Hibernado | Esperar 30 seg o usar Uptime Robot |
| CORS Error | Frontend rechazado | Actualizar `BACKEND_CORS_ORIGINS` |
| Cannot find module | `requirements.txt` incompleto | `pip freeze > requirements.txt` |
| Connection refused | BD desconectada | Verificar MongoDB URI |

→ **Más detalles**: [05-MONITOREO-LOGS.md](05-MONITOREO-LOGS.md#parte-3-errores-comunes)

---

## 📚 Documentos de Referencia

| Documento | Contenido |
|-----------|----------|
| [01-GUIA-GIT-GITHUB.md](01-GUIA-GIT-GITHUB.md) | Cómo subir proyecto a GitHub |
| [02-DEPLOYMENT-OPCIONES.md](02-DEPLOYMENT-OPCIONES.md) | Comparativa de plataformas |
| [03-DEPLOYMENT-RENDER.md](03-DEPLOYMENT-RENDER.md) | Render.com paso a paso |
| [04-DEPLOYMENT-FLY-IO.md](04-DEPLOYMENT-FLY-IO.md) | Fly.io paso a paso |
| [05-MONITOREO-LOGS.md](05-MONITOREO-LOGS.md) | Logs, monitoring, troubleshooting |
| [DEPLOY_VERCEL_RAILWAY_GUIA.md](DEPLOY_VERCEL_RAILWAY_GUIA.md) | Vercel + Railway paso a paso |
| [DESPLIEGUE_DOCKER_INTERNET.md](DESPLIEGUE_DOCKER_INTERNET.md) | Docker en VPS paso a paso |
| [.env.example](.env.example) | Template de variables |

---

## ✨ Resumen

1. **Prepara tu código** → [01-GUIA-GIT-GITHUB.md](01-GUIA-GIT-GITHUB.md)
2. **Elige una opción** → [02-DEPLOYMENT-OPCIONES.md](02-DEPLOYMENT-OPCIONES.md)
3. **Sigue la guía específica** → 03, 04, DEPLOY_VERCEL, DESPLIEGUE_DOCKER
4. **Configura monitoreo** → [05-MONITOREO-LOGS.md](05-MONITOREO-LOGS.md)

---

## 🎯 Próximos pasos

- [ ] Seguir guía Git → [01-GUIA-GIT-GITHUB.md](01-GUIA-GIT-GITHUB.md)
- [ ] Elegir plataforma → [02-DEPLOYMENT-OPCIONES.md](02-DEPLOYMENT-OPCIONES.md)
- [ ] Ejecutar deployment
- [ ] Configurar monitoreo
- [ ] Celebrar! 🎉
