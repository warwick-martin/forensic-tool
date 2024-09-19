# Use the official Python base image
FROM debian
SHELL ["/bin/bash", "-c"]

COPY . /app

# Set up working directory
WORKDIR /app

# Install required packages and dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Rye
RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash && echo 'source "$HOME/.rye/env"' >> ~/.bashrc

# Install Node.js (latest version)
RUN wget -qO- https://get.pnpm.io/install.sh | ENV="$HOME/.bashrc" SHELL="$(which bash)" bash -
RUN source ~/.bashrc && pnpm env use --global latest

WORKDIR /app/ui
RUN source ~/.bashrc && pnpm i

WORKDIR /app
RUN source ~/.bashrc && rye sync

# By default, run a shell
#CMD ["bash"]
ENTRYPOINT ["/app/entrypoint.sh"]
