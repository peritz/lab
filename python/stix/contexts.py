from contextlib import AbstractContextManager

from stix2 import (
    Environment,
    ObjectFactory,
    MemoryStore,
    Identity,
    Filter,
    Bundle,
    Malware,
    IPv4Address,
)

class BaseStixEnvironment(Environment):
    # Consider also passing in parent environments that can be treated in a standard way and
    # combined when moving up the context stack
    def __init__(self, creator_name: str, additional_source=None):
        self._isolated_store = MemoryStore()
        super().__init__(store=self._isolated_store, source=additional_source)
        creators = self.query(
            [Filter("type", "=", "Identity"), Filter("name", "=", creator_name)]
        )
        if len(creators) == 0:
            creator = self.create(
                Identity, name=creator_name, identity_class="organization"
            )

            self.set_default_creator(creator.id)
            self.add(creator)
        else:
            self.set_default_creator(creators[0].id)
            self.add(creators[0])

    def extend_bundle(self, bundle: Bundle):
        bundle.objects.extend(self._isolated_store.query())


class BaseStixContextManager(AbstractContextManager):
    _CONTEXT_CLASS = BaseStixEnvironment

    # Consider dealing with environments rather than a bundle
    # The bundle can be resolved at the end
    def __init__(self, creator_name: str, bundle: Bundle):
        self._context = self._CONTEXT_CLASS(creator_name)
        self._bundle = bundle

    def __enter__(self):
        return self._context

    def __exit__(self, *exc_details):
        # Possibly a function called "Merge Environments" that adds the other environment's source
        # as a source in the parent environment or something to that effect? Maybe "wrap"?
        # Don't necessarily need to do this at the end, do it at the beginning in the __init__ of
        # BaseStixEnvironment
        self._context.extend_bundle(self._bundle)


class MalwareContextManager(BaseStixContextManager):
    class _MalwareContext(BaseStixEnvironment):
        def add_ipv4_address(self, value):
            self.add(IPv4Address(value=value))

    _CONTEXT_CLASS = _MalwareContext

    def __init__(self, creator_name: str, bundle: Bundle, malware_name: str):
        super().__init__(creator_name, bundle)
        malware = self._context.create(Malware, name=malware_name, is_family=False)
        self._context.add(malware)


if __name__ == "__main__":
    # Test nested environments with a validation function to add C2 servers
    bundle = Bundle([IPv4Address(value="1.1.1.1")])
    with MalwareContextManager("Me, Myself, and I", bundle, "Spicy Potato") as ctx:
        # Cloudflare ftw
        ctx.add_ipv4_address("8.8.8.8")
    print(bundle.serialize(pretty=True))
