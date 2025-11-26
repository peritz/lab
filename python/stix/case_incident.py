from pycti import CustomObjectCaseIncident
from stix2 import Malware

malware = Malware(name="Silly Goose", is_family=True)
case = CustomObjectCaseIncident(name="test incident", object_refs=[malware.id])
print(case.get("object_refs"))
print(case.get("name"))
