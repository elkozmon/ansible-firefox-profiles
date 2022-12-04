# python 3 headers. Required if submitting to Ansible.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# XXX - Maybe add an option to return either relative or absolute
# directory.

DOCUMENTATION = """
  name: firefox_profile_directory
  author: Andrew Arensburger (arensb@ooblick.com)
  version_added: "2.9.6"
  short_description: Look up a Firefox profile's directory.
  description:
      - Each Firefox profile is stored in a separate directory. This module takes a profile name and returns the directory that the profile is stored in.
  options:
    _terms:
      Name(s) of profile(s) to look up.
"""

EXAMPLES = """
- debug: msg="{{ lookup('firefox_profile_directory', 'Foo') }"
"""

RETURN = """
  _raw:
    description:
      - Directory where the given profile is stored. This is relative to the profile.ini file.
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import os
# configparser: read .ini files.
# from configparser import ConfigParser, NoOptionError
import configparser

display = Display()

class LookupModule(LookupBase):
    """
    Firefox profile directory lookup.
    """

    # Get the default path to profiles.ini
    # XXX - This is the same code as in firefox_default_profile.
    # Combine them.

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
            :arg terms: profile(s) to look up
            :returns: a list of strings, the directories where the profiles
                named in 'terms' are stored.
        """
        # Read the profiles.ini file
        profiles = configparser.ConfigParser()
        try:
            with open(LookupModule.default_profiles_path) as inifile:
                profiles.read_file(inifile)
                display.vvvv(f"read file [{profiles}]")
        except AnsibleError as e:
            display.v(f"Error reading {LookupModule.default_profiles_path}: {e}")
            raise

        # Unfortunately, 'profiles.ini' isn't organized in a friendly
        # way: it's a series of sections of the form
        #     [Profile1]
        #     Name=Surfing
        #     IsRelative=1
        #     Path=apaphDab.Surfing
        #     Default=1
        #
        #     [Profile0]
        #     Name=Projects
        #     IsRelative=1
        #     Path=Kijnekfa.Projects
        #
        # So we need to walk each "ProfileN" section, see if it has
        # the right "Name" option, and if so, add the "Path" option to
        # retval.

        retval = []
        for profile_name in terms:
            display.v(f"Ought to look up profile {profile_name}")

            for section in profiles.sections():
                # Ignore non-"ProfileNNN" sections like "InstallNNN"
                # and "General".
                if not section.startswith("Profile"):
                    continue
                if profiles.get(section, "Name") == profile_name:
                    # Found a match. Look up its "Path" and append it
                    # to retval.
                    try:
                        retval.append(profiles.get(section, "Path"))
                    except configparser.NoOptionError as e:
                        display.warning(f"No Path option in profile {section}")

        return retval
