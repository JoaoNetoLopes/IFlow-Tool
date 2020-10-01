
import json
import requests
import csv
import requests
import datetime
import secrets
import ast
import hashlib
import base64
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import transaction, IntegrityError
from django.conf import settings
from django.urls import reverse
from models3 import Election
from models3 import Trustee
from models3 import Voter
from models3 import Question
from models3 import Answer
from models3 import Ballot
from ElectionServer.Crypto.ParameterGenerator import generate_parameters
from ElectionServer.Crypto import Schnorr
from typing import Iterable
from typing import NewType
from typing import Any, TypeVar, List, Tuple, cast, Set, Dict, Union, Optional, Callable, Sequence

class HCLI():
    pass

class HCHI(HCLI):
    pass

class LCLI(HCLI):
    pass

class LCHI(HCHI, LCLI):
    pass
T1 = TypeVar('T1', 'HCLI', 'HCHI', 'LCLI', 'LCHI')
T0 = TypeVar('T0', 'HCLI', 'HCHI', 'LCLI', 'LCHI')

def expressionHandler2(x0: Tuple[A, T0], x1: Tuple[A, T1]) -> Tuple[A, Union[T0, T1]]:
    return

def home(request: LCHI=LCHI()):
    return render(request, 'home.html', {'admin': (str(request.user) in settings.AUTHORIZED_ADMINS)})

def login(request: LCHI=LCHI()):
    return render(request, 'login.html')

def elections(request: LCHI=LCHI()):
    context = {'elections': Election.objects.all()}
    return render(request, 'elections.html', context)

@login_required
def manageElections(request: LCHI=LCHI()):
    context = HCLI()
    return render(request, 'manageElections.html', context)

def getElections(request: LCHI=LCHI()):
    if (request.method == 'GET'):
        data = HCLI()
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
@csrf_exempt
def createElection(request: LCHI=LCHI()):

    def postCreateElection(request: LCHI=LCHI()):
        try:
            data = cast(Dict[(str,  LCHI)], data)
            with transaction.atomic():
                election = Election()
                sup = HCLI()
                print(sup)
                leftside1 = LCHI()
                leftside1 = sup
                sup2 = LCHI()
                sup2 = sup
                sup = sup2
                election.name = data['name']
                data['name'] = election.name
                election.description = data['description']
                election.hybrid = data['paperVotes']
                election.startDate = data['startDate']
                election.endDate = data['endDate']
                if (datetime.datetime.strptime(data['startDate'], '%Y-%m-%d %H:%M') < datetime.datetime.now()):
                    return HttpResponse(json.dumps({'error': 'The election date is in the past.'}), content_type='application/json', status=406)
                if (election.endDate <= election.startDate):
                    return HttpResponse(json.dumps({'error': 'The election end date must be greater than the election start date.'}), content_type='application/json', status=406)
                if ('openCastTime' in data.keys()):
                    election.openCastTime = data['openCastTime']
                    election.closeCastTime = data['closeCastTime']
                election.admin = request.user
                parameters = generate_parameters()
                election.cryptoParameters = {'p': str(parameters['p']), 'q': str(parameters['q']), 'g': str(parameters['g'])}
                election.save()
                try:
                    r = requests.post(expressionHandler2(settings.CREDENTIAL_AUTHORITY, '/addElection/'), data=json.dumps({'election': {'id': str(election.id), 'endDate': election.endDate}}))
                except Exception as exception:
                    return HttpResponse(json.dumps({'error': 'Failed connection to credential authority'}), content_type='application/json', status=500)
                if (r.status_code != 200):
                    raise Exception((('Got error code ' + str(r.status_code)) + ' from registration server'))
            return HttpResponse(json.dumps({'success': True, 'currentUrl': reverse('createElection'), 'redirectUrl': reverse('election', args=[str(election.id)])}), content_type='application/json')
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    if (request.method == 'POST'):
        return postCreateElection(request)
    elif (request.method == 'GET'):
        return render(request, 'createElection.html')
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])

