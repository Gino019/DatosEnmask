# Monitoreo, Logs y Troubleshooting

Guía para monitorear tu aplicación en producción y solucionar problemas comunes.

---

## Parte 1: Monitoreo Básico

### ¿Por qué monitorear?

- Detectar errores antes que los usuarios
- Saber si el servidor está up/down
- Entender performance y uso de recursos
- Prevenir hibernación (Render) o inactividad

---

## 1.1) Uptime Robot (Gratuito)

Mantiene tus servicios "despiertos" haciendo ping cada X minutos.

### Pasos

1. Ve a [uptimerobot.com](https://uptimerobot.com)
2. Crea una cuenta gratis
3. New Monitor:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Enmask Backend
   - **URL**: `https://tu-backend.onrender.com/health` (o tu URL)
   - **Monitoring Interval**: 5 minutos
   - Click Create Monitor

4. Repite para Frontend:
   - **URL**: `https://tu-frontend.onrender.com`

Ahora:
✅ Tu app nunca hibernará (se despierta cada 5 min)  
✅ Recibirás alertas si algo falla  
✅ Verás estadísticas de uptime  

---

## 1.2) Monitoreo en Vercel

Si usas Vercel:

1. Dashboard → Proyecto → Analytics
2. Ver:
   - Requests por día
   - Errors
   - Response times

---

## 1.3) Monitoreo en Railway

Si usas Railway:

1. Dashboard → Servicio Backend → **Metrics**
2. Ver:
   - CPU
   - Memory
   - Requests

---

## Parte 2: Ver Logs

### Logs en Render

```
1. Dashboard → Servicio → Logs
2. Filtra por nivel (Error, Info, Debug)
3. Busca palabras clave
```

### Logs en Railway

```
1. Dashboard → Servicio Backend → Logs
2. En tiempo real ves qué está ocurriendo
```

### Logs en Fly.io

```bash
flyctl logs -a enmask-backend   # Backend
flyctl logs -a enmask-frontend  # Frontend
```

---

## Parte 3: Errores Comunes

### Error 502 Bad Gateway

**Causas**:
- Backend offline
- Backend tardando más de 30 segundos
- Memoria agotada

**Solución**:
```bash
# 1. Revisar logs del backend
# 2. Verificar que CORS está bien configurado
# 3. Escalar recursos
```

### Error 503 Service Unavailable

**Causas**:
- Servidor hibernado (Render)
- Base de datos desconectada
- Demasiadas solicitudes

**Solución**:
```bash
# 1. Esperar 30 segundos a que despierte
# 2. Verificar conexión a MongoDB
# 3. Aumentar timeout
```

### CORS Error en consola

```
Access to XMLHttpRequest at 'https://...' from origin 
'https://...' has been blocked by CORS policy
```

**Solución**:

Backend `fly.toml` o variables de entorno:
```
BACKEND_CORS_ORIGINS = "https://tu-frontend.com"
```

Luego redeploya.

### Error: Cannot read property 'xxx' of undefined

**Causas**:
- Backend no devolviendo JSON esperado
- Frontend no validando respuesta

**Solución**:
```bash
# 1. Abre DevTools → Network
# 2. Inspecciona la respuesta del backend
# 3. Compara con lo esperado en el código
```

### Base de datos desconectada

**Error típico**:
```
pymongo.errors.ServerSelectionTimeoutError: 
connection attempt failed
```

**Causas**:
- URI de MongoDB incorrecta
- IP no whitelisted
- Credenciales expiradas

**Solución**:
```bash
# 1. Verifica MONGODB_META_URI es correcta
# 2. En MongoDB Atlas → Network Access → Allow current IP
# 3. Redeploya
```

---

## Parte 4: Health Checks

Agrega un endpoint `/health` en tu backend para monitoring:

### Backend: `app/api/v1/health.py`

```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
```

### Backend: `app/main.py`

```python
from app.api.v1 import health

app.include_router(health.router)
```

Ahora puedes:
- Ping a `https://tu-backend.com/health`
- Usar en Uptime Robot
- Detectar problemas rápidamente

---

## Parte 5: Logging Centralizado

Para aplicaciones grandes, usa un servicio de logging centralizado.

### Opciones gratuitas:

| Servicio | Plan Gratuito | Ideal para |
|----------|--------------|-----------|
| **Sentry** | 5000 errors/mes | Error tracking |
| **LogRocket** | 1GB/mes | Session replay |
| **ELK Stack** | Self-hosted | Logs centralizados |

### Ejemplo: Sentry

1. Ve a [sentry.io](https://sentry.io), crea cuenta
2. Create Project → Python
3. Copia el DSN
4. En backend, instala:

```bash
pip install sentry-sdk
```

5. En `app/main.py`:

```python
import sentry_sdk

sentry_sdk.init(
    dsn="tu-dsn-aqui",
    traces_sample_rate=0.1
)
```

Ahora todos los errores se envían a Sentry automáticamente.

---

## Parte 6: Alertas

### Email alerts (Uptimerobot)

1. Dashboard → New Alert Contact
2. Email → Ingresa tu email
3. Save

Ahora recibiras emails si algo falla.

### Slack alerts (Avanzado)

1. Crea webhook en Slack
2. Integra con tu app o Sentry
3. Recibe notificaciones en tiempo real

---

## Parte 7: Performance

### Medir performance

**Frontend**:
- Abre DevTools → Lighthouse
- Run audit
- Ve qué optimizar

**Backend**:
- Agrega timing en logs:

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Optimizaciones rápidas

**Frontend**:
- ✅ Comprimir imágenes
- ✅ Code splitting
- ✅ Lazy loading
- ✅ Minificar CSS/JS

**Backend**:
- ✅ Indexar base de datos
- ✅ Caché en Redis
- ✅ Paginación
- ✅ Async/await

---

## Parte 8: Backup y Disaster Recovery

### Backup de base de datos MongoDB

```bash
# Local (manual)
mongodump --uri="tu-uri" --out backup/

# Restaurar
mongorestore --uri="tu-uri" backup/
```

### Backup automático en MongoDB Atlas

1. MongoDB Atlas → Backup → Edit Backup Settings
2. Enable Automated Backup
3. Retención: 7 días (gratis)

---

## Parte 9: Checklist de producción

Antes de ir a producción, verifica:

- [ ] ✅ HTTPS activado
- [ ] ✅ CORS configurado correctamente
- [ ] ✅ Variables de entorno seguros
- [ ] ✅ Database credenciales seguras
- [ ] ✅ Health check endpoint activo
- [ ] ✅ Logs configurados
- [ ] ✅ Uptime monitoring activado
- [ ] ✅ Backup automático
- [ ] ✅ Error tracking (Sentry)
- [ ] ✅ Performance monitoreado

---

## Parte 10: Escalabilidad

### Cuando tu app crece:

1. **Aumentar recursos**:
   - Railway: escala a 2 dyno
   - Render: plan pagado
   - Fly.io: múltiples máquinas

2. **Caché**:
   - Redis para sesiones
   - CDN para assets

3. **Base de datos**:
   - Índices optimizados
   - Read replicas

4. **Contenedores**:
   - Kubernetes (escalabilidad profesional)

---

## Recursos útiles

- [Uptime Robot](https://uptimerobot.com)
- [Sentry Error Tracking](https://sentry.io)
- [MongoDB Backup Guide](https://docs.mongodb.com/manual/core/backups/)
- [FastAPI Logging](https://fastapi.tiangolo.com/advanced/logging/)

---

## Siguiente: Configurar CI/CD

Ver: [GitHub Actions para Auto-Deploy](https://docs.github.com/en/actions)
