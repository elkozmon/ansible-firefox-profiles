# python 3 headers. Required if submitting to Ansible.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION2 = """
  name: default_profile
  author: Andrew Arensburger (arensb@ooblick.com)
  version_added: "2.9.6"
  short_description: Get the default Firefox profile
  description:
      - This lookup reads the 'profile.ini' file and looks up the default profile name.
  options:
    profile_file:
      description: Pathname of profile.ini file to read.
      type: string
      required: False
    option1:
      description: Dummy option
      type: string
      required: False
  notes:
    - 'profile.ini' contains one section with a name of the form "[InstallXXXXXX]". This is the default.
    - This module assumes that there is only one such section
"""

DOCUMENTATION = """
  name: default_profile
  options:
    option1:
      description: Dummy option
      type: string
      required: False
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import os
from configparser import ConfigParser

display = Display()

class LookupModule(LookupBase):


    # Get the default path to profiles.ini

    # XXX - This ought to come from a variable, if the caller has
    # set it. But that might use variables, so it needs to be
    # expanded.

    # XXX - Different default under MacOS. Probably a different
    # one in Windows as well.

    # XXX - Handle the case where $HOME isn't set.
    default_profiles_path = os.environ.get('HOME') + \
        "/.mozilla/firefox/profiles.ini"

    def run(self, terms, variables=None, **kwargs):

        display.vvv(f"inside run(terms=[{terms}]")
        display.vvv(f"default_profiles_path: {LookupModule.default_profiles_path}")
        # for var in variables:
        #     display.vvv(f"variable {var}: {variables[var]}")
        # self.set_options(var_options = variables, direct=kwargs)
        # for opt in self._options:
        #     display.vvv(f"option {opt}: {self._options[opt]}")

        # First of all, populate options.
        # This will already take into account environment variables
        # and ini config.
        ret = []
        for term in terms:
            display.debug(f"Default profile: term: {term}")

            # Find the file in the expected search path, using a class
            # method that implements the 'expected' search path for
            # Ansible plugins.
            # lookupfile = self.find_file_in_search_path(variables, 'files', term)

            # Don't use print or your own logging. The Display class
            # takes care of that in a unfied way.
            # display.vvvv(f"File lookup using {lookupfile} as a file")

            # try:
            #     if lookupfile:
            #         contents, show_data = self._loader._get_file_contents(lookupfile)
            #         ret.append(contents.rstrip())
            #     else:
            #         # Always use Ansible error classes to throw
            #         # 'final' exceptions, so the Ansible engine will
            #         # know how to deal with them.

            #         # The Parser error indicates that invalid options
            #         # were passed.
            #         raise AnsibleParserError()
            # except AnsibleParserError:
            #     raise AnsibleError(f"Could not locate file in lookup: {term}")

            # Consume an option: if this did something useful, you can
            # retrieve the option value here.
            if self.get_option('option1') == 'do_something':
                display.v(f"I was given option1 to do something.")

        # Read the profiles.ini file
        profiles = ConfigParser()
        try:
            with open(LookupModule.default_profiles_path) as inifile:
                profiles.read_file(inifile)
                display.vvv(f"read file [{profiles}]")
        except Exception as e:
            display.v(f"Error reading {LookupModule.default_profiles_path}: {e}")
            raise

        for section in profiles.sections():
            display.vvv(f"Found section {section}")
            # Find section beginning with "Install". This contains a
            # "Default=<directory>" option for the default profile for
            # this installation.
            # XXX - There can be multiple installations. How do we
            # want to deal with this?
            if section.startswith("Install"):
                display.vvv(f"Found the install section")
                install_section = section
                break

        # Get its "Default": that's the directory of the default
        # profile.
        default_profile_dir = profiles[install_section]['Default']
        display.vv(f"default profile dir: {default_profile_dir}")

        # XXX - Look through the "ProfileN" sections
        # XXX - Find one with "Path=" the directory that we found above.
        for section in profiles.sections():
            display.vv(f"Examining section {section}")
            if not section.startswith("Profile"):
                continue
            sect = profiles[section]
            if "Path" in sect and \
               sect['Path'] == default_profile_dir:
                # Found it
                # XXX - Return its "Name=".
                return [ sect['Name'] ]
        return []
