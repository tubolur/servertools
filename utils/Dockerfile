# This is a sample Dockerfile
FROM archlinux

ENV SOURCE_DIR=/usr/share/dev
ENV MAIN_USERNAME=debian
ENV SERVER_USERNAME=public
ENV HTTPS_SERVER_WORKING_DIR=~/public
ENV HTTPS_SERVER_SOURCE=https://github.com/tubolur/servertools

RUN pacman -Syu --noconfirm \
            wget \
    && find /var/cache/pacman/ -type f -delete

RUN pacman -Sy --noconfirm \
            freetype2 \
            gcc \
            git \
            make \
            python \
            python-virtualenv \
            sudo \
    && find /var/cache/pacman/ -type f -delete
    
RUN mkdir -p "$SOURCE_DIR"

RUN /sbin/useradd -m $SERVER_USERNAME\

USER $MAIN_USERNAME
RUN mkdir -p "~/downloads"
cd "~/downloads"
RUN git clone $HTTPS_SERVER_SOURCE
RUN cd servertools
RUN chmod +x utils/install.sh
RUN ./utils/install.sh

USER SERVER_USERNAME
CMD ["httpsserver"]


