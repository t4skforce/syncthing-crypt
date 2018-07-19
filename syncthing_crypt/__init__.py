#!/usr/bin/env python
import os
import sys
import logging
import click
from .lib import ClickIPAddress, ClickValidation, ClickLinuxUser
name = 'syncthing-crypt'
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger(name)
PACKAGE_HOME=os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


@click.group(invoke_without_command=True)
@click.option('-d','--debug', is_flag=True, default=False, help='enable debug level logging')
@click.option('-i','--interactive', is_flag=True, default=True, help='enable interactive mode',show_default=True)
@click.pass_context
def cli(ctx,debug,interactive):
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
    if ctx.obj is None: ctx.obj={}
    level = os.environ.get('LOG_LEVEL','INFO').upper()
    if hasattr(logging,level): logger.setLevel(getattr(logging,level))
    if debug: logger.setLevel(logging.DEBUG)
    logger.info('Debug mode is %s' % ('on' if debug else 'off'))
    ctx.obj['debug']=debug
    ctx.obj['interactive']=interactive
    if ctx.invoked_subcommand is None:
        with click.Context(cli) as ctx:
            click.echo(cli.get_help(ctx))


@cli.group(name='run', invoke_without_command=True, short_help='starts the server in interactive mode')
@click.option('-f','--foreground', is_flag=True, default=True, help='keep process in foregound',show_default=True)
@click.pass_context
def run(ctx,foreground):
    ctx.obj['foreground']=foreground
    if ctx.invoked_subcommand is None:
        with click.Context(run) as ctx:
            click.echo(run.get_help(ctx))

@run.command('backend', short_help='starts the backend server, requires root permissions')
@click.option('-s','--ssl', is_flag=True, default=False, help='enable ssl encyption for server',show_default=True)
@click.option('-l','--listen', default='127.0.0.1', help='configure listening interface for server', type=ClickIPAddress(),show_default=True)
@click.option('-p','--port', default=8079, help='configure port to listen on', type=click.IntRange(1,65535),show_default=True)
@click.pass_context
def run_backend(ctx,ssl,listen,port):
    ClickValidation.bindFree(listen,port)
    ClickValidation.requireRoot(ctx)
    if listen != '127.0.0.1':
        logger.warn('Running the backend server on to the internet is not a good idea, the process is running with root permissions! [%s:%s]'%(listen,port))
        if ssl == False:
            logger.warn('Running the backend server without ssl is not recommended! [%s:%s]'%(listen,port))
    logger.info('starting backend %s'%([ctx,listen,port],))

@run.command('frontend', short_help='starts the frontend server')
@click.option('-s','--ssl', default=True, is_flag=True, help='enable ssl encyption for server',show_default=True)
@click.option('-l','--listen', default='0.0.0.0', help='configure listening interface for server', type=ClickIPAddress(),show_default=True)
@click.option('-p','--port', default=8080, help='configure port to listen on', type=click.IntRange(1,65535),show_default=True)
@click.option('-u','--user',envvar='USER', help='user to run the server as',type=ClickLinuxUser(),show_default=True)
@click.option('-h','--home',envvar='HOME', help='home folder to use for the server',type=click.Path(exists=True,writable=True),show_default=True)
@click.pass_context
def run_frontend(ctx,ssl,listen,port,user,home):
    ClickValidation.bindFree(listen,port)
    if user == 'root':
        raise click.UsageError('The command "%s" requires to be a non root user "su - <user> -c" or provide a different user!'%(ctx.info_name,),ctx)
    logger.info('starting frontend %s'%([ctx,ssl,listen,port,user,home],))

@cli.group(name='service', invoke_without_command=True, short_help='manage local service status')
@click.pass_context
def service(ctx):
    if ctx.invoked_subcommand is None:
        with click.Context(service) as ctx:
            click.echo(service.get_help(ctx))

@service.command('install',short_help='install the service')
@click.pass_context
def install(ctx):
    logger.info("install")

@service.command('uninstall',short_help='uninstall the service')
@click.pass_context
def uninstall(ctx):
    if click.confirm('Do you want to uninstall %s?'%name):
        logger.info("uninstall")

@service.command('enable',short_help='enable the service autostart')
@click.pass_context
def enable(ctx):
    logger.info("enable")

@service.command('disable',short_help='disable the service autostart')
@click.pass_context
def disable(ctx):
    logger.info("disable")

@service.command('start',short_help='start the service')
@click.pass_context
def start(ctx):
    logger.info("enable")

@service.command('stop',short_help='stop the service')
@click.pass_context
def stop(ctx):
    logger.info("enable")

@cli.command('edit',short_help='edit the service defaults')
@click.pass_context
def edit(ctx):
    DEFAULTS_FILE='/etc/default/syncthing-crypt'
    click.edit(filename=DEFAULTS_FILE)
    click.echo('Edit: %s' % click.format_filename(DEFAULTS_FILE))
    if click.confirm('restart services?', default=True):
        pass

__all__ = ['cli']

if __name__ == '__main__':
    cli()
