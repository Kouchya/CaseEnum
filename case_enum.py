"""
	This program aims at proving by enumeration that our algorithm for the System
	Experiment is effective. In the output file (case_enum.txt), the program prints
	some cases of all players' status and the player index of the renegade. Not all
	cases are enumerated because it's not necessary to do so. The cases that are
	taken into consideration and the reason why they represent all cases will be
	given below.

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
		C4: The confirmation status sent by renegade sender contains 0, 1, 2 or 3
	False, and those who receive False from renegade sender are those who have the
	biggest 0, 1, 2 or 3 indices among all loyalist senders.

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
		C4: The roundend statuses loyalists record only rely on the confirmation
	statuses they just received, and since the rule forces all loyalists to record
	the same roundend status, it doesn't matter which loyalists receive confirmation
	status of True and which receive False.
"""


PLAYER_NUM = 5 #whose indices are 0, 1, 2, 3 and 4

fo = open("case_enum.txt", "w")


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

b01_lists = []
b1 = b2 = True
for b3 in [True, False]:
	for b4 in [True, False]:
		if not b3 and b4:
			continue
		for b5 in [True, False]:
			if not b4 and b5:
				continue
			b01_lists.append([b1, b2, b3, b4, b5])

b02_lists = []
b1 = b3 = True
for b2 in [True, False]:
	for b4 in [True, False]:
		if not b2 and b4:
			continue
		for b5 in [True, False]:
			if not b4 and b5:
				continue
			b02_lists.append([b1, b2, b3, b4, b5])

b03_lists = []
b1 = b4 = True
for b2 in [True, False]:
	for b3 in [True, False]:
		if not b2 and b3:
			continue
		for b5 in [True, False]:
			if not b3 and b5:
				continue
			b03_lists.append([b1, b2, b3, b4, b5])

b13_lists = []
b2 = b4 = True
for b1 in [True, False]:
	for b3 in [True, False]:
		if not b1 and b3:
			continue
		for b5 in [True, False]:
			if not b3 and b5:
				continue
			b13_lists.append([b1, b2, b3, b4, b5])

b23_lists = []
b3 = b4 = True
for b1 in [True, False]:
	for b2 in [True, False]:
		if not b1 and b2:
			continue
		for b5 in [True, False]:
			if not b2 and b5:
				continue
			b23_lists.append([b1, b2, b3, b4, b5])

def oneRound(renegade_id, receiver_id, ren1, ren2, ren3):
	global players
	# ren1: status which renegade sender provides for receiver
	# ren2: list of status which renegade receiver answers to each sender
	# ren3: list of status which renegade sender confirms to each sender

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

	# senders confirm the status returned by receiver with each other
	for i in others(receiver_id):
		for j in others(receiver_id, i):
			if players[i].role == "loyal":
				confirm = players[i].recv[receiver_id]
				players[i].sendTo(players[j], confirm)
			else:
				players[i].sendTo(players[j], ren3[j])

	# senders modify the effective status sent back by receiver
	# if 1 or less diff from what I received, then I don't modify what receiver sends to me
	# if 2 diff from what I received, then I change what receiver sends to me to False
	# if 3 diff from what I received, then I reverse what receiver sends to me
	for i in others(receiver_id):
		diff_count = 0
		for j in others(receiver_id, i):
			if players[i].recv[j] != players[i].recv[receiver_id]:
				diff_count += 1
		if diff_count <= 1:
			players[i].rounds.append(players[i].recv[receiver_id])
		elif diff_count == 2:
			players[i].rounds.append(False)
		elif diff_count == 3:
			players[i].rounds.append(not players[i].recv[receiver_id])

def oneDay(status_list, renegade_id, ren1, ren2, ren3):
	global players
	# meaning of ren1, ren2, ren3 is the same as those in oneRound()

	fightable = 0 # how many loyalists are able to attack
	for i in xrange(PLAYER_NUM):
		players[i].clr()
		players[i].status = status_list[i]

	for d in xrange(3):
		oneRound(renegade_id, d, ren1[d], ren2[d], ren3[d]) # let receiver be 0, 1, 2

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
							ren3_1 = bool_lists_0[0]
							for ren3_2 in b01_lists:
								for ren3_3 in b02_lists:
									ren3 = [ren3_1, ren3_2, ren3_3]
									fo.write("status: " + str(status_list) + "\n")
									fo.write("renegade: 0\n")
									for i in xrange(3):
										fo.write("renegade sends to receiver in round %d: " % (i + 1) + str(ren1[i]) + "\n")
									for i in xrange(3):
										fo.write("renegade returns to senders in round %d: " % (i + 1) + str(ren2[i]) + "\n")
									for i in xrange(3):
										fo.write("renegade confirms to others in round %d: " % (i + 1) + str(ren3[i]) + "\n")
									fo.write("\n")
									if not oneDay(status_list, renegade_id, ren1, ren2, ren3):
										fo.write("Failed!\n")
										return False
		elif renegade_id == 3:
			for status_list in bool_lists_3:
				for ren1_1 in [True, False]:
					for ren1_2 in [True, False]:
						for ren1_3 in [True, False]:
							ren1 = [ren1_1, ren1_2, ren1_3]
							ren2 = [bool_lists_3[0]] * 3
							for ren3_1 in b03_lists:
								for ren3_2 in b13_lists:
									for ren3_3 in b23_lists:
										ren3 = [ren3_1, ren3_2, ren3_3]
										fo.write("status: " + str(status_list) + "\n")
										fo.write("renegade: 3\n")
										for i in xrange(3):
											fo.write("renegade sends to receiver in round %d: " % (i + 1) + str(ren1[i]) + "\n")
										for i in xrange(3):
											fo.write("renegade returns to senders in round %d: " % (i + 1) + str(ren2[i]) + "\n")
										for i in xrange(3):
											fo.write("renegade confirms to others in round %d: " % (i + 1) + str(ren3[i]) + "\n")
										fo.write("\n")
										if not oneDay(status_list, renegade_id, ren1, ren2, ren3):
											fo.write("Failed!\n")
											return False
	return True

if play():
	fo.write("Succeeded!\n")
