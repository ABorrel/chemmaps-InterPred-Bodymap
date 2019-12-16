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
        supervisor \
        openbabel \
        default-jre \
        dirmngr \
    && apt-get clean

COPY ./compose/django/marvin_linux_19.11.deb /marvin_linux_19.11.deb

#RUN wget https://github.com/kmansouri/OPERA/releases/download/v2.4-beta5/OPERA2.4_CL_mcr.tar.gz && \
#    tar -xzvf OPERA2.3_CL_mcr.tar.gz

COPY compose/django/OPERA2.4_CL_mcr.tar.gz /OPERA2.4_CL_mcr.tar.gz
    
RUN tar -xzvf /OPERA2.4_CL_mcr.tar.gz && \
    /OPERA2_CL_mcr/OPERA2.4_CL_mcr.install -mode silent -agreeToLicense yes

#RUN apt install /marvin_linux_19.11.deb -y
#RUN rm -R OPERA2_CL_mcr && \
#    rm marvin_linux_19.11.deb

RUN echo "LD_LIBRARY='/usr/local/MATLAB/MATLAB_Runtime/v94/'" >> ~/.bashrc && \
    echo "alias opera='/usr/local/bin/OPERA/application/run_OPERA.sh $LD_LIBRARY'"

RUN echo "deb http://cran.rstudio.com/bin/linux/debian stretch-cran34/" >> /etc/apt/sources.list && \
    apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF' && \
    apt update && \
    apt install r-base -y

RUN echo "install.packages(\"randomForest\", repos=\"https://cran.rstudio.com\")" | R --no-save && \
    echo "install.packages(\"MASS\", repos=\"https://cran.rstudio.com\")" | R --no-save


RUN mkdir -p /app/logs && mkdir /app/project && \
    mkdir -p /tmp/interferences/ && groupadd -r django && \
    useradd -r -g django django

COPY compose/django/entrypoint.sh /app/project/entrypoint.sh
COPY requirements.txt ./requirements.txt
COPY conda.env /conda.env

RUN conda env create --name chemmaps -f /conda.env  && \
    . /opt/conda/etc/profile.d/conda.sh && \
    conda activate chemmaps && \
    pip install -U pip && \
    pip install -r /requirements.txt && \
    chmod +x /app/project/entrypoint.sh && \
    chown django /app/project/entrypoint.sh

# RUN chmod +x /app/project/entrypoint.sh && \
#     chown django /app/project/entrypoint.sh && \
#     pip install -U pip && \
#     pip install -r /requirements.txt

COPY src /app/project

RUN chown -R django /app
#USER django

WORKDIR /app/project

EXPOSE 8000

ENTRYPOINT ["/app/project/entrypoint.sh"]
