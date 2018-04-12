"""
	This program aims at proving by enumeration that our algorithm for the System
	Experiment is effective. In the output file (case_enmu.txt), the program prints
	every possible case of all players' status and the player index of the renegade.
	Under each case, if the renegade wins, the program will end with printing the
	messages the renegade sends; otherwise, the program goes on to the next case
	without any output. If all cases are examined without renegade's success, 
	the program will end with printing 'Succeeded!'.

	This program is only a coarse example of case enumeration without adequate
	optimization of time or space. Nevertheless its correctness is ensured.
"""


PLAYER_NUM = 5

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
bool_lists = []
for b1 in [True, False]:
	for b2 in [True, False]:
		for b3 in [True, False]:
			for b4 in [True, False]:
				for b5 in [True, False]:
					bool_lists.append([b1, b2, b3, b4, b5])

def oneRound(receiver_id, ren1, ren2, ren3):
	# ren1: status which renegade sender provides for receiver
	# ren2: list of status which renegade receiver answers to each sender
	# ren3: list of status which renegade sender confirms to each sender

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
	# meaning of ren1, ren2, ren3 is the same as those in oneRound()

	players[renegade_id].role = "renegade"
	fightable = 0 # how many loyalists are able to attack
	for i in xrange(PLAYER_NUM):
		players[i].clr()
		players[i].status = status_list[i]
		if players[i].status and players[i].role == "loyal":
			fightable += 1

	for d in xrange(3):
		oneRound(d, ren1, ren2, ren3) # let receiver be 1, 2, 3

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
	for status_list in bool_lists:
		for renegade_id in xrange(PLAYER_NUM):
			fo.write("\nstatus: " + str(status_list) + "\n")
			fo.write("renegade: %d\n" % renegade_id)
			for ren1 in [True, False]:
				for ren2 in bool_lists:
					for ren3 in bool_lists:
						if not oneDay(status_list, renegade_id, ren1, ren2, ren3):
							fo.write("Failed! Error occured with following renegade moves:\n")
							fo.write("renegade provide for receiver: " + str(ren1) + "\n")
							fo.write("renegade receiver answers: " + str(ren2) + "\n")
							fo.write("renegade confirm with other senders: " + str(ren3) + "\n")
							return False
	return True

if play():
	fo.write("\nSucceeded!")
