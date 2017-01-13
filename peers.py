from charms.reactive import hook
from charms.reactive import RelationBase
from charmhelpers.core.hookenv import log
from charmhelpers.core.hookenv import in_relation_hook
from charms.reactive import scopes


class PeerDiscovery(RelationBase):
    scope = scopes.UNIT

    @hook('{peers:peer-discovery}-relation-{joined,changed}')
    def joined_or_changed(self):
        self.set_state('{relation_name}.connected')
        self.set_state('{relation_name}.joined')

    @hook('{peers:peer-discovery}-relation-departed')
    def departed(self):
        self.set_state('{relation_name}.departed')
        if not self.units():
            self.remove_state('{relation_name}.connected')

    def units(self):
        hosts = []
        for conv in self.conversations():
            hosts.append(conv.get_remote('private-address'))
        return hosts
