import click
import ipaddress
import pwd
import grp

class ClickIPAddress(click.ParamType):
    name = 'ipaddress'

    def get_metavar(self, param):
        return '[IP]'

    def convert(self, value, param, ctx):
        try:
            return str(ipaddress.ip_address(value))
        except ValueError:
            self.fail('"%s" is not a valid IP Address' % value, param, ctx)

    def __repr__(self):
        return 'IPAddress'

class ClickLinuxUser(click.ParamType):
    name = 'linuxuser'

    def get_metavar(self, param):
        return '[USER]'

    def convert(self, value, param, ctx):
        try:
            pwd.getpwnam(str(value))
            return str(value)
        except KeyError:
            self.fail('User "%s" does not exist' % value, param, ctx)

class ClickLinuxGroup(click.ParamType):
    name = 'linuxgroup'

    def get_metavar(self, param):
        return '[GROUP]'

    def convert(self, value, param, ctx):
        try:
            grp.getgrnam(str(value))
            return str(value)
        except KeyError:
            self.fail('Group "%s" does not exist' % value, param, ctx)
