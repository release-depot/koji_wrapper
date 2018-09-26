
from os import path

from koji import AuthError
from koji import ClientSession
from koji import ConfigurationError
from koji import read_config
from koji import grab_session_options
from koji_wrapper.exceptions import UnknownAuthMethod


class KojiSessionFactory(object):
    """Factory for creating koji.ClientSession object

    This wraps the nitty gritty nuances of how to find/load
    configure/setup/authenticate a session with a koji instance
    """

    debug = False

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
            result = read_config(profile, user_config=user_config)
            for k, v in result.items():
                result[k] = path.expanduser(v) if type(v) is str else v
        except ConfigurationError as err:
            raise err

        return result

    @classmethod
    def open_session(cls, profile):
        """open a koji ClientSession using profile config

        :param profile: koji profile to load

        Open session and attempt to authenicate,  catching
        several of the common Error modes and returning
        unauthenicated session if it didn't work
        """

        user_options = cls.load_profile(profile)

        session = cls.open_session_custom(user_options=user_options)

        if not session.logged_in:
            try:
                cls.authenticate_session(session, user_options)

            except UnknownAuthMethod as err:
                print("UnknownAuthMethod: {0}".format(err))
            except AuthError as err:
                print("AuthError: {0}".format(err))

        return session

    @classmethod
    def authenticate_session(cls, session, user_options):
        """Use provide user_options to authenticate the provided session"""

        if user_options['authtype'] is None:
            session.ssl_login(user_options['cert'], None,
                              user_options['serverca'])
        elif user_options['authtype'] == 'kerberos':
            session.krb_login(principal=user_options['principal'],
                              keytab=user_options['keytab'])
        else:
            raise UnknownAuthMethod()

        return session

    @classmethod
    def open_session_custom(cls, user_options):
        """open a koji ClientSession using user_options provided

        :param user_options: koji profile+user options dictionary to use
               for opening a session
        """
        if user_options is None:
            raise TypeError("user_options not specified")

        server = user_options['server']
        options = grab_session_options(user_options)

        if cls.debug:
            print({'user_options': user_options, 'session_options': options})

        session = ClientSession(server, options)

        return session
