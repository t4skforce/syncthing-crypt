import click
import ipaddress
import os, socket, errno

class ClickValidation:
    def __init__(self):
        pass

    @staticmethod
    def isRoot():
        return os.getuid() == 0;

    @staticmethod
    def requireRoot(ctx):
        if os.getuid() != 0:
            raise click.UsageError('The command "%s" requires root permissions to run try using "sudo"!'%(ctx.info_name),ctx)

    @staticmethod
    def requireNonRoot(ctx):
        if os.getuid() == 0:
            raise click.UsageError('The command "%s" requires to be a non root user "sudo"!'%(ctx.info_name),ctx)

    @staticmethod
    def bindFree(ip,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((ip, port))
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                raise click.BadParameter('Invalid "--port" given port is already being used error:%s'%str(e))
            else:
                raise click.BadParameter('Invalid "--port" given error:%s'%str(e))
        finally:
            try:
                s.close()
            except:
                pass
