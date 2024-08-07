# Neovim doesn't currently provide a aarch64 package for ubuntu 
# so we build our own.
FROM ubuntu:23.10 as NEOVIM
USER root

ARG NEOVIM_VERSION=v0.10.0

RUN apt update && \
  apt install -y ninja-build gettext cmake unzip curl wget git file

WORKDIR /tmp

RUN wget --secure-protocol=TLSv1_2 https://github.com/neovim/neovim/archive/refs/tags/${NEOVIM_VERSION}.zip && \
  unzip *.zip 

RUN cd neovim* && \
  make CMAKE_BUILD_TYPE=RelWithDebInfo && \
  cd build && cpack -G DEB && dpkg -i nvim-linux64.deb

FROM ubuntu:23.10

ARG LVIM_BRANCH=1.4.0

# Use a unique and high id for both group and user.
ARG GROUPID=10000
ARG USERID=10000

RUN apt update && \
  apt install -y curl gpg && \
  mkdir -p /etc/apt/keyrings && \
  curl -fsSL https://repo.charm.sh/apt/gpg.key | gpg --dearmor -o /etc/apt/keyrings/charm.gpg && \
  echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" >> /etc/apt/sources.list.d/charm.list && \
  apt update && \
  apt install -y git python3 pip python-is-python3 make npm nodejs cargo wget zsh \
  sudo lsd zoxide bat mosh glow fzf tree ripgrep tmux jq && \
  apt purge -y rustc && \
  apt-get autoremove -y && \
  apt-get clean 

COPY --from=NEOVIM /tmp/neovim*/build/nvim-linux64.deb /tmp

RUN apt install -f /tmp/nvim-linux64.deb && rm -f /tmp/nvim-linux64.deb

RUN if [ "$(uname -m)" = "aarch64" ]; then LAZYGIT_ARCH=arm64; else LAZYGIT_ARCH=x86_64; fi && \
  LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[0-9.]+') && \
  curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_${LAZYGIT_ARCH}.tar.gz" && \
  tar xf lazygit.tar.gz -C /usr/local/bin lazygit && \
  rm -f lazygit.tar.gz

# Allow Lunarvim to install dependencies
RUN rm -f /usr/lib/python3.*/EXTERNALLY-MANAGED

# Configure groups and user
RUN if ! grep ":user:" /etc/group; then groupadd -g $GROUPID user; fi && \
   if ! grep ":user:" /etc/passwd; then useradd -l -m -u ${USERID} -g ${GROUPID} -s /usr/bin/zsh user; fi && \
    echo "user    ALL=(ALL)       NOPASSWD:ALL" > /etc/sudoers.d/user

USER user

WORKDIR /home/user

RUN curl --proto '=https' --tlsv1.3 -o install.sh https://sh.rustup.rs -sSf && \
  bash ./install.sh -q -y && \
  rm -f ./install.sh

# Going to get an error on zap install but it's ok
RUN wget https://raw.githubusercontent.com/zap-zsh/zap/master/install.zsh && \
  zsh ./install.zsh --branch release-v1 || true && \
  rm -f ./install.zsh

RUN . "$HOME/.cargo/env" && \
  curl -so /tmp/install.sh https://raw.githubusercontent.com/LunarVim/LunarVim/${LVIM_BRANCH}/utils/installer/install.sh && \
  bash /tmp/install.sh --install-dependencies -y && \
  rm -f install.sh

# Aliases
RUN zoxide init zsh >> ~/.zshrc && \
echo '\n \
#plug romkatv/powerlevel10k
export PATH=/home/user/.local/bin:$PATH \n\
alias cat=bat \n\
alias vi=lvim \n\
alias vim=lvim \n\
alias ls=lsd \n\
alias cd=z\n' \
>> ~/.zshrc


