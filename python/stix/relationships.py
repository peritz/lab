from stix2 import Relationship, Malware, IntrusionSet

intrusion_set = IntrusionSet(name="APT900")
malware = Malware(name="Poison Ivy", is_family=True)
relationship = Relationship(
    relationship_type="related-to", source_ref=malware.id, target_ref=intrusion_set.id
)

print(relationship.serialize(pretty=True))
