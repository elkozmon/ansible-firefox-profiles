# python 3 headers. Required if submitting to Ansible.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import os
# configparser: read .ini files.
import configparser

# XXX - Maybe add an option to return either relative or absolute
# directory.

# XXX - Add an "on_missing" option, similar to
# /usr/lib/python3/dist-packages/ansible/plugins/lookup/config.py
# 'error' => Raise a fatal error
# 'skip' => Ignore the term
# 'warn' => Ignore the term, but issue a warning.

DOCUMENTATION = """
  name: firefox_profile
  author: Andrew Arensburger (arensb@ooblick.com)
  version_added: "2.9.6"
  short_description: Look up information about a Firefox profile.
  description:
      - Fetch information about a Firefox profile from the profiles.ini file.
  options:
    _terms:
      Name(s) of profile(s) to look up.
    on_missing:
      description:
        - Action to take if a profile doesn't exist.
      default: error
      type: string
      choice: ['error', 'skip', 'warn']
"""

EXAMPLES = """
- name: Look up a profile's path
  debug:
    msg: "{{ lookup('firefox_profile', 'My Profile')['path'] }}"

- name: Look up a profile's path with a variable
  vars:
    profile_info: "{{ lookup('firefox_profile', 'NCBI3') }}"
  debug:
    msg: "{{ profile_info['path'] }}"

- name: Check whether a profile exists
  vars:
    profile_dir: "{{ lookup('firefox_profile', 'My Profile', errors='warn') }}"
  block:
    - debug:
        msg: "Profile directory is {{ profile_dir }}"
      when:
        - profile_dir != ""
    - debug:
        msg: "No such profile: {{ profile_dir }}"
      when:
        - profile_dir == ""
"""

RETURN = """
  _raw:
    description:
      - Dictionary containing all of the profile information from profiles.ini
"""

display = Display()


class LookupModule(LookupBase):
    """
    Firefox profile lookup.
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
                display.vvv(f"Looking at section {section}")
                # Ignore non-"ProfileNNN" sections like "InstallNNN"
                # and "General".
                if not section.startswith("Profile"):
                    continue
                display.vvv(f"Name: {profiles.get(section, 'Name')} ==? {profile_name}")
                if profiles.get(section, "Name") == profile_name:
                    # Found it. Look up its options, and append to
                    # retval.
                    display.vvv("Found it.")
                    # profile_opts = profiles.options(section)
                    profile_opts = {option: profiles.get(section, option)
                                    for option in profiles.options(section)}
                    retval.append(profile_opts)
                    break

            else:
                # XXX - If we get this far, we didn't find the profile.
                # raise AnsibleError(f"No such profile: {profile_name}")
                retval.append(None)

        display.v(f"Returning {retval}")
        return retval
