import numpy as np
import matplotlib.pyplot as plt


#Corpus: I like deep learning. I like NLP. I enjoy sailing.
la = np.linalg
words = ["I", "like", "enjoy", "deep", "learning", "NLP", "sailing", "."]

X = np.array([[0,2,1,0,0,0,0,0],
			  [2,0,0,1,0,1,0,0],
			  [1,0,0,0,0,0,1,0],
			  [0,1,0,0,1,0,0,0],
			  [0,0,0,1,0,0,0,1],
			  [0,1,0,0,0,0,0,1],
			  [0,0,1,0,0,0,0,1],
			  [0,0,0,0,1,1,1,0]])

print('before svd')
U, s, V = la.svd(X, full_matrices=False)
print('after svd')


for i in range(len(words)):
	plt.text(U[i, 0], U[i, 1], words[i])
print('after loop')

plt.show()
