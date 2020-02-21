"""Certbot command line constants"""
import sys
import os

# For help strings, figure out how the user ran us.
# When invoked from letsencrypt-auto, sys.argv[0] is something like:
# "/home/user/.local/share/certbot/bin/certbot"
# Note that this won't work if the user set VENV_PATH or XDG_DATA_HOME before
# running letsencrypt-auto (and sudo stops us from seeing if they did), so it
# should only be used for purposes where inability to detect letsencrypt-auto
# fails safely

LEAUTO = "letsencrypt-auto"
if "CERTBOT_AUTO" in os.environ:
    # if we're here, this is probably going to be certbot-auto, unless the
    # user saved the script under a different name
    LEAUTO = os.path.basename(os.environ["CERTBOT_AUTO"])

old_path_fragment = os.path.join(".local", "share", "letsencrypt")
new_path_prefix = os.path.abspath(os.path.join(os.sep, "opt",
                                               "eff.org", "certbot", "venv"))
if old_path_fragment in sys.argv[0] or sys.argv[0].startswith(new_path_prefix):
    cli_command = LEAUTO
else:
    cli_command = "certbot"


# Argparse's help formatting has a lot of unhelpful peculiarities, so we want
# to replace as much of it as we can...

# This is the stub to include in help generated by argparse
SHORT_USAGE = """
  {0} [SUBCOMMAND] [options] [-d DOMAIN] [-d DOMAIN] ...

Certbot can obtain and install HTTPS/TLS/SSL certificates.  By default,
it will attempt to use a webserver both for obtaining and installing the
certificate. """.format(cli_command)

# This section is used for --help and --help all ; it needs information
# about installed plugins to be fully formatted
COMMAND_OVERVIEW = """The most common SUBCOMMANDS and flags are:

obtain, install, and renew certificates:
    (default) run   Obtain & install a certificate in your current webserver
    certonly        Obtain or renew a certificate, but do not install it
    renew           Renew all previously obtained certificates that are near expiry
    enhance         Add security enhancements to your existing configuration
   -d DOMAINS       Comma-separated list of domains to obtain a certificate for

  %s
  --standalone      Run a standalone webserver for authentication
  %s
  --webroot         Place files in a server's webroot folder for authentication
  --manual          Obtain certificates interactively, or using shell script hooks

   -n               Run non-interactively
  --test-cert       Obtain a test certificate from a staging server
  --dry-run         Test "renew" or "certonly" without saving any certificates to disk

manage certificates:
    certificates    Display information about certificates you have from Certbot
    revoke          Revoke a certificate (supply --cert-name or --cert-path)
    delete          Delete a certificate (supply --cert-name)

manage your account:
    register        Create an ACME account
    unregister      Deactivate an ACME account
    update_account  Update an ACME account
  --agree-tos       Agree to the ACME server's Subscriber Agreement
   -m EMAIL         Email address for important account notifications
"""

# This is the short help for certbot --help, where we disable argparse
# altogether
HELP_AND_VERSION_USAGE = """
More detailed help:

  -h, --help [TOPIC]    print this message, or detailed help on a topic;
                        the available TOPICS are:

   all, automation, commands, paths, security, testing, or any of the
   subcommands or plugins (certonly, renew, install, register, nginx,
   apache, standalone, webroot, etc.)
  -h all                print a detailed help page including all topics
  --version             print the version number
"""

# These argparse parameters should be removed when detecting defaults.
ARGPARSE_PARAMS_TO_REMOVE = ("const", "nargs", "type",)


# These sets are used when to help detect options set by the user.
EXIT_ACTIONS = set(("help", "version",))


ZERO_ARG_ACTIONS = set(("store_const", "store_true",
                        "store_false", "append_const", "count",))


# Maps a config option to a set of config options that may have modified it.
# This dictionary is used recursively, so if A modifies B and B modifies C,
# it is determined that C was modified by the user if A was modified.
VAR_MODIFIERS = {"account": set(("server",)),
                 "renew_hook": set(("deploy_hook",)),
                 "server": set(("dry_run", "staging",)),
                 "webroot_map": set(("webroot_path",))}
