# nginx/Dockerfile
FROM nginx:1.25-alpine

# Удаляем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# Копируем наш конфиг
COPY nginx.conf /etc/nginx/conf.d

# Nginx будет слушать на порту 80 внутри контейнера
EXPOSE 80