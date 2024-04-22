FROM stain/jena-fuseki:4.8.0

ADD --chown=fuseki:fuseki ./init /init

EXPOSE 3030