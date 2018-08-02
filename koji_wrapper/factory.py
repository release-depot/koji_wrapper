
from os import path

import koji
from koji_wrapper.exceptions import UnknownAuthMethod


class KojiSessionFactory(object):
    """Factory for creating koji.ClientSession object

    This wraps the nitty gritty nuances of how to find/load
    configure/setup/authenticate a session with a koji instance
    """

    @classmethod
    def load_profile(cls, profile='koji', user_config=None):
        """Load a koji profile and normalize paths

        :param profile: Which koji profile to load
        :param user_config: options to pass in and combine

        This would be used in the case where you have custom
        user_config or want to process the profile dictionary
        inspection/debugging
        """
        try:
            result = koji.read_config(profile, user_config=user_config)
            for k, v in result.items():
                result[k] = path.expanduser(v) if type(v) is str else v
        except koji.ConfigurationError as err:
            raise err

        return result

    @classmethod
    def open_session(cls, profile=None, user_options=None,
                     authenticate=False, debug=False):
        """open a koji ClientSession using profile or user_options provided

        :param profile koji: profile to load (need either profile or user_options)
        :param user_options: koji profile+user options dictionary to use
               for opening a session (need either profile or user_options)
        :param authenticate: boolean for if you want the session to be logged
               in or not (No session returned if not authenticated)
        :param debug: print out debugging details

        This is one factory option for creating a session which can be
        provided to a KojiWrapper object
        """
        if user_options is None:
            user_options = cls.load_profile(profile)

        server = user_options['server']
        options = koji.grab_session_options(user_options)

        session = koji.ClientSession(server, options)

        if debug:
            print({'user_options': user_options, 'session_options': options})

        # TODO(jmls) Might be better to split this out slightly and either
        #    stack or have a helper function that can handle login via
        #    different means.
        if authenticate:
            if user_options['authtype'] is None:
                session.ssl_login(user_options['cert'], None,
                                  user_options['serverca'])
            elif user_options['authtype'] == 'kerberos':
                session.krb_login(principal=user_options['principal'],
                                  keytab=user_options['keytab'])
            else:
                raise UnknownAuthMethod()
            if not session.logged_in:
                session.login()

        return session
