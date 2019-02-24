
# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = "Comet Guide"

WELCOME = _("Welcome to Comet Guide!")
HELP = _("Ask something to hear about the university of texas at dallas  and its services... Currently I can answer you housing, alumni, counseling related queries... So... which option would you like to go for?")
ABOUT = _("Comet guide is the virtual guide that will help you with your queries with respect to campus services.")
STOP = _("Okay, see you next time!")
GENERIC_REPROMPT = _("What can I help you with?")

MY_API = {
    "host": "3.17.130.148",
    "port": 80,
    "path": "/question",
}