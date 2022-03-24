ARG mysql_version

FROM mysql:${mysql_version}

COPY ./chinook/*.sql /docker-entrypoint-initdb.d/
