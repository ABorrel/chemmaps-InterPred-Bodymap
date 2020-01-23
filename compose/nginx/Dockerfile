FROM nginx:1.17.4-alpine
EXPOSE 8003
RUN rm /etc/nginx/conf.d/default.conf
COPY compose/nginx/nginx.conf /etc/nginx/conf.d