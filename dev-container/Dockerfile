FROM ubuntu:23.04

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
  apt-get autoremove && \
  apt-get autoclean 

RUN wget https://github.com/neovim/neovim/releases/download/stable/nvim-linux64.tar.gz && \
  tar xvf nvim-linux64.tar.gz && \
  cp -Rp nvim-linux64/. /usr/local/ && \
  rm -rf nvim-linux64*

RUN LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[0-9.]+') && \
  curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz" && \
  tar xf lazygit.tar.gz -C /usr/local/bin lazygit && \
  rm -f lazygit.tar.gz

# Allow Lunarvim to install dependencies
RUN rm -f /usr/lib/python3.*/EXTERNALLY-MANAGED

# Configure groups and user
RUN if ! grep ":${GROUPID}:" /etc/group; then groupadd -g $GROUPID user; fi && \
    useradd -l -m -u ${USERID} -g ${GROUPID} -s /usr/bin/zsh user && \
    echo "user    ALL=(ALL)       NOPASSWD:ALL" > /etc/sudoers.d/user

USER user

WORKDIR /home/user

# Going to get an error on zap install but it's ok
RUN wget https://raw.githubusercontent.com/zap-zsh/zap/master/install.zsh && \
  zsh ./install.zsh --branch release-v1 || true && \
  rm -f ./install.zsh

RUN LV_BRANCH='release-1.3/neovim-0.9' && \
  wget https://raw.githubusercontent.com/LunarVim/LunarVim/release-1.3/neovim-0.9/utils/installer/install.sh && \
  bash ./install.sh --install-dependencies -y && \
  rm -f install.sh

# Aliases
RUN zoxide init zsh >> ~/.zshrc && \
cat >> ~/.zshrc <<'EOF'
#plug romkatv/powerlevel10k
export PATH=/home/user/.local/bin:$PATH
alias grep=rg
alias cat=bat
alias vi=lvim
alias vim=lvim
alias ls=lsd
alias cd=z
EOF


