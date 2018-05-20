#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
An incomplete sample script.

This is not a complete bot; rather, it is a template from which simple
bots can be made. You can rename it to mybot.py, then edit it in
whatever way you want.

Use global -simulate option for test purposes. No changes to live wiki
will be done.

The following parameters are supported:

&params;

-always           If used, the bot won't ask if it should file the message
                  onto user talk page.

-text:            Use this text to be added; otherwise 'Test' is used

-replace:         Dont add text but replace it

-top              Place additional text on top of the page

-summary:         Set the action summary message for the edit.
"""
#
# (C) Pywikibot team, 2006-2016
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

__version__ = '$Id: c1795dd2fb2de670c0b4bddb289ea9d13b1e9b3f $'
#

import pywikibot, re, urllib
from pywikibot import pagegenerators, textlib

from pywikibot.textlib import _MultiTemplateMatchBuilder
from pywikibot.bot import (
    SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot)
from pywikibot.tools import issue_deprecation_warning

# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}


class BasicBot(
    # Refer pywikobot.bot for generic bot classes
    SingleSiteBot,  # A bot only working on one site
    # CurrentPageBot,  # Sets 'current_page'. Process it in treat_page method.
    #                  # Not needed here because we have subclasses
    ExistingPageBot,  # CurrentPageBot which only treats existing pages
    NoRedirectPageBot,  # CurrentPageBot which only treats non-redirects
    AutomaticTWSummaryBot,  # Automatically defines summary; needs summary_key
):

    """
    An incomplete sample bot.

    @ivar summary_key: Edit summary message key. The message that should be used
        is placed on /i18n subdirectory. The file containing these messages
        should have the same name as the caller script (i.e. basic.py in this
        case). Use summary_key to set a default edit summary message.
    @type summary_key: str
    """

    summary_key = 'basic-changing'

    def __init__(self, generator, **kwargs):
        """
        Constructor.

        @param generator: the page generator that determines on which pages
            to work
        @type generator: generator
        """
        # Add your own options to the bot and set their defaults
        # -always option is predefined by BaseBot class
        self.availableOptions.update({
            'replace': False,  # delete old text and write the new text
            'summary': None,  # your own bot summary
            'text': 'Test',  # add this text from option. 'Test' is default
            'top': False,  # append text on top of the page
        })

        # call constructor of the super class
        super(BasicBot, self).__init__(site=True, **kwargs)

        # handle old -dry paramter
        self._handle_dry_param(**kwargs)

        # assign the generator to the bot
        self.generator = generator

    def _handle_dry_param(self, **kwargs):
        """
        Read the dry parameter and set the simulate variable instead.

        This is a private method. It prints a deprecation warning for old
        -dry paramter and sets the global simulate variable and informs
        the user about this setting.

        The constuctor of the super class ignores it because it is not
        part of self.availableOptions.

        @note: You should ommit this method in your own application.

        @keyword dry: deprecated option to prevent changes on live wiki.
            Use -simulate instead.
        @type dry: bool
        """
        if 'dry' in kwargs:
            issue_deprecation_warning('dry argument',
                                      'pywikibot.config.simulate', 1)
            # use simulate variable instead
            pywikibot.config.simulate = True
            pywikibot.output('config.simulate was set to True')

    def treat_page(self):
        """Load the given page, do some changes, and save it."""
        text = self.current_page.text

        ################################################################
        #                           výjimky                            #
        ################################################################

        #exceptions = ['comment', 'math', 'nowiki', 'pre', 'startspace', 'table', 'template']
        exceptions = ['comment','nowiki','pre']

        ################################################################
        #                           shrnutí                            #
        ################################################################

        #shrnuti = self.getOption('summary')
        shrnuti = 'doplnění chybějící šablony překlad'

        ################################################################
        #                            regexy                            #
        ################################################################

        soubor = urllib.request.urlopen('https://tools.wmflabs.org/urbanecmbot/test/preklads.txt')
        radky = soubor.readlines()
        nahrady = {}
        for radek in radky:
            nahrady[str(radek.split(b'\t')[0],'utf-8')] = str(radek.split(b'\t')[1].rstrip(),'utf-8')
        
        preklad = nahrady[self.current_page.title(underscore=True)]

        if re.search(r'(?i)== *Reference *==', text):
            text = textlib.replaceExcept(text, r'(?i)==(=?) *Reference *===?\s*', r'==\1 Reference ==\1\n' + preklad + r'\n', exceptions)
        elif re.search(r'(?i)== *Poznámky *==', text):
            text = textlib.replaceExcept(text, r'(?i)==(=?) *Poznámky *===?\s+(.*)\s*', r'==\1 Poznámky ==\1\n\2\n\n==\1 Reference ==\1\n' + preklad + r'\n\n', exceptions)
        elif re.search(r'(?i)== *(Literatura|Související články|Externí odkazy) *==', text):
            text = textlib.replaceExcept(text, r'(?i)\s*==(=?) *(Literatura|Související články|Externí odkazy) *===?', r'\n\n==\1 Reference ==\1\n' + preklad + r'\n\n==\1 \2 ==\1', exceptions, count=1)
        elif re.search(r'(?i)\{\{(Autoritní data|Portály|DEFAULTSORT)[^\}]*\}\}', text):
            text = textlib.replaceExcept(text, r'(?i)\s*\{\{((Autoritní data|Portály|DEFAULTSORT)[^\}]*)\}\}', r'\n\n== Reference ==\n' + preklad + r'\n\n{{\1}}', exceptions, count=1)
        elif re.search(r'(?i)\[\[Kategorie:[^\]]*\]\]', text):
            text = textlib.replaceExcept(text, r'(?i)\s*\[\[Kategorie:([^\]]*)\]\]', r'\n\n== Reference ==\n' + preklad + r'\n\n[[Kategorie:\1]]', exceptions, count=1)
        else:
            text = text + '\n\n== Reference ==\n' + preklad

        ################################################################
        self.put_current(text, summary='Robot: ' + shrnuti)


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    options = {}
    # Process global arguments to determine desired site
    local_args = pywikibot.handle_args(args)

    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    genFactory = pagegenerators.GeneratorFactory()

    # Parse command line arguments
    for arg in local_args:

        # Catch the pagegenerators options
        if genFactory.handleArg(arg):
            continue  # nothing to do here

        # Now pick up your own options
        arg, sep, value = arg.partition(':')
        option = arg[1:]
        if option in ('summary', 'text'):
            if not value:
                pywikibot.input('Please enter a value for ' + arg)
            options[option] = value
        # take the remaining options as booleans.
        # You will get a hint if they aren't pre-definded in your bot class
        else:
            options[option] = True

    gen = genFactory.getCombinedGenerator()
    if gen:
        # The preloading generator is responsible for downloading multiple
        # pages from the wiki simultaneously.
        gen = pagegenerators.PreloadingGenerator(gen)
        # pass generator and private options to the bot
        bot = BasicBot(gen, **options)
        bot.run()  # guess what it does
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False

if __name__ == '__main__':
    main()