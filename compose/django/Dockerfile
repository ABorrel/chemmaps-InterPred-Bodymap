FROM continuumio/miniconda3:4.4.10

RUN apt-get update && \
    mkdir -p /usr/share/man/man1  && \
    apt-get install -y \
        zip \
        unzip \
        wget \
        wkhtmltopdf \
        libaio1 \
        libpq-dev \
        openbabel \
        default-jre \
        dirmngr \
    && apt-get clean

COPY compose/django/OPERA2.4_CL_mcr.tar.gz /OPERA2.4_CL_mcr.tar.gz
COPY compose/django/marvin_linux_20.1_openjdk11.deb /marvin_linux_20.1_openjdk11.deb

RUN dpkg -i /marvin_linux_20.1_openjdk11.deb

RUN tar -xzvf /OPERA2.4_CL_mcr.tar.gz && \
    ./OPERA2_CL_mcr/OPERA2.4_CL_mcr.install -mode silent -agreeToLicense yes

RUN echo "deb http://cran.rstudio.com/bin/linux/debian stretch-cran34/" >> /etc/apt/sources.list && \
    apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF' && \
    apt update && \
    apt install r-base -y

RUN echo "install.packages(\"randomForest\", repos=\"https://cran.rstudio.com\")" | R --no-save && \
    echo "install.packages(\"MASS\", repos=\"https://cran.rstudio.com\")" | R --no-save


RUN mkdir -p /app/logs && mkdir /app/project && \
    mkdir -p /tmp/interferences/ && groupadd -r django && \
    useradd -r -g django django

COPY compose/django/entrypoint.sh /entrypoint.sh
COPY requirements.txt ./requirements.txt
COPY conda.env /conda.env

RUN conda env create --name chemmaps -f /conda.env  && \
    . /opt/conda/etc/profile.d/conda.sh && \
    conda activate chemmaps && \
    pip install -U pip && \
    pip install -r /requirements.txt && \
    chmod +x /entrypoint.sh && \
    chown django:django /entrypoint.sh

RUN chown -R django:django /app
#USER django
WORKDIR /app/project
EXPOSE 8001
ENTRYPOINT ["/entrypoint.sh"]

