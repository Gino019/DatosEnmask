# QUICK START - Deploy en 15 minutos

Si quieres ir rápido, sigue esto. Para más detalles, consulta los otros documentos.

---

## ¿Cuál es tu opción favorita?

### 🟢 Opción A: Render.com (Lo más fácil)

```bash
# 1. GitHub
git add .
git commit -m "Initial commit"
git push

# 2. Ve a https://render.com → Sign up con GitHub

# 3. Backend:
# - New Web Service
# - Build: pip install -r requirements.txt
# - Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
# - Root Path: /backend
# - Add environment variables (ver .env.example)
# - Create

# 4. Frontend:
# - New Static Site
# - Build: cd frontend && npm install && npm run build
# - Publish: frontend/dist
# - Add: VITE_API_URL=<tu-backend-url>
# - Create

# ✅ Listo!
```

---

### 🔵 Opción B: Vercel + Railway (Popular)

```bash
# 1. GitHub (como arriba)

# 2. Frontend en Vercel:
# - https://vercel.com → Import Project
# - Build: cd frontend && npm run build
# - Output: frontend/dist
# - Add: VITE_API_URL

# 3. Backend en Railway:
# - https://railway.app → New Project
# - Deploy from GitHub
# - Root Path: /backend
# - Add environment variables
# - Deploy

# ✅ Listo!
```

---

### 🟡 Opción C: Fly.io (Más escalable)

```bash
# 1. Instala Fly
curl -L https://fly.io/install.sh | sh

# 2. Login
flyctl auth login

# 3. Backend
cd backend
flyctl launch
flyctl deploy

# 4. Frontend
cd ../frontend
flyctl launch
flyctl deploy

# ✅ Listo!
```

---

## Variables de entorno (todas las plataformas)

Necesitas estas 5:

```
SECRET_KEY=cualquier_valor_largo_aqui_12345678
ADMIN_EMAILS=tu_email@ejemplo.com
MONGODB_META_URI=mongodb+srv://user:pass@cluster.mongodb.net/enmask_meta
BACKEND_CORS_ORIGINS=https://tu-frontend.app
PROJECT_NAME=Enmask SDM Platform
```

Copia de `.env.example`:
```bash
cp .env.example .env
# Edita .env con tus valores
```

---

## Después del deploy

1. **Prueba tu app**
   - Frontend: https://tu-frontend.com
   - Backend: https://tu-backend.com/docs

2. **Configura Uptime Robot** (opcional)
   - https://uptimerobot.com
   - Agrega URL de frontend
   - Ping cada 5 minutos
   - Así no se hibernan

3. **Ver logs**
   - Render: Dashboard → Logs
   - Railway: Dashboard → Logs
   - Fly.io: `flyctl logs -a tu-app`

---

## 🆘 Si algo falla

### Error: "Cannot find module"
```bash
# Backend
cd backend
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update deps"
git push
# Tu plataforma re-deployará automáticamente
```

### Error: CORS
Actualiza en tu plataforma:
```
BACKEND_CORS_ORIGINS=https://tu-frontend-url.com
```

### Backend no responde
```bash
# Verifica logs
# Railway: Dashboard → Backend → Logs
# Render: Dashboard → Service → Logs
# Fly.io: flyctl logs -a enmask-backend
```

---

## Próximos pasos

Para más detalles:
- [DEPLOYMENT-ROADMAP.md](DEPLOYMENT-ROADMAP.md) - Plan completo
- [02-DEPLOYMENT-OPCIONES.md](02-DEPLOYMENT-OPCIONES.md) - Comparativa
- [05-MONITOREO-LOGS.md](05-MONITOREO-LOGS.md) - Troubleshooting

---

## ✅ Checklist

- [ ] Código en GitHub
- [ ] `.env.example` con variables
- [ ] `requirements.txt` actualizado
- [ ] `package.json` con build script
- [ ] Plataforma elegida
- [ ] Cuenta creada en plataforma
- [ ] Repo conectado
- [ ] Variables de entorno configuradas
- [ ] Deploy ejecutado
- [ ] Frontend cargando
- [ ] Backend respondiendo
- [ ] Monitoring configurado

---

**¿Listo?** Elige una opción arriba y comienza. Cualquier pregunta, ve a [05-MONITOREO-LOGS.md](05-MONITOREO-LOGS.md).
