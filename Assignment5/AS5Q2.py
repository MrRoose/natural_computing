from math import factorial, ceil

def majVoteProb(c, p):
	m = ceil((c+1)/2)
	totalMajProb = 0
	correctVotes = m

	while (correctVotes <= c):
		incorrectVotes = c - correctVotes
		combIncVotes = factorial(c) / factorial(incorrectVotes) / factorial(c-incorrectVotes)
		majProb = (p ** correctVotes) * ((1-p) ** incorrectVotes)
		totalMajProb = totalMajProb + majProb * combIncVotes
		correctVotes = correctVotes + 1
	
	return totalMajProb

def part2b():
	c = 31
	p = 0.6
	tmp = majVoteProb(c, p)
	print(f'Probability of correct majority vote for {c} people with individual correctness probability {p}: {round(tmp, 3)}')


if __name__ == "__main__":
	part2b()
