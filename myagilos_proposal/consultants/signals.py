from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from .models import Certification_targets, Certification_progress, Consultants, Consultant_certifications, ForgotPassword
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


@receiver(post_save, sender=User)
def update_consultant_fields(instance, created, **kwargs):
    """
    Update consultant fields upon saving a User object.

    Args:
        instance (User): The User object that was saved.
        created (bool): A boolean indicating whether the User object was created or updated.
        **kwargs: Additional keyword arguments passed to the function.

    Returns:
        None
    """
    if not created:
        consultant, created = Consultants.objects.get_or_create(user=instance)

        for field in ['first_name', 'last_name', 'email']:
            setattr(consultant, field, getattr(instance, field, None))

        Consultants.objects.filter(pk=consultant.id).update(
            **{field: getattr(instance, field) for field in ['first_name', 'last_name', 'email']})
    else:
        # Create first name, last name, email from the user's username
        first_name, last_name = instance.username.split(".")
        email = f"{first_name[0]}{last_name[0]}{last_name[1]}@agilos.com"
        fields = {
            "first_name": first_name.capitalize(),
            "last_name": last_name.capitalize(),
            "email": email.lower()
        }
        # Create a consultant and link it to the user
        # + add the first name last name and email values to the consultant
        # + add the current target.
        Consultants.objects.create(
            user=instance, **fields, target=Certification_targets.objects.get(active=True)
        )
        # Update the user's username, first name, last name and email
        # Update() method because user already exists into instance variable
        # and we must avoid recursive triggers by using the save() method
        User.objects.filter(pk=instance.id).update(
            username=instance.username.lower(), **fields)
        # Add certification's consultant progress state into certification_progress model
        Certification_progress.objects.create(
            consultant=Consultants.objects.get(user=instance),
            target=Certification_targets.objects.get(active=True),
            achieved=False
        )


@receiver(post_save, sender=Consultants)
def update_user_fields(instance, created, **kwargs):
    """
    Update user fields upon saving a Consultants object.

    Args:
        instance (Consultants): The Consultants object that was saved.
        created (bool): A boolean indicating whether the Consultants object was created or updated.
        **kwargs: Additional keyword arguments passed to the function.

    Returns:
        None
    """
    if not created:
        try:
            user = instance.user
        except User.DoesNotExist:
            raise User.DoesNotExist("The user does not exist")

        for field in ['first_name', 'last_name', 'email']:
            setattr(user, field, getattr(instance, field, None))

        user.save(update_fields=['first_name', 'last_name', 'email'])


@receiver(post_delete, sender=Consultants)
def delete_consultant(instance, **kwargs):
    """
    Delete the corresponding User object when a Consultants object is deleted.

    Args:
        instance (Consultants): The Consultants object that was deleted.
        **kwargs: Additional keyword arguments passed to the function.

    Returns:
        None
    """
    try:
        user_to_del = instance.user
    except User.DoesNotExist:
        pass
    else:
        user_to_del.delete()


@receiver(pre_save, sender=Consultant_certifications)
def check_progress(instance, **kwargs):
    if instance.id is not None:
        previous = Consultant_certifications.objects.get(pk=instance.id)
        if previous.certification == Certification_targets.objects.get(active=True).certification:
            Certification_progress.objects.filter(
                consultant=previous.consultant,
                target=Certification_targets.objects.get(active=True)
            ).update(
                achieved=False
            )


@receiver(post_save, sender=Consultant_certifications)
def update_progress(instance, **kwargs):

    if instance.certification == Certification_targets.objects.get(active=True).certification:
        Certification_progress.objects.filter(
            consultant=instance.consultant,
            target=Certification_targets.objects.get(active=True)
        ).update(
            achieved=True
        )


@receiver(post_save, sender=Certification_targets)
def update_consultants_target_and_progress(instance, **kwargs):
    """
    Update the target field of all Consultant objects when a Certification_targets object is saved.

    Args:
        instance (Certification_targets): The Certification_targets object that was saved.
        **kwargs: Additional keyword arguments passed to the function.

    Raises:
        ValidationError: If there is no active Certification_targets object.

    Returns:
        None
    """
    if instance.active:
        def bulk_progress(consultants_list, achieved):
            """
            Bulk creates `Certification_progress` objects for the given list of consultants.

            Args:
                consultants_list (list): A list of `Consultants` objects for which the `Certification_progress` objects will be created.
                achieved (bool): The value to be assigned to the `achieved` field of the `Certification_progress` objects.

            Returns:
                None

            Raises:
                Certification_targets.DoesNotExist: If no active `Certification_targets` object is found.

            Notes:
                This function uses the `bulk_create` method of the `Certification_progress` model to efficiently create multiple objects at once.

            Example usage:
                consultants = Consultants.objects.all()
                consultants_without_target_certifs = [consultant for consultant in consultants if not consultant.certifications.filter(target__active=True).exists()]
                bulk_progress(consultants_without_target_certifs, achieved=False)
            """
            active_target = Certification_targets.objects.get(active=True)
            bulk = []
            for consultant in consultants_list:
                bulk.append(
                    Certification_progress(
                        consultant=consultant,
                        target=active_target,
                        achieved=achieved
                    )
                )
            Certification_progress.objects.bulk_create(bulk)

        # Set every other targets to False
        Certification_targets.objects.exclude(
            pk=instance.id).update(active=False)

        # Create progress for those who already have a certification that is the new target
        bulk_progress([consultant for consultant in Consultants.objects.all(
        ) if consultant.certifications.filter(target__active=True).exists()], True)
        bulk_progress([consultant for consultant in Consultants.objects.all(
        ) if not consultant.certifications.filter(target__active=True).exists()], False)

        # Set all consultants target to current target
        Consultants.objects.all().update(target=instance)
    # If there is no active target, raise an error
    elif not Certification_targets.objects.filter(active=True).exists():
        # Certification_targets.objects.filter(pk=instance.id).update(active=True)
        raise ValidationError("You must have at least one active target.")


@receiver(post_save, sender=ForgotPassword)
def update_case_state(instance, **kwargs):
    if instance.active:
        ForgotPassword.objects.filter(username=instance.username).exclude(pk=instance.pk).update(active=False)
