from math import factorial, ceil
import matplotlib.pyplot as plt

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
	c = 30
	p = 0.6
	tmp = majVoteProb(c, p)
	print(f'Probability of correct majority vote for {c} people with individual correctness probability {p}: {round(tmp, 3)}')

def part2c():
	groupSize = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50]
	pRadiologist = 0.85
	pDoctor = 0.75
	pMedStudent = 0.6
	tmpR = [majVoteProb(gs, pRadiologist) for gs in groupSize]
	tmpD = [majVoteProb(gs, pDoctor) for gs in groupSize]
	tmpM = [majVoteProb(gs, pMedStudent) for gs in groupSize]

	plt.plot(groupSize, tmpR, color='green', label='Radiologist')
	plt.plot(groupSize, tmpD, color='red', label='Doctor')
	plt.plot(groupSize, tmpM, color='blue', label='Medical student')
	plt.legend()
	plt.xlabel('Group size')
	plt.ylabel('Probability correct majority vote')
	plt.savefig('A5Q2C.png')
	plt.show()

if __name__ == "__main__":
	part2b()
	part2c()
