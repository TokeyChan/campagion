def duplicate(instance, parent_instance = None):
    fkeys = []
    fields = []
    for field in instance._meta.fields:
        if parent_instance != None:
        if field.get_internal_type() == "ForeignKey":
            fkeys.append(field)
        else:
            fields.append(field)

    new_instance = instance._meta.model()
    for field in fields:
        setattr(new_instance, field.name, getattr(instance, field.name))

    new_instance.save()

    for fkey in fkeys:
