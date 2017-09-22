Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.box_version = "2.3.1"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder ".", "/var/hermercury"
  config.vm.provision :shell, name: "setup", path: "environment/setup.sh"
end
