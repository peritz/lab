from stix2 import Bundle, Malware

malware1 = Malware(name="Poison Ivy 1", is_family=False)
malware2 = Malware(name="Poison Ivy 2", is_family=False)
bundle = Bundle(malware1)
print(bundle.__dir__())
bundle.objects.append(malware2)
print(bundle.serialize(pretty=True))