@login_required
@csrf_exempt
def addTrustees(request: LCHI(), election_id):
    if (request.method == 'POST'):
        try:
            election = HCLI()
            if (request.user != election.admin):
                return HttpResponseForbidden('Access denied')
            if (datetime.datetime.now() >= election.startDate):
                return HttpResponse(json.dumps({'error': 'The election has already started. Cannot add trustees now.'}), content_type='application/json', status=500)
            data = cast(Dict[(str,  LCLI())], data)
            with transaction.atomic():
                for trusteeData in data['trusteeList']:
                    t = Trustee()
                    t.election = election
                    t.identifier = trusteeData['id']
                    t.name = trusteeData['name']
                    t.email = trusteeData['email']
                    t.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        except IntegrityError:
            return HttpResponse(json.dumps({'error': (('Trustee ' + trusteeData['id']) + ' already present')}), content_type='application/json', status=500)
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
@csrf_exempt
def removeTrustees(request: LCHI(), election_id: LCLI()):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() >= election.startDate):
            return HttpResponse(json.dumps({'error': 'The election has already started. Cannot remove trustees now.'}), content_type='application/json', status=500)
        try:
            data = cast(Dict[(str,  LCHI())], data)
            for trusteeData in data['trusteeList']:
                Trustee.objects.get(identifier=trusteeData, election=election).delete()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except Trustee.DoesNotExist:
            pass
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def getTrustees(request: LCHI(), election_id: LCHI()):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        data = HCLI()
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def addVoters(request: LCHI(), election_id):

    def addVotersFile(request: LCHI(), election):
        try:
            csvfile = request.FILES['csv']
            reader = LCHI()
            with transaction.atomic():
                for row in reader:
                    if (len(row) > 0):
                        voter = Voter()
                        voter.election = election
                        voter.identifier = row[0]
                        voter.email = row[1]
                        voter.save()
        except IntegrityError:
            return HttpResponse(json.dumps({'error': (('Voter with id ' + row[0]) + ' is already in the election')}), content_type='application/json', status=500)
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')

    @csrf_exempt
    def addVotersJson(request: LCHI(), election: LCLI()):
        try:
            data = cast(Dict[(str,  LCLI())], data)
            with transaction.atomic():
                for voterData in data['voterList']:
                    voter = Voter()
                    voter.election = election
                    voter.identifier = voterData['id']
                    voter.email = voterData['email']
                    voter.save()
        except IntegrityError:
            return HttpResponse(json.dumps({'error': (('Voter with id ' + voterData['id']) + ' is already in the election')}), content_type='application/json', status=500)
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() >= election.startDate):
            return HttpResponse(json.dumps({'error': 'The election has already started. Cannot add voters now.'}), content_type='application/json', status=500)
        if request.FILES:
            return addVotersFile(request, election)
        else:
            return addVotersJson(request, election)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
