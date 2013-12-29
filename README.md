# Skyler

PaaS prototype based on OpenStack + Heat and Docker

## Usage

```
vagrant plugin install vagrant-cachier
vagrant up
```

## Exports

export OS_TENANT_NAME=demo
export OS_USERNAME=admin
export OS_PASSWORD=pass
export OS_AUTH_URL=http://127.0.0.1:5000/v2.0
glance image-list

