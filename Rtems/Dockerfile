FROM ubuntu:22.04

RUN apt-get update -y && \
    apt-get install -y git \
        curl \
        python3 \
        python3-dev \
        gcc \
        g++ \
        flex \
        bison \
        make \
        bzip2 \
        unzip \
        xz-utils

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN mkdir -p /development/src
WORKDIR $HOME/development/src

RUN git clone git://git.rtems.org/rtems-source-builder.git rsb
RUN git clone git://git.rtems.org/rtems.git

WORKDIR /development/src/rsb/rtems
RUN ../source-builder/sb-set-builder --prefix=$HOME/development/rtems/6 6/rtems-sparc

RUN export PATH=/development/rtems/6/bin:"$PATH"

WORKDIR /development/src/rtems
RUN echo "[sparc/leon3]" > config.ini && echo "BUILD_TESTS = True" >> config.ini
RUN ./waf configure ---prefix=/development/rtems/6
RUN ./waf
RUN ./waf install

RUN mkdir -p /development/app/hello
WORKDIR /development/app/hello

RUN curl https://waf.io/waf-2.0.10 > waf && chmod +x waf

RUN git init
RUN git submodule add git://git.rtems.org/rtems_waf.git rtems_waf
# RUN git clone --branch bugfix/catch-stop-iteration https://github.com/fingercracker/rtems_waf.git rtems_waf

COPY hello.c ./
COPY init.c ./
COPY wafscript ./

RUN ./waf configure --rtems=/development/rtems/6 --rtems-bsp=sparc/leon3
RUN ./waf

CMD ["tail", "-f", "/dev/null"]

