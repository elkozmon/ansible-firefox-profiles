# python 3 headers. Required if submitting to Ansible.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# XXX - Not sure why this requires the "plugin_type" entry. Other
# lookup plugins don't have it.
DOCUMENTATION = """
  name: firefox_default_profile
  author: Andrew Arensburger (arensb@ooblick.com)
  version_added: "2.9.6"
  short_description: Get the default Firefox profile
  description:
      - This lookup reads the 'profile.ini' file and looks up the default profile name.
  plugin_type: lookup
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import os
# configparser: read .ini files.
from configparser import ConfigParser

display = Display()

class LookupModule(LookupBase):
    """Given a Firefox profiles.ini file, look up the default profile."""

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
        """
            :arg terms: not used.
            :kwargs variables: ansible variables active at the time of lookup.
            :returns: a string, the name of the default profile. This is
                the "Name=" option in the section of the default profile.
        """
        # Read the profiles.ini file
        profiles = ConfigParser()
        try:
            with open(LookupModule.default_profiles_path) as inifile:
                profiles.read_file(inifile)
                display.vvvv(f"read file [{profiles}]")
        except AnsibleError as e:
            display.v(f"Error reading {LookupModule.default_profiles_path}: {e}")
            raise

        for section in profiles.sections():
            display.vvvv(f"Found section {section}")
            # Find section beginning with "Install". This contains a
            # "Default=<directory>" option for the default profile for
            # this installation.
            # XXX - There can be multiple installations. How do we
            # want to deal with this?
            if section.startswith("Install"):
                display.vvvv(f"Found the install section")
                install_section = section
                break

        # Get its "Default": that's the directory of the default
        # profile.
        default_profile_dir = profiles[install_section]['Default']
        display.vvv(f"default Firefox profile directory: {default_profile_dir}")

        # Look through the "ProfileN" sections
        for section in profiles.sections():
            display.vvvv(f"Examining section {section}")
            # Find one with "Path=" the directory that we found above.
            if not section.startswith("Profile"):
                continue
            sect = profiles[section]
            if "Path" in sect and \
               sect['Path'] == default_profile_dir:
                # Found it
                display.vvvv(f"Found it: section {section}, Name={sect['name']}")

                # Return its "Name=".
                return [ sect['Name'] ]

        # If we get this far, we didn't find anything.
        return []
