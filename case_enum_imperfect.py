"""
	This program aims at proving by enumeration that our PREVIOUS algorithm for
	the System Experiment is NOT effective. In the output file
	(case_enum_imperfect.txt), the program prints some cases of all players'
	status and the player index of the renegade. Not all cases are enumerated
	because it's not necessary to do so. The cases that are taken into
	consideration and the reason why they represent all cases will be given below.

	Under each case, if the renegade wins, the program will end with printing the
	messages the renegade sends; otherwise, the program goes on to the next case
	without any output. If all cases are examined without renegade's success, 
	the program will end with printing 'Succeeded!'.

	Only such cases are enumerated that meet all the conditions below:
		C0: Receivers' indices are 0, 1 and 2.
		C1: Renegade's index is 0 or 3, whose status is always True.
		C2: The loyalists whose statuses are False are those who have the biggest
	0, 1, 2, 3 or 4 indices among all loyalists.
		C3: The response status returned by renegade receiver (according to C0 and
	C1, its index must be 0) is among the following: all True, only 4 is False, 3
	and 4 is False, only 1 is True, all False.

	Proof of that the cases above represent all conditions:
		C0: Who acts as the receiver does nothing with the whole process.
		C1: All receivers are equivalent to each other, all senders are equivalent
	to each other, and a receiver isn't equivalent to a sender. Therefore, given
	the cases where the renegade will be a receiver in one round and the cases where
	the renegade will remain a sender, we only need to test one case of each. 
	Moreover, renegade's message doesn't deal with its status, so it is safe to
	let its status always be True.
		C2: Considering the initial status, all loyalists are equivalent to each
	other. Thus it doesn't matter which loyalists are distributed with False.
		C3: Loyalists' decisions after receiving the response status only rely on
	the response itself, and once the number of True among the responses is given,
	it doesn't matter which senders receive True and which receive False.
"""


PLAYER_NUM = 5 #whose indices are 0, 1, 2, 3 and 4

fo = open("case_enum_imperfect.txt", "w")


class Player(object):
	def __init__(self, ID):
		self.id = ID #identity number
		self.status = False #whether one can attack or not
		self.role = "loyal" #loyal: must be faithful; renegade: arbitrarily move
		self.recv = {} #{sender_id : status that player with such id sends to self}
		self.rounds = [] #list of modified status sent to self each round
		self.decision = False #final choice whether to attack every day

	def sendTo(self, player, status):
		player.recv[self.id] = status

	def clr(self): # initialize all attributes except id
		self.status = False
		self.role = "loyal"
		self.recv = {}
		self.rounds = []
		self.decision = False


def others(*args):
	return [i for i in xrange(PLAYER_NUM) if i not in args]

players = [Player(i) for i in xrange(PLAYER_NUM)]

bool_lists_0 = [
	[True, True, True, True, True],
	[True, True, True, True, False],
	[True, True, True, False, False],
	[True, True, False, False, False],
	[True, False, False, False, False]
]

bool_lists_3 = [
	[True, True, True, True, True],
	[True, True, True, True, False],
	[True, True, False, True, False],
	[True, False, False, True, False],
	[False, False, False, True, False]
]

def oneRound(renegade_id, receiver_id, ren1, ren2):
	global players
	# ren1: status which renegade sender provides for receiver
	# ren2: list of status which renegade receiver answers to each sender

	players[renegade_id].role = "renegade"
	for p in players:
		p.recv = {}

	# senders 'send' their status to receiver. Actually we don't even need to call sendTo() method.
	# if status is True, then fight_count add 1
	fight_count = 1 if players[receiver_id].status else 0
	for i in others(receiver_id):
		status = ren1 if (players[i].role == "renegade") else players[i].status
		if status:
			fight_count += 1

	# receiver answers back to senders
	if players[receiver_id].role == "loyal": # for loyalists, (including self) 3 True or over then answer True
		answer = (fight_count >= 3)
		players[receiver_id].rounds.append(answer)
		for i in others(receiver_id):
			players[receiver_id].sendTo(players[i], answer)
	else: # for renegade, arbitrarily answer back
		for i in others(receiver_id):
			answer = ren2[i]
			players[receiver_id].sendTo(players[i], answer)

	# senders directly record the response statuses as their roundend statuses
	for i in others(receiver_id):
		players[i].rounds.append(players[i].recv[receiver_id])

def oneDay(status_list, renegade_id, ren1, ren2):
	global players
	# meaning of ren1, ren2 is the same as those in oneRound()

	fightable = 0 # how many loyalists are able to attack
	for i in xrange(PLAYER_NUM):
		players[i].clr()
		players[i].status = status_list[i]

	for d in xrange(3):
		oneRound(renegade_id, d, ren1[d], ren2[d]) # let receiver be 0, 1, 2

	for i in xrange(PLAYER_NUM):
		if players[i].status and players[i].role == "loyal":
			fightable += 1

	# make choices according to the results of three rounds
	# if more of what I received (after modification) is True, then attack, and vice versa
	fight = False
	for i in xrange(PLAYER_NUM):
		players[i].decision = (players[i].rounds.count(True) > players[i].rounds.count(False))
		if players[i].role == "loyal" and players[i].decision:
			fight = True

	# if two loyalists make diff choices, then lose
	for i in xrange(PLAYER_NUM):
		for j in xrange(PLAYER_NUM):
			if players[i].role == "loyal" and players[j].role == "loyal" \
			and players[i].decision != players[j].decision:
				return False

	# if the number of attackable loyalists and loyalists' decision don't match the rule, then lose
	# rule: 3 or more can attack, then must attack; 1 or less can attack, then mustn't attack
	# 2 can attack, then arbitrarily choose
	if (fightable >= 3 and not fight) or (fightable <= 1 and fight):
		return False

	return True

def play():
	global players
	for renegade_id in [0, 3]:
		if renegade_id == 0:
			for status_list in bool_lists_0:
				ren1_1 = True
				for ren1_2 in [True, False]:
					for ren1_3 in [True, False]:
						ren1 = [ren1_1, ren1_2, ren1_3]
						ren2_2 = bool_lists_0[0]
						ren2_3 = ren2_2
						for ren2_1 in bool_lists_0:
							ren2 = [ren2_1, ren2_2, ren2_3]
							fo.write("status: " + str(status_list) + "\n")
							fo.write("renegade: 0\n")
							for i in xrange(3):
								fo.write("renegade sends to receiver in round %d: " % (i + 1) + str(ren1[i]) + "\n")
							for i in xrange(3):
								fo.write("renegade returns to senders in round %d: " % (i + 1) + str(ren2[i]) + "\n")
							fo.write("\n")
							if not oneDay(status_list, renegade_id, ren1, ren2):
								fo.write("Failed!\n")
								return False
		elif renegade_id == 3:
			for status_list in bool_lists_3:
				for ren1_1 in [True, False]:
					for ren1_2 in [True, False]:
						for ren1_3 in [True, False]:
							ren1 = [ren1_1, ren1_2, ren1_3]
							ren2 = [bool_lists_3[0]] * 3
							fo.write("status: " + str(status_list) + "\n")
							fo.write("renegade: 3\n")
							for i in xrange(3):
								fo.write("renegade sends to receiver in round %d: " % (i + 1) + str(ren1[i]) + "\n")
							for i in xrange(3):
								fo.write("renegade returns to senders in round %d: " % (i + 1) + str(ren2[i]) + "\n")
							fo.write("\n")
							if not oneDay(status_list, renegade_id, ren1, ren2):
								fo.write("Failed!\n")
								return False
	return True

if play():
	fo.write("Succeeded!\n")
