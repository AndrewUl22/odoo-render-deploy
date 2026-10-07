FROM odoo:19

USER root

# Custom addons: copied into the path already present in the default
# addons_path of this image (/mnt/extra-addons)
COPY ./library /mnt/extra-addons/library
COPY ./portfolio /mnt/extra-addons/portfolio

# Custom start script: passes DB connection args explicitly (DB_HOST,
# DB_PORT, DB_USER, DB_PASSWORD) and binds Odoo's HTTP server to whatever
# port Render assigns via $PORT — avoids relying on the base image's
# auto env-var mapping, whose variable names (HOST/PORT/USER/PASSWORD)
# collide with Render's own reserved $PORT.
COPY start.sh /start.sh
RUN chown -R odoo:odoo /mnt/extra-addons && chmod +x /start.sh

USER odoo

EXPOSE 8069

CMD ["/start.sh"]
