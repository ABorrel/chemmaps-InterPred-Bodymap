
FROM mcs07/postgres-rdkit

# build rdkit from source
# - http://www.rdkit.org/docs/Install.html#building-from-source
# - https://github.com/InformaticsMatters/rdkit_cartridge/blob/master/Dockerfile
# - https://github.com/rdkit/conda-rdkit/blob/master/rdkit/build.sh
# - https://github.com/rdkit/homebrew-rdkit/blob/master/Formula/rdkit.rb
# - https://raw.githubusercontent.com/rdkit/rdkit/master/Code/PgSQL/rdkit/README
# RUN apt-get update && \
#     apt-get install -y \
#         wget unzip cmake \
#         postgresql-server-dev-9.6 \
#         build-essential python-numpy cmake python-dev sqlite3 libsqlite3-dev \
#         libboost-dev libboost-all-dev libboost-system-dev libboost-thread-dev \
#         libboost-serialization-dev libboost-python-dev libboost-regex-dev \
#         libeigen3-dev libcairo2-dev && \
#     \
#     apt-get clean

# RUN cd /tmp && \
#     wget https://github.com/rdkit/rdkit/archive/Release_2017_09_3.zip && \
#     unzip Release_2017_09_3.zip && \
#     mkdir -p /tmp/rdkit-Release_2017_09_3/build && \
#     cd /tmp/rdkit-Release_2017_09_3/build && \
#     cmake  \
#     -D RDK_BUILD_INCHI_SUPPORT=ON \
#         -D RDK_BUILD_AVALON_SUPPORT=ON \
#         -D RDK_BUILD_THREADSAFE_SSS=ON \
#         -D RDK_BUILD_CAIRO_SUPPORT=ON \
#         -D RDK_BUILD_PGSQL=ON\
#         -D RDK_TEST_MULTITHREADED=ON \
#         -D PostgreSQL_ROOT=/usr/lib/postgresql/9.6 \
#         -D PostgreSQL_TYPE_INCLUDE_DIR=/usr/include/postgresql/9.6/server \
#         -D CMAKE_BUILD_TYPE=Release \
#        	.. \
#     && make -j7 \
#     && make install && \
#     sh ./Code/PgSQL/rdkit/pgsql_install.sh && \
#     cd ~ \
#    rm /tmp/Release_2017_09_3.zip && \
#    rm -rf /tmp/rdkit-Release_2017_09_3

# data dump
COPY compose/postgres/data/ChemMap_Dec.dump /docker-entrypoint-initdb.d/ChemMap_Dec.dump

# add postgres config
COPY compose/postgres/postgresql.conf /etc/postgresql/postgresql.conf

# ENV PGDATA=/data
# make them executable
#RUN chmod +x /usr/local/bin/app-backups && \
 

