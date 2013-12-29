# vim: set ft=ruby

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network :private_network, ip:"10.0.5.10"
  config.cache.auto_detect = true

#  config.vm.forward_port 80, 8888

  config.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--memory", "2048"]
    v.name = "Skyler-Devstack"
    v.gui = true
  end

  config.vm.provision "shell",
    path: "scripts/openstack.sh"

end
