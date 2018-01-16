# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

# config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
  config.vm.provider "virtualbox" do |vb|
     # Display the VirtualBox GUI when booting the machine
     vb.gui = false
  #   # Customize the amount of memory on the VM:
     vb.memory = "4096"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y htop curl wget git git-core zsh vim tmux python3-pip httpie jq exuberant-ctags sqlite3
    pip3 install virtualenv
    pip3 install --upgrade pip
  SHELL

  config.vm.provision "shell", privileged:false, inline: <<-SHELL
    echo $USER
    if [ ! -d ".oh-my-zsh" ]; then
      wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
    fi
    sudo chsh -s `which zsh`
    if [ ! -d "dotfiles" ]; then
      git clone http://github.com/IngoS11/dotfiles
    fi
    cp $HOME/dotfiles/.vimrc $HOME 
    cp $HOME/dotfiles/.zshrc $HOME
    cp $HOME/dotfiles/.tmux.conf $HOME
    cp -r $HOME/dotfiles/.vim $HOME
    cd /vagrant
    make env/setup
    source env/bin/activate
    make pip/update
    make db/setup
  SHELL

  config.vm.provision "shell", inline: "chsh -s /usr/bin/zsh vagrant"

end
