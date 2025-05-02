# This is a sample Dockerfile
FROM archlinux

ENV SOURCE_DIR=/usr/share/dev
ENV MAIN_USERNAME=debian
ENV SERVER_USERNAME=public
ENV HTTPS_SERVER_WORKING_DIR=~/public
ENV HTTPS_SERVER_SOURCE=https://github.com/tubolur/servertools
ENV ALIAS_SOURCE=https://github.com/tubolur/vps_config

RUN /bin/sh -c locale-gen

CMD ["/usr/bin/bash"]

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
            nano \
            sqlite \
    && find /var/cache/pacman/ -type f -delete
    
RUN mkdir -p "$SOURCE_DIR"

RUN /sbin/useradd -m $SERVER_USERNAME
RUN echo "$SERVER_USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

#USERLAND
USER public
RUN mkdir -p "/home/$SERVER_USERNAME/dev"

# ALIASES
RUN cd "/home/$SERVER_USERNAME/dev" && git clone "$ALIAS_SOURCE" && cat vps_config/.bash_aliases "/home/$SERVER_USERNAME/.bashrc" > vps_config/.bashrc && mv vps_config/.bashrc "/home/$SERVER_USERNAME/.bashrc" && source "/home/$SERVER_USERNAME/.bashrc"

# HTTPS SERVER
RUN cd "/home/$SERVER_USERNAME/dev" && git clone "$HTTPS_SERVER_SOURCE" && cd servertools && chmod +x utils/install.sh
RUN cd "/home/$SERVER_USERNAME/dev" && cd servertools && python -m venv venv && source venv/bin/activate && pip install -r utils/requirements.txt
RUN mkdir -p "/home/$SERVER_USERNAME/public"
RUN echo "this is a test server" > "/home/$SERVER_USERNAME/public/hello.txt"
RUN echo "alias httpserver='cd /home/$SERVER_USERNAME/public && source /home/$SERVER_USERNAME/dev/servertools/venv/bin/activate && python3 /home/$SERVER_USERNAME/dev/servertools/runHTTPS.py'" >> "/home/$SERVER_USERNAME/.bashrc" && source /home/$SERVER_USERNAME/.bashrc
