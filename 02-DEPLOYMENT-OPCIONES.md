# Opciones de Deployment Gratuitas - Comparativa

Este documento compara las diferentes plataformas de hosting gratuitas para desplegar tu aplicación Enmask (Frontend + Backend).

---

## Tabla Comparativa

| Plataforma | Frontend | Backend | Base de Datos | Costo | Dificultad | Escalabilidad |
|-----------|----------|---------|--------------|-------|-----------|--------------|
| **Vercel + Railway** | ✅ | ✅ | ✅ (MongoDB) | Gratis | Fácil | Media |
| **Render.com** | ✅ | ✅ | ✅ | Gratis | Fácil | Media |
| **Fly.io** | ✅ | ✅ | ✅ | Gratis | Media | Alta |
| **Docker en VPS** | ✅ | ✅ | ✅ | Bajo (~$5-10/mes) | Difícil | Alta |
| **GitHub Pages** | ✅ | ❌ | N/A | Gratis | Fácil | Baja |
| **Netlify** | ✅ | ❌ | N/A | Gratis | Fácil | Media |

---

## Opción 1: Vercel + Railway (⭐ RECOMENDADO)

### Descripción
- **Frontend**: React/Vite en Vercel
- **Backend**: FastAPI en Railway
- **Base de datos**: MongoDB Atlas (gratis con limitaciones)

### Ventajas
✅ Frontend deployado al borde (CDN global)  
✅ Backend simple de configurable  
✅ Perfecta integración con GitHub  
✅ Fácil scalabilidad  
✅ Planes gratuitos generosos  

### Desventajas
❌ Railway tiene límites de tiempo de ejecución (5 horas gratuitas al mes)  
❌ Requiere 2 servicios (Frontend y Backend en plataformas diferentes)  

### Costo
- **Vercel**: Gratis (hasta 100GB de ancho de banda/mes)
- **Railway**: Gratis (solo $ 5 USD de crédito mensual)
- **MongoDB Atlas**: Gratis (5GB almacenamiento)

### Guía completa
→ Ver [DEPLOY_VERCEL_RAILWAY_GUIA.md](DEPLOY_VERCEL_RAILWAY_GUIA.md)

---

## Opción 2: Render.com

### Descripción
- Todo en una sola plataforma
- Frontend y Backend en el mismo lugar
- Base de datos incluida

### Ventajas
✅ Simplicidad: todo en un lugar  
✅ Buen plan gratuito  
✅ Soporte a múltiples lenguajes (Node, Python, Go, etc.)  
✅ Incluye PostgreSQL/MySQL gratis  
✅ Actualizaciones automáticas  

### Desventajas
❌ Los servicios gratuitos se hibernan después de 15 minutos sin uso  
❌ Menos opciones de customización que Vercel  

### Costo
- **Render**: Gratis (con limitaciones)
- Pago: desde $7/mes

### Guía completa
→ Ver [03-DEPLOYMENT-RENDER.md](03-DEPLOYMENT-RENDER.md)

---

## Opción 3: Fly.io

### Descripción
- Plataforma de contenedores
- Deploy directo de Docker
- Excelente para aplicaciones escalables

### Ventajas
✅ Infraestructura moderna y confiable  
✅ Soporte a Docker nativamente  
✅ Plan gratuito muy competitivo  
✅ Excelente para microservicios  
✅ Buen rendimiento global  

### Desventajas
❌ Curva de aprendizaje más alta  
❌ Requiere configurar variables de entorno manualmente  

### Costo
- **Fly.io**: Gratis (3 máquinas compartidas, 3 volúmenes de 3GB)

### Guía completa
→ Ver [04-DEPLOYMENT-FLY-IO.md](04-DEPLOYMENT-FLY-IO.md)

---

## Opción 4: Docker en VPS (DigitalOcean, Hetzner, Contabo)

### Descripción
- Tu propio servidor con Docker
- Control total sobre la infraestructura
- Ideal para producción completa

