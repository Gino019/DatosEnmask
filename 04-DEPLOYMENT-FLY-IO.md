# Deployment en Fly.io - Guía Paso a Paso

Fly.io es una plataforma moderna basada en contenedores. Excelente si ya tienes Dockerfiles o quieres aprender DevOps.

---

## Ventajas de Fly.io

✅ **Infrastructure moderna** (basada en Firecracker VMs)  
✅ **Plan gratuito generoso** (3 máquinas compartidas, 3 volúmenes de 3GB)  
✅ **Soporte nativo a Docker**  
✅ **Escalabilidad excelente**  
✅ **Distributed globally** (mejor rendimiento)  
✅ **Buen panel de control**  

---

## Limitaciones

> ⚠️ Plan gratuito tiene:  
> - 3 máquinas compartidas (CPU compartida)  
> - 3 volúmenes de 3GB max  
> - Memoria limitada  
> - Si necesitas más: pago desde $5-10/mes

---

## Requisitos previos

1. ✅ Proyecto en GitHub (ver [01-GUIA-GIT-GITHUB.md](01-GUIA-GIT-GITHUB.md))
2. ✅ Docker instalado localmente (para testing)
3. ✅ `Dockerfile` en backend y frontend

---

## Paso 1: Instalar Fly CLI

### Windows (PowerShell)

```powershell
# Opción A: Usando Chocolatey (si lo tienes instalado)
choco install flyctl

# Opción B: Descargar directamente
$ProgressPreference = 'SilentlyContinue'
iex (New-Object Net.WebClient).DownloadString('https://fly.io/install.ps1')

# Verificar instalación
flyctl version
```

### Alternativa: Instalador ejecutable

Ve a https://fly.io/docs/getting-started/installing-flyctl/ y descarga el instalador para Windows.

---

## Paso 2: Crear Dockerfiles (si no los tienes)

### Backend: `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para iniciar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend: `frontend/Dockerfile`

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Frontend: `frontend/nginx.conf`

```nginx
server {
    listen 80;
    server_name _;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://enmask-backend.internal;
        proxy_set_header Host $host;
    }
}
```

---

## Paso 3: Iniciar sesión en Fly

```powershell
flyctl auth login
```

Se abrirá el navegador para autenticar con GitHub o email.

---

## Paso 4: Crear app en Fly

```powershell
# Desde la raíz del proyecto
flyctl apps create enmask-platform

# Esto creará la app en Fly
```

Si es la primera vez, Fly te pedirá crear una organización. Usa el nombre por defecto.

---

## Paso 5: Desplegar Backend

### 5.1) Crear archivo `fly.toml` para backend

Desde la carpeta `backend/`:

```bash
cd backend
flyctl launch
```

Fly te preguntará:

```
? App Name: enmask-backend
? Region: [Elige el más cercano a ti, ej: sjc (San José)]
? Would you like to set up a Postgresql database now? no
? Would you like to set up an upstash redis now? no
```

Esto crea `backend/fly.toml`

### 5.2) Configurar variables de entorno

Edita `backend/fly.toml` y añade antes de `[env]`:

```toml
[env]
API_V1_STR = "/api/v1"
PROJECT_NAME = "Enmask SDM Platform"
SECRET_KEY = "una_clave_larga_y_aleatoria_aqui"
ADMIN_EMAILS = "tu_email@ejemplo.com"
REPOSITORY_BACKEND = "mongodb"
MONGODB_META_URI = "mongodb+srv://usuario:password@cluster.mongodb.net/database"
METADATA_DATABASE = "enmask_meta"
BACKEND_CORS_ORIGINS = "https://enmask-frontend.fly.dev"
LOG_LEVEL = "INFO"
```

### 5.3) Desplegar

```powershell
cd backend
flyctl deploy
```

Fly construirá la imagen Docker y deployará. Espera 5-10 minutos.

Una vez terminado:

```
https://enmask-backend.fly.dev
```

**Copia esta URL** para el frontend.

---

## Paso 6: Desplegar Frontend

### 6.1) Crear app para frontend

```powershell
cd ../frontend
flyctl launch
```

Configuración similar:

```
? App Name: enmask-frontend
? Region: [Mismo que el backend]
? Databases: no
? Redis: no
```

### 6.2) Configurar variables

Edita `frontend/fly.toml`:

```toml
[env]
VITE_API_URL = "https://enmask-backend.fly.dev"
```

### 6.3) Desplegar

```powershell
flyctl deploy
```

Una vez terminado:

```
https://enmask-frontend.fly.dev
```

---

## Paso 7: Verificar conexión

1. Abre `https://enmask-frontend.fly.dev`
2. Abre DevTools (F12)
3. Ve a Network y prueba una acción que llame al backend
4. Si hay CORS errors, actualiza `BACKEND_CORS_ORIGINS` en backend

---

## Monitoreo y Logs

### Ver logs en tiempo real

```powershell
# Backend
flyctl logs -a enmask-backend

# Frontend
flyctl logs -a enmask-frontend
```

### Ver estado de la app

```powershell
flyctl status -a enmask-backend
```

### Escalar a múltiples máquinas

```powershell
flyctl scale count 2 -a enmask-backend
```

---

## Actualizar después de cambios

Cuando hagas `git push`:

```powershell
# Backend
cd backend
flyctl deploy

# Frontend
cd ../frontend
flyctl deploy
```

O configura GitHub Actions (avanzado) para auto-deploy.

---

## Configurar dominio personalizado

```powershell
# Agregar dominio
flyctl certs create midominio.com -a enmask-backend

# Esto te dará registros DNS que debes agregar a tu DNS provider
```

---

## Troubleshooting

### Error: "build failed"

```powershell
# Ver logs del build
flyctl logs -a enmask-backend
```

Causas comunes:
- `requirements.txt` incompleto
- Dockerfile con ruta incorrecta

Solución:

```powershell
cd backend
pip freeze > requirements.txt
flyctl deploy
```

### App está lenta

Fly en plan gratuito usa CPU compartida. Para mejorar:

```powershell
# Escalar a máquina dedicada ($10/mes)
flyctl machine create -a enmask-backend --vm-memory 256
```

### CORS errors

El backend rechaza solicitudes desde el frontend. Actualiza en backend `fly.toml`:

```toml
BACKEND_CORS_ORIGINS = "https://enmask-frontend.fly.dev"
```

Luego:

```powershell
flyctl deploy
```

---

## Comparación: Costos Fly.io

| Plan | Precio | Máquinas | Memoria |
|------|--------|----------|---------|
| **Gratuito** | $0 | 3 compartidas | Limitada |
| **Starter** | $5-10/mes | 1 dedicada | 256 MB |
| **Scale** | $15+/mes | Varias | 512 MB+ |

---

## Próximos pasos

1. **Monitoreo avanzado**: Ver [05-MONITOREO-LOGS.md](05-MONITOREO-LOGS.md)
2. **Database persistent**: Configura un volumen Fly
3. **CI/CD con GitHub Actions**: Auto-deploy en cada `git push`

---

## Recursos útiles

- [Fly.io Docs](https://fly.io/docs/)
- [Fly CLI Reference](https://fly.io/docs/flyctl/cmd/)
- [Pricing](https://fly.io/docs/about/pricing/)
