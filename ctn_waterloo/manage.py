import subprocess

from flask.ext.script import Manager, Server

from . import app
from .freezer import freezer


manager = Manager(app, with_default_commands=False)

manager.add_command('run', Server(host="0.0.0.0"))


@manager.command
def freeze(serve=False):
    """Freezes the static version of the website."""
    if serve:
        freezer.run(debug=True)
    else:
        urls = freezer.freeze()
        print 'Built %i files.' % len(urls)


@manager.command
def up(destination, link=None):
    print '### Freezing'
    freeze()
    print '### Uploading to', destination
    subprocess.call(['rsync', '-Pah', '--del', freezer.root + '/', destination])

    if link is not None:
        destparts = destination.split(':')
        print '### Linking', link
        subprocess.call(['ssh', destparts[0],
                         "'ln -s " + link + " " + destparts[1] + "'"])


@manager.shell
def shell_context():
    from . import app, pages
    from .freezer import freezer
    return locals()


if __name__ == '__main__':
    manager.run()
