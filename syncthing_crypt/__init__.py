#!/usr/bin/env python
import os
import sys
import logging
import click
name = 'syncthing-crypt'
logger = logging.getLogger('syncthing-crypt')
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger(name)
PACKAGE_HOME=os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    """First paragraph.

    This is a very long second paragraph and as you
    can see wrapped very early in the source text
    but will be rewrapped to the terminal width in
    the final output.

    \b
    This is
    a paragraph
    without rewrapping.

    And this is a paragraph
    that will be rewrapped again.
    """
    level = os.environ.get('LOG_LEVEL','INFO').upper()
    if hasattr(logging,level): logger.setLevel(getattr(logging,level))
    if debug: logger.setLevel(logging.DEBUG)
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command('serve',short_help='serve the web frontend')
def serve():
    try:
        logger.info(PACKAGE_HOME)
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    sys.exit(0)

@cli.command('install',short_help='install the service')
def install(**kwargs):
    logger.info("install")

@cli.command('uninstall',short_help='uninstall the service')
def uninstall(**kwargs):
    if click.confirm('Do you want to uninstall %s?'%name):
        logger.info("uninstall")

@cli.command('enable',short_help='enable the service autostart')
def enable(**kwargs):
    logger.info("enable")

@cli.command('disable',short_help='disable the service autostart')
def disable(**kwargs):
    logger.info("disable")

@cli.command('start',short_help='start the service')
def start(**kwargs):
    logger.info("enable")

@cli.command('stop',short_help='stop the service')
def stop(**kwargs):
    logger.info("enable")

@cli.command('edit',short_help='edit the service defaults')
def edit(**kwargs):
    DEFAULTS_FILE='/etc/default/syncthing-crypt'
    click.edit(filename=DEFAULTS_FILE)
    click.echo('Edit: %s' % click.format_filename(DEFAULTS_FILE))
    if click.confirm('restart services?', default=True):
        stop()
        start()

__all__ = ['cli']

if __name__ == '__main__':
    cli()
