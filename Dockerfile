FROM odoo:19

USER root

# Custom addons: copied into the path already present in the default
# addons_path of this image (/mnt/extra-addons)
COPY ./library /mnt/extra-addons/library
COPY ./portfolio /mnt/extra-addons/portfolio

# Custom start script (see DEPLOY.md for why it exists). The sed strips
# Windows line endings in case the file was edited on Windows.
COPY start.sh /start.sh
RUN sed -i 's/\r$//' /start.sh \
    && chown -R odoo:odoo /mnt/extra-addons \
    && chmod +x /start.sh

USER odoo

EXPOSE 8069

CMD ["/start.sh"]
