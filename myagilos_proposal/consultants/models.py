import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
import json
from os import path


def semester_num():
    """
    Returns the semester number based on the current month.

    Returns:
        int: 1 if the current month is in the first half of the year, 2 otherwise.
    """
    today = datetime.date.today()
    return 1 if today.month < 7 else 2


class Consultants(models.Model):
    """
    Model representing consultants.
    """
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name="as_consultant")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=64, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    certifications = models.ManyToManyField(
        "Certifications", through="consultant_certifications", related_name="related_consultants")
    target = models.ForeignKey(
        "Certification_targets", null=True, blank=True, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Consultants"

    def __str__(self):
        """
        Returns the string representation of the consultant.

        Returns:
            str: The consultant's full name or username if personal info is missing.
        """
        if self.first_name or self.last_name:
            return f"{self.last_name} {self.first_name}"
        return f"{self.user.username} - missing personal info (please, fill in)"


class Certifications(models.Model):
    """
    Model representing certifications.
    """
    ALL_CERTIFICATIONS = path.join(path.dirname(
        __file__), f"static/certifications/{timezone.now().year}_allCertifications_.json")
    with open(ALL_CERTIFICATIONS, "r") as rf:
        file = rf.read()
        COMPANIES = [("---", "---")] + [
            (company["company"], company["company"])
            for company in json.loads(file)
        ]
        CERTIFICATIONS = [("---", "---")] + [
            (certification["name"], certification["name"])
            for company in json.loads(file)
            for certification in company["certifications"]
        ]

        CODES = [("---", "---")] + [
            (certification["code"], certification["code"])
            for company in json.loads(file)
            for certification in company["certifications"]
        ]

        CERTIFICATIONS_CODES = [
            (f"{certification['code']} - {certification['name']}",
             f"{certification['code']} - {certification['name']}")
            for company in json.loads(file)
            for certification in company["certifications"]
        ]

    company = models.CharField(max_length=64, choices=COMPANIES)
    title = models.CharField(
        max_length=254, choices=CERTIFICATIONS, unique=True)
    code = models.CharField(
        max_length=64, choices=CODES, unique=True, blank=True, null=True)
    consultants = models.ManyToManyField(
        "Consultants", through="Consultant_certifications", related_name="related_certifications")
    class Meta:
        verbose_name_plural = "Certifications"
        unique_together = (
            ("company", "title"),
        )

    def __str__(self):
        """
        Returns the string representation of the certification.

        Returns:
            str: The certification's company and title.
        """
        return f"{self.company} - {self.title}"


class Consultant_certifications(models.Model):
    """
    Model representing the relationship between consultants and certifications.
    """
    consultant = models.ForeignKey("Consultants", on_delete=models.CASCADE)
    certification = models.ForeignKey(
        "Certifications", on_delete=models.CASCADE)
    earned_at = models.DateField()
    expires_at = models.DateField(blank=True, null=True)
    certification_idcode = models.CharField(
        max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Consultant_certifications"
        # unique_together = (("consultant", "certification"),)

    def __str__(self):
        """
        Returns the string representation of the consultant certification relationship.

        Returns:
            str: The consultant's full name, certification title and date earned.
        """
        return f"{self.consultant.first_name} {self.consultant.last_name} - {self.certification.title} - Earned: {self.earned_at.strftime('%Y-%m-%d')}"


class Certification_progress(models.Model):
    """
    Model representing the progress of a consultant towards a certification target.
    """
    consultant = models.ForeignKey(
        "Consultants", on_delete=models.CASCADE, related_name="progress")
    target = models.ForeignKey(
        "Certification_targets", on_delete=models.CASCADE, related_name="progress")
    achieved = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Certification_progress"
        unique_together = (("consultant", "target"),)

    def __str__(self):
        """
        Returns a string representation of the Certification_progress instance.
        """
        if self.achieved:
            return f"{self.consultant.first_name} {self.consultant.last_name} - {self.target.certification.title} - Achieved"
        return f"{self.consultant.first_name} {self.consultant.last_name} - {self.target.certification.title} - Not achieved"

class Certification_targets(models.Model):
    """
    Model representing a certification target for a certain certification and year.
    """
    certification = models.ForeignKey(
        "Certifications", on_delete=models.CASCADE, related_name="target", unique_for_year="created_at")
    target_year = models.PositiveSmallIntegerField(default=timezone.now().year)
    semester = models.PositiveSmallIntegerField(default=semester_num)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Certification_targets"

    def __str__(self):
        """
        Returns a string representation of the Certification_targets instance.
        """
        if self.semester == 1:
            self.verbose = "st"
        else:
            self.verbose = "nd"
        if self.active:
            return f"{self.target_year} - {str(self.semester) + self.verbose} semester: {self.certification.title} - Active"
        return f"{self.target_year} - {str(self.semester) + self.verbose} semester: {self.certification.title} - Inactive"


class Cases(models.Model):
    """
    Model representing a case study for a project completed by a consultant.
    """
    INDUSTRIES = [
        ("---", "---"),
        ("Aerospace and Defense", "Aerospace and Defense"),
        ("Agriculture", "Agriculture"),
        ("Automotive", "Automotive"),
        ("Bank", "Bank"),
        ("Construction", "Construction"),
        ("Education", "Education"),
        ("Energy", "Energy"),
        ("Environmental Conservation and Sustainability",
         "Environmental Conservation and Sustainability"),
        ("Finance", "Finance"),
        ("Government and Public Administration",
         "Government and Public Administration"),
        ("Health", "Health"),
        ("Hospitality", "Hospitality"),
        ("Insurance", "Insurance"),
        ("Law and Legal Services", "Law and Legal Services"),
        ("Manufacturing", "Manufacturing"),
        ("Media and Entertainment", "Media and Entertainment"),
        ("Nonprofit and Social Services", "Nonprofit and Social Services"),
        ("Pharmaceuticals", "Pharmaceuticals"),
        ("Real Estate", "Real Estate"),
        ("Retail", "Retail"),
        ("Sports and Fitness", "Sports and Fitness"),
        ("Telecommunications", "Telecommunications"),
        ("Technology", "Technology"),
        ("Transportation", "Transportation")
    ]
    industry = models.CharField(max_length=64, choices=INDUSTRIES)
    company = models.CharField(max_length=64)
    author = models.ForeignKey(
        "consultants", on_delete=models.CASCADE, related_name="case")
    created_at = models.DateTimeField(auto_now_add=True)
    year = models.PositiveSmallIntegerField(default=timezone.now().year)
    project_start = models.DateField()
    project_end = models.DateField()
    gpt_content = models.TextField(max_length=10000)
    issue = models.TextField(max_length=400)
    architecture = models.TextField(max_length=400)
    challenge = models.TextField(max_length=400)
    solution = models.TextField(max_length=400)
    tools = models.TextField(max_length=400)
    why_agilos = models.TextField(max_length=400)

    class Meta:
        verbose_name_plural = "Cases"

    def __str__(self):
        """
        Returns a string representation of the Cases instance.
        """
        return f"{self.company} - {self.year}'s case, by {self.author.first_name} {self.author.last_name}"


class ForgotPassword(models.Model):
    username = models.CharField(max_length=60)
    email = models.EmailField(max_length=60)
    salt_and_hash = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=(
        timezone.now() + datetime.timedelta(minutes=60)), null=True, blank=True)
    active = models.BooleanField(default=True)
