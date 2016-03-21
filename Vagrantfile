# -*- mode: ruby -*-
# vi: set ft=ruby :

MESSAGE = <<-MESSAGE
WELCOME to

      ######   #######     #     #     #  #     #
      #     #  #          # #    #     #   #   #
      #     #  #         #   #   #     #    # #
      ######   #####    #     #  #     #     #
      #     #  #        #######   #   #      #
      #     #  #        #     #    # #       #
      ######   #######  #     #     #        #

  #----------------------------------------------------#
  #                                                    #
  #  If you need any help, feel free to chat us up at  #
  #                                                    #
  #      https://gitter.im/beavyHQ/beavy               #
  #                                                    #
  #----------------------------------------------------#

You can now log into your development enviroment via

    vagrant ssh

and in there start all processes in a tmux session via

    ./start.sh


----
Glad to have you on board, champ!
    Have fun!

MESSAGE

# The list of packages we want to install
INSTALL = <<-INSTALL
sudo apt-get update
sudo apt-get install -y postgresql-9.4 postgresql-client-9.4 postgresql-server-dev-9.4 redis-server python3 python3-pip python3-virtualenv virtualenv nodejs npm zsh git tmux libffi-dev libncurses5-dev xvfb chromedriver chromium build-essential libssl-dev curl git-core

INSTALL

# Provising on the system and user level
SETUP = <<-SETUP

# prepare database
sudo -u postgres createuser vagrant
sudo -u postgres createdb -O vagrant beavy-dev

# fix postgres config
sudo cp /vagrant/.infrastructure/vagrant/pg_hba.conf /etc/postgresql/9.4/main/pg_hba.conf
sudo /etc/init.d/postgresql reload

# make sure chrome & chromedriver are accessible
sudo ln -s /usr/bin/chromium /usr/bin/chrome
sudo ln -s /usr/lib/chromium/chromedriver /usr/bin/chromedriver

# install latest nvm to vagrant
git clone git://github.com/creationix/nvm.git /home/vagrant/.nvm
. /home/vagrant/.nvm/nvm.sh

# install latest stable node
nvm install stable
nvm alias default stable

# make sure npm is up to date
sudo npm install -g npm

# set user bash to zsh
sudo chsh -s /bin/zsh vagrant

# create the virualenv for vagrant
sudo -u vagrant virtualenv -p python3 /home/vagrant/venv

SETUP

Vagrant.configure(2) do |config|
  config.vm.box = "debian/jessie64"
  config.vm.post_up_message = MESSAGE

  config.vm.network "forwarded_port", guest: 2992, host: 2992
  config.vm.network "private_network", ip: "10.1.1.10"

  # tuned options for best webpack watch performance, see
  # https://blog.inovex.de/doh-my-vagrant-nfs-is-slow/
  config.vm.synced_folder ".", "/vagrant",  type: 'nfs', mount_options: ['rw', 'vers=3', 'tcp', 'fsc' ,'actimeo=1']

  config.vm.provision "shell", inline: INSTALL
  config.vm.provision "shell", path: ".infrastructure/install_icu.sh"
  config.vm.provision "shell", inline: SETUP

  # add local git and zsh config
  config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  config.vm.provision "file", source: ".infrastructure/vagrant/zshrc", destination: "~/.zshrc"

end
