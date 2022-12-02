# python 3 headers. Required if submitting to Ansible.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
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

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        # First of all, populate options.
        # This will already take into account environment variables
        # and ini config.
        ret = []
        for term in terms:
            display.debug(f"Default profile: term: {term}")

            # Find the file in the expected search path, using a class
            # method that implements the 'expected' search path for
            # Ansible plugins.
            lookupfile = self.find_file_in_search_path(variables, 'files', term)

            # Don't use print or your own logging. The Display class
            # takes care of that in a unfied way.
            display.vvvv(f"File lookup using {lookupfile} as a file")

            try:
                if lookupfile:
                    contents, show_data = self._loader._get_file_contents(lookupfile)
                    ret.append(contents.rstrip())
                else:
                    # Always use Ansible error classes to throw
                    # 'final' exceptions, so the Ansible engine will
                    # know how to deal with them.

                    # The Parser error indicates that invalid options
                    # were passed.
                    raise AnsibleParserError()
            except AnsibleParserError:
                raise AnsibleError(f"Could not locate file in lookup: {term}")

            # Consume an option: if this did something useful, you can
            # retrieve the option value here.
            if self.get_option('option1') == 'do_something':
                display.v(f"I was given option1 to do something.")

        return ret
