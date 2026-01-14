## Despliegue a producción

Contruir la imagen de Docker para el backend de Django:
```bash
docker build -t django-backend .
```
O bien, construir todas las imágenes definidas en el archivo de composición de Docker para producción:
```bash
docker compose -f docker-compose.prod.yml build
```

Levantar los servicios en modo producción:
```bash
docker-compose -f docker-compose.prod.yml up -d
```