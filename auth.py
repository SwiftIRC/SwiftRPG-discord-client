#!/usr/bin/env python3

class Auth:
    auth = {"Dragon": {"character": "Dragon"},
            "Dragon#1088": {"character": "Dragon"},
            "foo": {"character": "foo"},
            }

    def __init__(self):
        pass

    def login(self, nick, username, password):
        if '{}'.format(nick) in self.auth and self.auth[nick]['character'] == username:
            return True
        return False
        # log into website with credentials

    def check(self, nick):
        return (True if '{}'.format(nick) in self.auth else False)

    def logout(self, nick):
        del self.auth[nick]

    def rename(self, nick, newnick):
        self.auth[newnick] = self.auth[nick]
        del self.auth[nick]