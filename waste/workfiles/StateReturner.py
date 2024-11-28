

class StateReturner:

    @staticmethod
    def relations_objects_state_return(relations):
        from waste.models import Organization, WasteStorage

        organizations = Organization.objects.filter(relations=relations)
        storages = WasteStorage.objects.filter(relations=relations)

        for organization in organizations:
            organization.plastic = organization.generate_plastic
            organization.glass = organization.generate_glass
            organization.bio_wastes = organization.generate_bio_wastes
            organization.save()

        for storage in storages:
            storage.plastic = 0
            storage.glass = 0
            storage.bio_wastes = 0
            storage.save()

    @staticmethod
    def relations_all_paths_clear(relations):
        relations.ways_structure = {}
        relations.save()
