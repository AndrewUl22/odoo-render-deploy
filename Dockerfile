FROM odoo:19

# Render injects env vars at runtime, but the official Odoo image expects
# the DB password via a file or the PASSWORD env var — both are supported
# by its entrypoint script, so no extra wiring is needed here.

USER root

# Custom addons: copied into the path already present in the default
# addons_path of this image (/mnt/extra-addons)
COPY ./library /mnt/extra-addons/library
COPY ./portfolio /mnt/extra-addons/portfolio

RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo

EXPOSE 8069
