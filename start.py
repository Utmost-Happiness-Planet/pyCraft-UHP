#!/usr/bin/env python

import getpass
import pickle
import re
import sys
from optparse import OptionParser

from minecraft import authentication
from minecraft.backend import register_backend
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound


def get_options():
    parser = OptionParser()

    parser.add_option("-u", "--username", dest="username", default=None,
                      help="username to log in with")

    parser.add_option("-m", "--microsoft", dest="microToken", default=None,
                      help="The Token of Microsoft. You can get it from \n https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_typ"
                           "e=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf")

    parser.add_option("-p", "--password", dest="password", default=None,
                      help="password to log in with")

    parser.add_option("-t", "--token", dest="token", default=None,
                      help="Minecraft Token")

    parser.add_option("--UUID", dest="uuid", default=None,
                      help="Minecraft UUID")

    parser.add_option("-f", "--file", dest="file", action="store_true",
                      help="Use information file(LOGIN_INFO that save by --save argument) to login")

    parser.add_option("-s", "--server", dest="server", default=None,
                      help="server host or host:port "
                           "(enclose IPv6 addresses in square brackets)")

    parser.add_option("-o", "--offline", dest="offline", action="store_true",
                      help="connect to a server in offline mode "
                           "(no password required)")

    parser.add_option("--save", dest="save", action="store_true",
                      help="Save login information in a file.")

    parser.add_option("-d", "--dump-packets", dest="dump_packets",
                      action="store_true",
                      help="print sent and received packets to standard error")

    parser.add_option("-v", "--dump-unknown-packets", dest="dump_unknown",
                      action="store_true",
                      help="include unknown packets in --dump-packets output")

    (options, args) = parser.parse_args()

    if options.file:
        options.username = "_"
        options.password = "_"

    if options.microToken:
        options.username = "_"
        options.password = "_"
        if options.microToken == '*':
            print("https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_typ"
                  "e=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf")
            options.microToken = input("Microsoft Token: ")

    if options.token and options.uuid:
        options.password = "_"

    if not options.username:
        options.username = input("Enter your username: ")

    if not options.password and not options.offline:
        options.password = getpass.getpass("Enter your password (leave "
                                           "blank for offline mode): ")
        options.offline = options.offline or (options.password == "")

    if not options.server:
        options.server = input("Enter server host or host:port "
                               "(enclose IPv6 addresses in square brackets): ")
    # Try to split out port and address
    match = re.match(r"((?P<host>[^\[\]:]+)|\[(?P<addr>[^\[\]]+)\])"
                     r"(:(?P<port>\d+))?$", options.server)
    if match is None:
        raise ValueError("Invalid server address: '%s'." % options.server)
    options.address = match.group("host") or match.group("addr")
    options.port = int(match.group("port") or 25565)

    return options


def main():
    options = get_options()

    if options.offline:
        print("Connecting in offline mode...")
        connection = Connection(
            options.address, options.port, username=options.username)
    else:
        auth_token = authentication.AuthenticationToken()
        if options.file:
            with open("LOGIN_INFO", "rb") as f:
                auth_token = pickle.load(f)
        elif options.token and options.uuid:
            auth_token.DirectToken(
                options.username, options.token, options.uuid)
            print("Logged in as %s..." % auth_token.username)
            print("Minecraft Token is:\n%s" % auth_token.access_token)
            print("UUID is:\n%s" % auth_token.profile.id_)
        elif options.microToken:
            try:
                auth_token.microsoftAuthenticate(options.microToken)
            except YggdrasilError as e:
                print(e)
                sys.exit()
            print("Logged in as %s..." % auth_token.username)
            print("Minecraft Token is:\n%s" % auth_token.access_token)
            print("UUID is:\n%s" % auth_token.profile.id_)
        else:
            try:
                auth_token.authenticate(options.username, options.password)
            except YggdrasilError as e:
                print(e)
                sys.exit()
            print("Logged in as %s..." % auth_token.username)

        if options.save:
            with open("LOGIN_INFO", "wb") as f:
                pickle.dump(auth_token, f)

        connection = Connection(
            options.address, options.port, auth_token=auth_token)

    if options.dump_packets:
        def print_incoming(packet):
            if type(packet) is Packet:
                # This is a direct instance of the base Packet type, meaning
                # that it is a packet of unknown type, so we do not print it
                # unless explicitly requested by the user.
                if options.dump_unknown:
                    print('--> [unknown packet] %s' % packet, file=sys.stderr)
            else:
                print('--> %s' % packet, file=sys.stderr)

        def print_outgoing(packet):
            print('<-- %s' % packet, file=sys.stderr)

        connection.register_packet_listener(
            print_incoming, Packet, early=True)
        connection.register_packet_listener(
            print_outgoing, Packet, outgoing=True)

    def handle_join_game(join_game_packet):
        print('Connected.')

    connection.register_packet_listener(
        handle_join_game, clientbound.play.JoinGamePacket)

    def print_chat(chat_packet):
        print("Message (%s): %s" % (
            chat_packet.field_string('position'), chat_packet.json_data))

    connection.register_packet_listener(
        print_chat, clientbound.play.ChatMessagePacket)

    connection.connect()

    return connection


if __name__ == "__main__":
    connection = main()
    player = register_backend(connection)