@csrf_exempt
def removeVoters(request: LCHI(), election_id: LCLI()):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() >= election.startDate):
            return HttpResponse(json.dumps({'error': 'The election has already started. Cannot remove voters now.'}), content_type='application/json', status=500)
        try:
            data = cast(Dict[(str,  LCLI())], data)
            for voterData in data['voterList']:
                Voter.objects.get(identifier=voterData, election=election).delete()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except Voter.DoesNotExist:
            pass
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def getVoters(request: LCHI(), election_id: LCLI()):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        data = serializers.serialize('json', list(Voter.objects.all().filter(election=election)))
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
@csrf_exempt
def addQuestions(request: LCHI(), election_id: LCLI()):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() >= election.startDate):
            return HttpResponse(json.dumps({'error': 'The election has already started. Cannot add questions now.'}), content_type='application/json', status=500)
        try:
            data = cast(Dict[(str,  LCHI())], data)
            with transaction.atomic():
                for questionData in data['questionList']:
                    question = Question()
                    question.election = election
                    question.question = questionData['question']
                    question.save()
                    for answerData in questionData['answers']:
                        answer = Answer()
                        answer.question = question
                        answer.answer = answerData
                        answer.save()
        except IntegrityError:
            return HttpResponse(json.dumps({'error': 'Cannot have duplicate question for the same election or duplicate answers for the same question'}), content_type='application/json', status=500)
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
@csrf_exempt
def removeQuestions(request: LCHI(), election_id):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() >= election.startDate):
            return HttpResponse(json.dumps({'error': 'The election has already started. Cannot remove questions now.'}), content_type='application/json', status=404)
        try:
            data = cast(Dict[(str,  LCHI())], data)
            for questionData in data['questionList']:
                Question.objects.get(id=questionData, election=election).delete()
        except Question.DoesNotExist:
            pass
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def getQuestions(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        data = getQuestionsAux(election)
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def register(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        try:
            voter = Voter.objects.get(identifier=request.user, election=election)
        except Voter.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Voter is not eligible for this election'}), content_type='application/json', status=404)
        if ((datetime.datetime.now() >= election.endDate) or (datetime.datetime.now() < election.startDate)):
            return HttpResponse(json.dumps({'error': 'The election is not currently running.'}), content_type='application/json', status=500)
        try:
            cryptoParameters = json.loads(election.cryptoParameters.replace("'", '"'))
            payload = {'election': str(election.id), 'electionName': election.name, 'cryptoParameters': {'p': cryptoParameters['p'], 'g': cryptoParameters['g'], 'q': cryptoParameters['q']}, 'voter': voter.identifier, 'email': voter.email}
            r = requests.post(settings.CREDENTIAL_AUTHORITY, data=json.dumps(payload))
            if (r.status_code != 200):
                return HttpResponse(json.dumps({'error': (str(r.status_code) + 'from credential Authority')}), content_type='application/json', status=r.status_code)
            data = r.json()
            voter.publicCredential = data['publicCredential']
            voter.save()
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
@csrf_exempt
def cast(request: LCHI(), election_id):
    try:
        election = HCLI()
    except Election.DoesNotExist:
        return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
    try:
        voter = Voter.objects.get(identifier=request.user, election=election)
    except Voter.DoesNotExist:
        return HttpResponse(json.dumps({'error': 'Voter is not eligible for this election'}), content_type='application/json', status=404)
    if (request.method == 'POST'):
        if (datetime.datetime.now() <= election.startDate):
            return HttpResponse(json.dumps({'error': 'The election has not started'}), content_type='application/json', status=404)
        if (datetime.datetime.now() >= election.endDate):
            return HttpResponse(json.dumps({'error': 'The election has ended'}), content_type='application/json', status=404)
        if ((election.openCastTime != None) and (election.closeCastTime != None)):
            if ((datetime.datetime.now().time() <= election.openCastTime) or (datetime.datetime.now().time() >= election.closeCastTime)):
                return HttpResponse(json.dumps({'error': ((('The ballot box is closed between ' + election.openCastTime) + ' and ') + election.closeCastTime)}), content_type='application/json', status=404)
        data = cast(Dict[(str,  LCHI())], data)
        try:
            if (voter.publicCredential != data['publicCredential']):
                return HttpResponse(json.dumps({'error': ('Invalid public credential for voter with id ' + voter.identifier)}), content_type='application/json', status=404)
            ballot = Ballot.objects.get(election=election, publicCredential=voter.publicCredential)
            return HttpResponse(json.dumps({'error': (('The voter with id ' + voter.identifier) + ' has already cast a ballot')}), content_type='application/json', status=404)
        except Ballot.DoesNotExist:
            try:
                questions = getQuestionsAux(election)
                randoms = json.loads(voter.proofRandomValues)
                cryptoParameters = json.loads(election.cryptoParameters.replace("'", '"'))
                p = int(cryptoParameters['p'])
                q = int(cryptoParameters['q'])
                g = int(cryptoParameters['g'])
                h = int(election.publicKey, 16)
                schnorr = Schnorr.Schnorr()
                schnorr.keys = {'pub': {'p': p, 'q': q, 'alpha': g, 'beta': int(data['publicCredential'])}}
                signMessage = 1
                for (i, question) in enumerate(questions['questionList']):
                    if (question['id'] not in data['ballot']):
                        return HttpResponse(json.dumps({'error': 'Ballot is not well formed'}), content_type='application/json', status=500)
                    questionData = cast(Dict[(str,  LCLI())], questionData)
                    totalAlpha = 1
                    totalAlpha = 1
                    totalBeta = 1
                    for (j, answer) in enumerate(question['answers']):
                        if (answer['id'] not in questionData['answers']):
                            return HttpResponse(json.dumps({'error': 'Ballot is not well formed'}), content_type='application/json', status=500)
                        answerData = cast(Dict[(str,  LCLI())], answerData)
                        alpha = int(answerData['alpha'])
                        beta = int(answerData['beta'])
                        totalAlpha = expressionHandler2(totalAlpha, alpha)
                        totalBeta = expressionHandler2(totalBeta, beta)
                        signMessage = expressionHandler2(expressionHandler2(signMessage, alpha), beta)
                        random = int(randoms[question['id']][answer['id']])
                        if (random == ((int(answerData['individualProof'][0]['challenge']) + int(answerData['individualProof'][1]['challenge'])) % p)):
                            print(answerData['individualProof'][0])
                            leftside2 = LCHI()
                            leftside2 = answerData['individualProof'][0]
                            proof0 = testProof(int(answerData['individualProof'][0]['challenge']), int(answerData['individualProof'][0]['response']), g, h, p, alpha, beta, 0)
                            print(proof0)
                            leftside3 = LCHI()
                            leftside3 = proof0
                            print(answerData['individualProof'][1])
                            leftside4 = LCHI()
                            leftside4 = answerData['individualProof'][1]
                            proof1 = testProof(int(answerData['individualProof'][1]['challenge']), int(answerData['individualProof'][1]['response']), g, h, p, alpha, beta, 1)
                            print(proof1)
                            leftside5 = LCHI()
                            leftside5 = proof1
                            if ((int(answerData['individualProof'][0]['A']) == proof0[0]) and (int(answerData['individualProof'][0]['B']) == proof0[1]) and (int(answerData['individualProof'][1]['A']) == proof1[0]) and (int(answerData['individualProof'][1]['B']) == proof1[1])):
                                continue
                            else:
                                return HttpResponse(json.dumps({'error': 'Proof verification failed.'}), content_type='application/json', status=500)
                        else:
                            return HttpResponse(json.dumps({'error': 'Proof verification failed.'}), content_type='application/json', status=500)
                    random = int(randoms[question['id']]['overall'])
                    if (random == ((int(questionData['overall_proof'][0]['challenge']) + int(questionData['overall_proof'][1]['challenge'])) % p)):
                        proof0 = testProof(int(questionData['overall_proof'][0]['challenge']), int(questionData['overall_proof'][0]['response']), g, h, p, totalAlpha, totalBeta, 0)
                        proof1 = testProof(int(questionData['overall_proof'][1]['challenge']), int(questionData['overall_proof'][1]['response']), g, h, p, totalAlpha, totalBeta, 1)
                        if ((int(questionData['overall_proof'][0]['A']) == proof0[0]) and (int(questionData['overall_proof'][0]['B']) == proof0[1]) and (int(questionData['overall_proof'][1]['A']) == proof1[0]) and (int(questionData['overall_proof'][1]['B']) == proof1[1])):
                            continue
                        else:
                            return HttpResponse(json.dumps({'error': 'Proof verification failed.'}), content_type='application/json', status=500)
                    else:
                        return HttpResponse(json.dumps({'error': 'Proof verification failed.'}), content_type='application/json', status=500)
                signMessage = expressionHandler2(signMessage, p)
                if (not schnorr.verify([int(data['ballot']['signature'][0]), int(data['ballot']['signature'][1])], signMessage)):
                    return HttpResponse(json.dumps({'error': 'Failed signature verification'}), content_type='application/json', status=500)
                ballot = Ballot()
                ballot.election = election
                ballot.publicCredential = voter.publicCredential
                ballot.ballot = data['ballot']
                ballot.SBT = hashlib.sha256(request.body).hexdigest()
                ballot.save()
            except Exception as exception:
                return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    elif (request.method == 'GET'):
        if voter.publicCredential:
            if (datetime.datetime.now() <= election.startDate):
                return render(request, 'closedBallotBox.html', {'election': election})
            if (datetime.datetime.now() >= election.endDate):
                return render(request, 'closedBallotBox.html', {'election': election})
            if ((election.openCastTime != None) and (election.closeCastTime != None)):
                if ((datetime.datetime.now().time() <= election.openCastTime) or (datetime.datetime.now().time() >= election.closeCastTime)):
                    return render(request, 'closedBallotBox.html', {'election': election})
            try:
                ballot = HCLI()
                return render(request, 'closedBallotBox.html', {'election': election})
            except Ballot.DoesNotExist:
                cryptoParameters = json.loads(election.cryptoParameters.replace("'", '"'))
                questions = getQuestionsAux(election)
                randoms = {}
                for question in questions['questionList']:
                    randoms[question['id']] = {}
                    randoms[question['id']]['overall'] = str(secrets.randbelow(int(cryptoParameters['p'])))
                    for answer in question['answers']:
                        randoms[question['id']][answer['id']] = str(secrets.randbelow(int(cryptoParameters['p'])))
                voter.proofRandomValues = json.dumps(randoms)
                voter.save()
                return render(request, 'ballotBox.html', {'election': election, 'questions': json.dumps(questions), 'randoms': json.dumps(randoms)})
        else:
            if ((datetime.datetime.now() >= election.endDate) or (datetime.datetime.now() <= election.startDate)):
                return render(request, 'closedBallotBox.html', {'election': election})
            if election.publicKey:
                return render(request, 'register.html', {'election': election, 'email': voter.email})
            else:
                return HttpResponse(json.dumps({'error': 'Election does not have a public key.'}), content_type='application/json', status=404)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def testProof(challenge, response, g, h, p, alpha, beta, message):
    A = expressionHandler2(expressionHandler2(pow(g, response, p), pow(pow(alpha, expressionHandler2(p, 2), p), challenge, p)), p)
    B = expressionHandler2(expressionHandler2(expressionHandler2(pow(h, response, p), pow(pow(beta, expressionHandler2(p, 2), p), challenge, p)), pow(g, expressionHandler2(message, challenge), p)), p)
    return (A, B)

@login_required
def election(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            raise Http404('Election does not exist')
        if (request.user == election.admin):
            endOfElection = False
            if (datetime.datetime.now() >= election.endDate):
                endOfElection = True
            return render(request, 'manageElection.html', {'election': election, 'endOfElection': endOfElection})
        else:
            return HttpResponseForbidden('Access denied')
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def manageTrustees(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            raise Http404('Election does not exist')
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        keyshares = {}
        for t in Trustee.objects.filter(election=election):
            if t.publicKeyShare:
                if ('pk' in json.loads(t.publicKeyShare.replace("'", '"'))):
                    keyshares[t.identifier] = json.loads(t.publicKeyShare.replace("'", '"'))
                    keyshares[t.identifier]['proof']['e'] = t.keyShareProofRandom
        return render(request, 'manageTrustees.html', {'election': election, 'keyShares': keyshares})
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def manageVoters(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            raise Http404('Election does not exist')
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        return render(request, 'manageVoters.html', {'election': election})
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def manageQuestions(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            raise Http404('Election does not exist')
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        return render(request, 'manageQuestions.html', {'election': election})
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def trustee(request: LCHI(), election_id):

    def getMethodTrustee(election, t: HCHI()):
        if (datetime.datetime.now() < election.startDate):
            try:
                if (not t.keyShareProofRandom):
                    t.keyShareProofRandom = str(secrets.randbelow(int(ast.literal_eval(election.cryptoParameters)['p'])))
                    t.save()
                    return render(request, 'generateKeyShare.html', {'election': election, 'trustee': t})
                else:
                    return render(request, 'generateKeyShare.html', {'election': election, 'trustee': t})
            except Exception as exception:
                return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
        elif ((datetime.datetime.now() > election.endDate) and election.aggregatedEncTally):
            cryptoParams = HCLI()
            questions = getQuestionsAux(election)
            if (not t.partialDecryption):
                randoms = {}
                for question in questions['questionList']:
                    randoms[question['id']] = {}
                    for answer in question['answers']:
                        randoms[question['id']][answer['id']] = str(secrets.randbelow(int(cryptoParams['p'])))
                try:
                    t.decryptionProofRandom = json.dumps(randoms)
                    t.save()
                except:
                    return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
            return render(request, 'partialDecrypt.html', {'election': election, 'trustee': t, 'aggregatedEncTally': election.aggregatedEncTally.replace("'", '"'), 'p': cryptoParams['p'], 'g': cryptoParams['g'], 'randoms': json.dumps(t.decryptionProofRandom)})
        else:
            return render(request, 'generateKeyShare.html', {'election': election, 'trustee': t, 'started': True})

    def postMethodTrustee(election: HCHI, t):
        if (datetime.datetime.now() < election.startDate):
            if t.publicKeyShare:
                return HttpResponse(json.dumps({'error': 'You have already generated a key share'}), content_type='application/json', status=500)
            else:
                data = cast(Dict[(str,  LCLI())], data)
                if ('pk' in data):
                    t.publicKeyShare = data
                    try:
                        t.save()
                    except Exception as exception:
                        return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
                    return HttpResponse(json.dumps({'success': True}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'error': 'Bad json. Does not have necessary elements.'}), content_type='application/json', status=500)
        elif (datetime.datetime.now() > election.endDate):
            return
        else:
            return HttpResponseForbidden('Access denied')
    try:
        election = HCLI()
    except Election.DoesNotExist:
        raise Http404('Election does not exist')
    try:
        t = Trustee.objects.get(election=election, identifier=request.user)
    except Trustee.DoesNotExist:
        return HttpResponseForbidden('Access denied')
    if (request.method == 'GET'):
        return getMethodTrustee(election, t)
    elif (request.method == 'POST'):
        return postMethodTrustee(election, t)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@login_required
def trusteeElectionList(request: LCLI()):
    if (request.method == 'GET'):
        t = Trustee.objects.filter(identifier=request.user)
        return render(request, 'trusteeElectionList.html', {'trustee': t})
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def addElectionPublicKey(request: LCHI(), election_id):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            raise Http404('Election does not exist')
        if (election.admin != request.user):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() >= election.startDate):
            return HttpResponse(json.dumps({'error': 'The election has already started. Cannot set the public key.'}), content_type='application/json', status=404)
        if election.publicKey:
            return HttpResponse(json.dumps({'error': 'The election already has a public key'}), content_type='application/json', status=404)
        try:
            data = cast(Dict[(str,  LCLI())], data)
            if ('pk' in data):
                election.publicKey = data['pk']
                election.save()
                return HttpResponse(json.dumps({'sucess': True}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'error': 'The json is not well formed.'}), content_type='application/json', status=404)
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def bulletinBoard(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            raise Http404('Election does not exist')
        keyshares = {}
        for t in Trustee.objects.filter(election=election):
            if t.publicKeyShare:
                if ('pk' in json.loads(t.publicKeyShare.replace("'", '"'))):
                    keyshares[t.identifier] = json.loads(t.publicKeyShare.replace("'", '"'))
        voters = {}
        for voter in Voter.objects.filter(election=election):
            if voter.paperVoter:
                voters[voter.identifier] = 'paper Voter'
                continue
            if voter.publicCredential:
                try:
                    ballot = Ballot.objects.get(election=election, publicCredential=voter.publicCredential)
                    voters[voter.identifier] = ballot.SBT
                except Ballot.DoesNotExist:
                    voters[voter.identifier] = ''
            else:
                voters[voter.identifier] = ''
        tally = None
        if election.tally:
            tally = json.loads(election.tally.replace("'", '"'))
        return render(request, 'bulletinBoard.html', {'election': election, 'keyShares': keyshares, 'voters': voters, 'tally': tally, 'eligibleVoter': (str(request.user) in voters.keys())})
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def auditBallot(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            raise Http404('Election does not exist')
        questions = getQuestionsAux(election)
        try:
            voter = Voter.objects.get(identifier=request.user, election=election)
        except Voter.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Voter is not eligible for this election'}), content_type='application/json', status=404)
        randoms = voter.proofRandomValues
        if randoms:
            return render(request, 'auditBallot.html', {'election': election, 'questions': json.dumps(questions), 'randoms': randoms})
        else:
            return HttpResponse(json.dumps({'error': "Voter didn't access ballot box to create a ballot"}), content_type='application/json', status=404)
    else:
        return HttpResponseNotAllowed(['GET'])

def getQuestionsAux(election: HCLI()):
    data = {'questionList': []}
    for question in Question.objects.all().filter(election=election):
        questionData = HCLI()
        questionData['id'] = str(question.id)
        questionData['question'] = question.question
        questionData['answers'] = []
        for answer in Answer.objects.all().filter(question=question):
            questionData['answers'].append({'id': str(answer.id), 'answer': answer.answer})
        data['questionList'].append(questionData)
    return data

@login_required
def manageTally(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            raise Http404('Election does not exist')
        if (request.user == election.admin):
            if (datetime.datetime.now() >= election.endDate):
                paperVoters = Voter.objects.filter(election=election, paperVoter=True)
                paperVotersIdentifiers = paperVoters.values_list('identifier', flat=True)
                paperVoterCredentials = paperVoters.values_list('publicCredential', flat=True)
                ballots = []
                numberOfEBallots = 0
                for b in Ballot.objects.filter(election=election).exclude(publicCredential__in=paperVoterCredentials).values_list('ballot', flat=True):
                    ballots.append(json.loads(b.replace("'", '"')))
                    numberOfEBallots += 1
                finalEBallots = json.dumps({'ballotList': ballots})
                cryptoParameters = json.loads(election.cryptoParameters.replace("'", '"'))
                trustees = Trustee.objects.filter(election=election)
                partialDecryptions = {'partialDecryptionList': []}
                numberOfPartialeDecryptions = 0
                for t in trustees:
                    if t.partialDecryption:
                        p = json.loads(t.partialDecryption.replace("'", '"'))
                        p['publicKeyShare'] = json.loads(t.publicKeyShare.replace("'", '"'))
                        p['randoms'] = json.loads(t.decryptionProofRandom.replace("'", '"'))
                        partialDecryptions['partialDecryptionList'].append(p)
                        numberOfPartialeDecryptions += 1
                return render(request, 'manageTally.html', {'election': election, 'paperVoters': paperVotersIdentifiers, 'questions': json.dumps(getQuestionsAux(election)), 'p': cryptoParameters['p'], 'g': cryptoParameters['g'], 'trustees': trustees, 'partialDecryptions': json.dumps(partialDecryptions), 'numberOfEBallots': numberOfEBallots, 'ready': (numberOfPartialeDecryptions == len(trustees.values_list('publicKeyShare', flat=True)))})
            else:
                return HttpResponseForbidden('Election has not yet ended. Cannot manage tally without election ending.')
        else:
            return HttpResponseForbidden('Access denied')
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def addPaperVoters(request: LCHI(), election_id):

    def addPaperVotersFile(request: LCHI(), election):
        try:
            csvfile = request.FILES['csv']
            reader = csv.reader(csvfile.read().decode('utf-8-sig').split('\n'), delimiter=';')
            with transaction.atomic():
                for row in reader:
                    if (len(row) > 0):
                        voter = Voter.objects.get(identifier=row[0], election=election)
                        voter.paperVoter = True
                        voter.save()
        except Voter.DoesNotExist:
            return HttpResponse(json.dumps({'error': (('Voter with id ' + row[0]) + 'is not an eligible voter.')}), content_type='application/json', status=500)
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() <= election.endDate):
            return HttpResponse(json.dumps({'error': 'The election has not ended. Cannot add paper voters yet!'}), content_type='application/json', status=404)
        if request.FILES:
            return addPaperVotersFile(request, election)
        else:
            return HttpResponse(json.dumps({'error': 'No file submited'}), content_type='application/json', status=404)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
@csrf_exempt
def removePaperVoters(request: LCHI(), election_id):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() <= election.endDate):
            return HttpResponse(json.dumps({'error': 'The election has not ended. Cannot manage paper voters.'}), content_type='application/json', status=404)
        try:
            data = cast(Dict[(str,  LCLI())], data)
            for voterData in data['voterList']:
                voter = Voter.objects.get(identifier=voterData, election=election)
                voter.paperVoter = False
                voter.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except Voter.DoesNotExist:
            pass
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def submitPaperResults(request: LCHI(), election_id):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() <= election.endDate):
            return HttpResponse(json.dumps({'error': 'The election has not ended. Cannot submit paper voting results.'}), content_type='application/json', status=404)
        try:
            data = cast(Dict[(str,  LCLI())], data)
            questions = getQuestionsAux(election)
            for (i, question) in enumerate(questions['questionList']):
                if (question['id'] not in data.keys()):
                    return HttpResponse(json.dumps({'error': 'Incomplete Results.'}), content_type='application/json', status=500)
                for answer in questions['questionList'][i]['answers']:
                    if (answer['id'] not in data[question['id']].keys()):
                        return HttpResponse(json.dumps({'error': 'Incomplete Results.'}), content_type='application/json', status=500)
            numberOfPaperVoters = len(Voter.objects.filter(election=election, paperVoter=True))
            for question in data:
                numberOfPaperVotes = 0
                for answer in data[question]:
                    numberOfPaperVotes = expressionHandler2(numberOfPaperVotes, int(data[question][answer]))
                if (numberOfPaperVoters != numberOfPaperVotes):
                    return HttpResponse(json.dumps({'error': "Number of paper votes and voters doesn't match. Please review them"}), content_type='application/json', status=500)
            election.paperResults = data
            election.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def submitPartialDecryption(request: LCHI(), election_id):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        try:
            t = Trustee.objects.get(election=election, identifier=request.user)
        except Trustee.DoesNotExist:
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() <= election.endDate):
            return HttpResponse(json.dumps({'error': 'The election has not ended. Cannot submit partial decryption.'}), content_type='application/json', status=404)
        if (not t.publicKeyShare):
            return HttpResponse(json.dumps({'error': "Trustee didn't participate in the protocol"}), content_type='application/json', status=500)
        if (not election.aggregatedEncTally):
            return HttpResponse(json.dumps({'error': 'Trustee cannot submit decryption without aggregated tally'}), content_type='application/json', status=500)
        data = cast(Dict[(str,  LCLI())], data)
        questions = getQuestionsAux(election)
        for question in questions['questionList']:
            if (question['id'] not in data.keys()):
                return HttpResponse(json.dumps({'error': 'Partial Decryption not well formed.'}), content_type='application/json', status=500)
            for answer in question['answers']:
                if (answer['id'] not in data[question['id']].keys()):
                    return HttpResponse(json.dumps({'error': 'Partial Decryption not well formed.'}), content_type='application/json', status=500)
        try:
            t.partialDecryption = data
            t.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def publishResults(request: LCHI(), election_id):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() <= election.endDate):
            return HttpResponse(json.dumps({'error': 'The election has not ended. Cannot submit election tally.'}), content_type='application/json', status=404)
        try:
            data = cast(Dict[(str,  LCLI())], data)
            paperVoters = Voter.objects.filter(election=election, paperVoter=True)
            paperVoterCredentials = paperVoters.values_list('publicCredential', flat=True)
            NumberEVoters = Ballot.objects.filter(election=election).exclude(publicCredential__in=paperVoterCredentials)
            questions = getQuestionsAux(election)
            for question in questions['questionList']:
                numberOfVotes = 0
                if (question['id'] not in data.keys()):
                    return HttpResponse(json.dumps({'error': 'Results not well formed.'}), content_type='application/json', status=500)
                for answer in question['answers']:
                    if (answer['id'] not in data[question['id']][1].keys()):
                        return HttpResponse(json.dumps({'error': 'Results not well formed.'}), content_type='application/json', status=500)
                    numberOfVotes = expressionHandler2(numberOfVotes, int(data[question['id']][1][answer['id']][1]))
                if ((len(NumberEVoters) + len(paperVoters)) != numberOfVotes):
                    return HttpResponse(json.dumps({'error': 'Results are invalid. Different number of voters and votes'}), content_type='application/json', status=500)
            election.tally = data
            election.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def deleteElection(request: LCHI(), election_id):
    if (request.method == 'POST'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        try:
            election.delete()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except Exception as exception:
            return HttpResponse(json.dumps({'error': repr(exception)}), content_type='application/json', status=500)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def aggregateEncTally(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if (request.user != election.admin):
            return HttpResponseForbidden('Access denied')
        if (datetime.datetime.now() >= election.endDate):
            paperVoters = Voter.objects.filter(election=election, paperVoter=True)
            paperVoterCredentials = paperVoters.values_list('publicCredential', flat=True)
            ballots = []
            numberOfEBallots = 0
            for b in Ballot.objects.filter(election=election).exclude(publicCredential__in=paperVoterCredentials).values_list('ballot', flat=True):
                ballots.append(json.loads(b.replace("'", '"')))
                numberOfEBallots += 1
            questions = getQuestionsAux(election)
            result = {}
            p = int(json.loads(election.cryptoParameters.replace("'", '"'))['p'])
            for question in questions['questionList']:
                result[question['id']] = {}
                for answer in question['answers']:
                    for ballot in ballots:
                        ballotAnswer = ballot[question['id']]['answers'][answer['id']]
                        if (answer['id'] in result[question['id']]):
                            alpha = result[question['id']][answer['id']]['alpha']
                            beta = result[question['id']][answer['id']]['beta']
                            aux = {'alpha': expressionHandler2(expressionHandler2(alpha, int(ballotAnswer['alpha'])), p), 'beta': expressionHandler2(expressionHandler2(beta, int(ballotAnswer['beta'])), p)}
                        else:
                            aux = {'alpha': int(ballotAnswer['alpha']), 'beta': int(ballotAnswer['beta'])}
                        result[question['id']][answer['id']] = aux
                    result[question['id']][answer['id']]['alpha'] = str(result[question['id']][answer['id']]['alpha'])
                    result[question['id']][answer['id']]['beta'] = str(result[question['id']][answer['id']]['beta'])
            election.aggregatedEncTally = json.dumps(result)
            election.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        else:
            return HttpResponseForbidden('Election has not yet ended. Cannot manage tally without election ending.')
    else:
        return HttpResponseNotAllowed(['GET'])

def exportData(request: LCHI(), election_id):
    if (request.method == 'GET'):
        try:
            election = HCLI()
        except Election.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Election does not exist'}), content_type='application/json', status=404)
        if election.tally:
            export = {}
            electionExport = {}
            electionExport['uuid'] = str(election.id)
            electionExport['name'] = election.name
            electionExport['CryptoParameters'] = json.loads(election.cryptoParameters.replace("'", '"'))
            electionExport['ElectionPublicKey'] = election.publicKey
            electionExport['questions'] = getQuestionsAux(election)
            electionExport['aggregatedEncryptedTally'] = json.loads(election.aggregatedEncTally)
            trusteesExport = {}
            for t in Trustee.objects.filter(election=election):
                if t.publicKeyShare:
                    if ('pk' in json.loads(t.publicKeyShare.replace("'", '"'))):
                        trusteesExport[t.identifier] = {}
                        trusteesExport[t.identifier]['KeyShare'] = json.loads(t.publicKeyShare.replace("'", '"'))
                        trusteesExport[t.identifier]['KeyShare']['proof']['e'] = t.keyShareProofRandom
                        trusteesExport[t.identifier]['PartialDecryptions'] = json.loads(t.partialDecryption.replace("'", '"'))
                        trusteesExport[t.identifier]['PartialDecryptionsRandom'] = json.loads(t.decryptionProofRandom.replace("'", '"'))
            ballotsExport = {}
            paperVoters = Voter.objects.filter(election=election, paperVoter=True)
            paperVoterCredentials = paperVoters.values_list('publicCredential', flat=True)
            numberOfEBallots = 0
            for b in Ballot.objects.filter(election=election).exclude(publicCredential__in=paperVoterCredentials):
                ballotsExport[b.publicCredential] = {}
                ballotsExport[b.publicCredential]['ballotData'] = json.loads(b.ballot.replace("'", '"'))
                ballotsExport[b.publicCredential]['SBT'] = b.SBT
            export['election'] = electionExport
            export['trusteesData'] = trusteesExport
            export['ballotExport'] = ballotsExport
            response = HttpResponse(json.dumps(export), content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename=export.json'
            return response
        else:
            return HttpResponse(json.dumps({'error': "Election doesn't have the results publishes yet!"}), content_type='application/json', status=404)
    else:
        return HttpResponseNotAllowed(['GET'])