### Ventajas
✅ Control total  
✅ Mejor rendimiento  
✅ Escalabilidad ilimitada  
✅ Costo muy bajo (~$5-10/mes)  
✅ Ideal para proyectos a largo plazo  

### Desventajas
❌ Requiere más conocimiento de DevOps  
❌ Mantenimiento manual del servidor  
❌ Responsabilidad de seguridad y backups  

### Costo
- **DigitalOcean Droplet**: $5/mes
- **Hetzner Cloud**: €3-5/mes
- **Contabo**: desde €4/mes

### Guía completa
→ Ver [DESPLIEGUE_DOCKER_INTERNET.md](DESPLIEGUE_DOCKER_INTERNET.md)

---

## Opción 5: Solo Frontend (GitHub Pages, Netlify, Vercel)

### Descripción
Solo si necesitas desplegar el frontend (sin backend).

### Plataformas
- **GitHub Pages**: Gratis, integración nativa
- **Netlify**: Gratis, con preview automáticos
- **Vercel**: Gratis, optimizado para Vite

### Limitaciones
❌ No puedes tener backend  
❌ Solo para contenido estático  
❌ Funciones serverless limitadas en plan gratuito  

---

## 🎯 Recomendación por Caso

### Para comenzar / Prototipo
→ **Vercel + Railway** o **Render.com**
- Fácil de configurar
- Perfecto para aprender
- Escalable si crece el proyecto

### Para producción con presupuesto bajo
→ **Docker en VPS (DigitalOcean)**
- Costo muy bajo
- Control total
- Escalable

### Para máxima facilidad
→ **Render.com**
- Todo integrado
- Mínima configuración
- Soporte excelente

### Para mejor performance global
→ **Fly.io** o **Vercel + Railway**
- Infraestructura distribuida
- Buen CDN

---

## Próximos pasos

1. **Lee primero**: [01-GUIA-GIT-GITHUB.md](01-GUIA-GIT-GITHUB.md)
   - Necesitas tu proyecto en GitHub antes de desplegar

2. **Elige una opción** y sigue la guía específica:
   - Vercel + Railway → [DEPLOY_VERCEL_RAILWAY_GUIA.md](DEPLOY_VERCEL_RAILWAY_GUIA.md)
   - Render.com → [03-DEPLOYMENT-RENDER.md](03-DEPLOYMENT-RENDER.md)
   - Fly.io → [04-DEPLOYMENT-FLY-IO.md](04-DEPLOYMENT-FLY-IO.md)
   - Docker VPS → [DESPLIEGUE_DOCKER_INTERNET.md](DESPLIEGUE_DOCKER_INTERNET.md)

3. **Configurar variables de entorno**
   - Copia `.env.example` → `.env.production`
   - Rellena los valores para producción

4. **Monitorear y troubleshoot**
   - Ver [05-MONITOREO-LOGS.md](05-MONITOREO-LOGS.md)

---

## Tabla de Recursos

| Servicio | Link | Plan Gratuito |
|----------|------|--------------|
| **GitHub** | https://github.com | Repositorios ilimitados |
| **Vercel** | https://vercel.com | 100GB ancho de banda/mes |
| **Railway** | https://railway.app | $5 crédito mensual |
| **Render** | https://render.com | Hiberna después de 15 min |
| **Fly.io** | https://fly.io | 3 máquinas compartidas |
| **MongoDB Atlas** | https://www.mongodb.com/cloud/atlas | 5GB |
| **DigitalOcean** | https://www.digitalocean.com | $200 crédito x 60 días (nuevo) |
| **Hetzner Cloud** | https://www.hetzner.com/cloud | Prueba gratuita |

---

## Dudas frecuentes

**P: ¿Cuál es la más barata?**  
R: Para corto plazo, Vercel + Railway. Para largo plazo, VPS ($5/mes).

**P: ¿Cuál escala mejor?**  
R: Fly.io o Docker en VPS.

**P: ¿Cuál es más fácil para empezar?**  
R: Render.com (todo integrado).

**P: ¿Puedo cambiar de plataforma después?**  
R: Sí, solo necesitas reconfigurar las variables de entorno y variables en GitHub.
