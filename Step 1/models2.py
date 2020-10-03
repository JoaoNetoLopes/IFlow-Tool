import uuid

from django.db import models
#from django.contrib.auth.models import AbstractUser


from typing import (Any, TypeVar, List, Tuple, cast, Set, Dict, Union, Optional, Callable, Sequence,)

class HCLI():
    pass

class HCHI(HCLI):
    pass

class LCLI(HCLI):
    pass

class LCHI(LCLI,HCHI):
    pass
    


class FenixUser():
    name = models.CharField(max_length=250) # type: HCLI
    email = models.EmailField(max_length=100) # type: HCLI
    status = models.CharField(max_length=100) # type: HCLI

class Election(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False) # type: HCLI
    name = models.TextField() # type: HCLI
    description = models.TextField() # type: HCLI
    startDate = models.DateTimeField() # type: HCLI
    endDate = models.DateTimeField() # type: HCLI
    openCastTime = models.TimeField(null=True) # type: HCLI
    closeCastTime = models.TimeField(null=True) # type: HCLI
    cryptoParameters = models.TextField() # type: HCLI
    admin = models.ForeignKey(FenixUser, on_delete = models.CASCADE) # type: HCLI
    publicKey = models.TextField() # type: HCLI
    hybrid = models.BooleanField() # type: HCLI
    aggregatedEncTally = models.TextField(null=True) # type: HCLI
    tally = models.TextField(null=True) # type: HCLI
    paperResults = models.TextField(null=True) # type: HCLI

class Trustee(models.Model):
    election = models.ForeignKey(Election,on_delete = models.CASCADE) # type: HCLI
    identifier = models.TextField() # type: HCLI
    name = models.TextField() # type: HCLI
    email = models.EmailField(max_length=200) # type: HCLI
    publicKeyShare = models.TextField(null=True) # type: HCLI
    partialDecryption = models.TextField(null=True) # type: HCLI
    keyShareProofRandom = models.TextField(null=True) # type: HCLI
    decryptionProofRandom = models.TextField(null=True) # type: HCLI
    class Meta:
        unique_together = (('election','identifier'),)
    
class Voter(models.Model):
    election = models.ForeignKey(Election,on_delete = models.CASCADE) # type: HCLI
    identifier = models.TextField() # type: HCLI
    email = models.EmailField(max_length=200) # type: HCLI
    publicCredential = models.TextField() # type: HCLI
    proofRandomValues = models.TextField(null=True) # type: HCLI
    paperVoter = models.BooleanField(default=False) # type: HCLI
    class Meta:
        unique_together = (('election','identifier'),)

class Question(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False) # type: HCLI
    election = models.ForeignKey(Election,on_delete = models.CASCADE) # type: HCLI
    question = models.TextField() # type: HCLI
    class Meta:
        unique_together = (('election','question'),)

class Answer(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False) # type: HCLI
    question = models.ForeignKey(Question,on_delete = models.CASCADE) # type: HCLI
    answer = models.TextField() # type: HCLI    
    class Meta:
        unique_together = (('question','answer'),)

class Ballot(models.Model):
    election = models.ForeignKey(Election,on_delete = models.CASCADE) # type: HCLI
    ballot = models.TextField() # type: HCLI
    publicCredential = models.TextField() # type: HCLI
    SBT = models.TextField()        #SBT = smart Ballot Tracker
    class Meta:
        unique_together = (('election','publicCredential'),)
