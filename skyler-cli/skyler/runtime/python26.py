import shutil
import logging
import tempfile
import tarfile

import os
from skyler.conf import CONFIG
from skyler.db import Session, Deployment, Application, DEPLOYMENT_STATE_STARTED, DEPLOYMENT_STATE_BUILT_OK
from skyler.clients.docker_client import Docker
from skyler.utils import SkylerException


log = logging.getLogger(__name__)


class Runtime(object):
    def __init__(self, application_name):
        session = Session()
        self.application = session.query(Application). \
            filter(Application.name == application_name).first()
        if not self.application:
            log.error("No application found")
            raise SkylerException("No application found")

        self.deployment = None
        self.params = {'run_script': 'runapp.sh',
                       'setup_script': 'setupapp.sh',
                       'base_image': 'skyler-python26'}
        self.configurations = {}

    def pack_env(self):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tar = tarfile.open(fileobj=tmp, mode='w:gz')
        tar.add(self.application.source, '.')
        tar.close()
        tmp.flush()
        tmp.close()
        log.debug('packed {}'.format(tmp.name))
        self.params['packed_env'] = tmp.name

    def build_templates(self, configuration):
        b_dir = tempfile.mkdtemp()
        dockerfile = os.path.join(CONFIG.get('base', 'templates'), 'dockerfile')
        runapp = os.path.join(CONFIG.get('base', 'templates'), 'runapp_{}.sh'.format('python26'))
        setupapp = os.path.join(CONFIG.get('base', 'templates'), 'setup_{}.sh'.format('python26'))
        log.debug('generating templates')
        params = self.params.copy()
        params['command'] = self.configurations[configuration]

        shutil.move(self.params['packed_env'], os.path.join(b_dir, 'env.tgz'))
        params['packed_env'] = 'env.tgz'

        dockerfile_content = file(dockerfile).read().format(**params)
        runapp_content = file(runapp).read().format(**params)
        setupapp_content = file(setupapp).read().format(**params)
        with file(os.path.join(b_dir, 'Dockerfile'), 'w') as f:
            f.write(dockerfile_content)
        with file(os.path.join(b_dir, 'runapp.sh'), 'w') as f:
            f.write(runapp_content)
        with file(os.path.join(b_dir, 'setupapp.sh'), 'w') as f:
            f.write(setupapp_content)
        log.debug('template directory complete {}'.format(b_dir))
        return b_dir

    def start_deploy(self):
        session = Session()
        d = Deployment(application_id=self.application.id,
                       state=DEPLOYMENT_STATE_STARTED)
        session.add(d)
        session.commit()
        self.deployment = d
        session.flush()

        log.info('deployment {} <{}> #{}'.format(self.application.name, self.application.source, d.id))
        self.configurations = self.inspect_env()
        self.pack_env()

        b_dir = self.build_templates('web')
        self.build_image(b_dir, 'web')

        d.state = DEPLOYMENT_STATE_BUILT_OK
        session.add(d)
        session.commit()

    def inspect_env(self):
        ret = {}
        procfile = file(os.path.join(self.application.source, 'Procfile')).readlines()
        for name, cmd in ((x[:x.find(':')], x[x.find(':') + 1:]) for x in procfile):
            ret[name.strip()] = cmd.strip()
        return ret

    def build_image(self, b_dir, config):
        log.info('building image...')
        docker = Docker.client
        template = '{}_{}_d{}'.format(
            self.application.name, config, self.deployment.id)
        new_image = docker.build(b_dir, template)[0]
        log.info('image built {}'.format(new_image))
        registry_image = '{}/{}'.format(CONFIG.get('base', 'docker-registry'), template)
        docker.tag(new_image, registry_image)
        log.info('pushing to registry {}'.format(registry_image))
        docker.push(registry_image)
        log.debug('finished')
        self.deployment.image = template
