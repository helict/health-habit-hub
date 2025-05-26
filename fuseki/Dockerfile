FROM stain/jena-fuseki:5.1.0

ADD --chown=fuseki:fuseki ./init /init

ENTRYPOINT [ "/sbin/tini", "--", "/docker-entrypoint.sh" ]
CMD sh -c \
    "/jena-fuseki/tdbloader2 --loc /fuseki/databases/hhh /init/data.ttl \
    && /jena-fuseki/fuseki-server --loc /fuseki/databases/hhh --tdb2 --update --rdfs /init/schema.ttl /hhh"

EXPOSE 3030
