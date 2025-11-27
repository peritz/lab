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

    def __init__(self, creator_name: str, bundle: Bundle):
        self._context = self._CONTEXT_CLASS(creator_name)
        self._bundle = bundle

    def __enter__(self):
        return self._context

    def __exit__(self, *exc_details):
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
    bundle = Bundle([IPv4Address(value="1.1.1.1")])
    with MalwareContextManager("Me, Myself, and I", bundle, "Spicy Potato") as ctx:
        # Cloudflare ftw
        ctx.add_ipv4_address("8.8.8.8")
    print(bundle.serialize(pretty=True))
