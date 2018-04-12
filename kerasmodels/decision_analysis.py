import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon

test_result_file = 'D:\\PycharmProjects\\Lobster\\data\\logs\\keras_debug_logs\\matthew_network\\unfrozen_cov\\training_results.pkl'
pickled_test_result = open(test_result_file,'rb')
per_class_test_results = pickle.load(pickled_test_result)['raw_test_results']

x_correct = []
x_incorrect = []
N = 0
acc = 0

for label in per_class_test_results:
    results = per_class_test_results[label]
    for result in results:
        if result['prediction']:
            x_correct.append(result['max_score'])
            acc += 1.
        else:
            x_incorrect.append(result['max_score'])
        N += 1.
acc = acc/N

def compute_xent(x):
    return -np.log(np.array(x))

def estimate_lambda(x):
    return x.size/np.sum(x)

def compute_marginal(p_x_0, p_x_1, p_0, p_1):
    return p_0 * p_x_0 + p_1 * p_x_1

def compute_posterior(p_x_0, p_x_1, p_0, p_1):
    p_x = compute_marginal(p_x_0, p_x_1, p_0, p_1)
    p_0_x = p_x_0 * p_0 / p_x
    p_1_x = p_x_1 * p_1 / p_x
    return p_0_x, p_1_x

def query_marginals(lambda_pr_0, lambda_pr_1, p0, xq):
    p_x_0 = expon.pdf(xq, 0, 1. / lambda_pr_0)
    p_x_1 = expon.pdf(xq, 0, 1. / lambda_pr_1)
    return compute_marginal(p_x_0, p_x_1, p0, 1-p0)

def query_posteriors(lambda_pr_0, lambda_pr_1, p0, xq):
    p_x_0 = expon.pdf(xq, 0, 1. / lambda_pr_0)
    p_x_1 = expon.pdf(xq, 0, 1. / lambda_pr_1)
    p_0_x, p_1_x = compute_posterior(p_x_0, p_x_1, p0, (1 - p0))
    return p_0_x, p_1_x

x_correct = compute_xent(x_correct)
x_incorrect = compute_xent(x_incorrect)
x = np.append(x_correct, x_incorrect)

lambda_correct = estimate_lambda(x_correct)
lambda_incorrect = estimate_lambda(x_incorrect)

plt.figure()

plt.subplot(3,1,1)
n_correct ,_ ,_ = plt.hist(x_correct, bins=30, density=True)
n_correct.sort()
p_x_correct = expon.pdf(n_correct, 0, 1./lambda_correct)
plt.plot(n_correct, p_x_correct)
plt.xlim([0, 2.0])

plt.subplot(3,1,2)
n_incorrect ,_ , _ = plt.hist(x_incorrect, bins=30, density=True)
n_incorrect.sort()
p_x_incorrect = expon.pdf(n_incorrect, 0, 1./lambda_incorrect)
plt.plot(n_incorrect, p_x_incorrect)
plt.xlim([0, 2.0])

plt.subplot(3,1,3)
n_all ,_ , _ = plt.hist(x, bins=30, density=True)
n_all.sort()
p_x = query_marginals(lambda_correct, lambda_incorrect, acc, n_all)
plt.plot(n_all, p_x)
plt.xlim([0, 2.0])

plt.figure()
xq = np.linspace(0.0, 1.0, num=100)
p_correct_x, p_incorrect_x = query_posteriors( lambda_correct, lambda_incorrect, acc, xq)
plt.plot(xq, p_correct_x, 'g', xq, p_incorrect_x, 'r')

plt.show()

def get_loss(max_score, L, lambda_pr_0, lambda_pr_1, acc):
    x = max_score
    p_0_x, p_1_x = query_posteriors(lambda_pr_0, lambda_pr_1, acc, x)
    p = np.hstack([p_0_x, p_1_x])
    L = L.transpose()
    loss = np.matmul(p, L)
    return loss

cm = np.zeros(shape=(2,2))
L = np.array(
    [
        [0, 1],
        [1, 0]
    ]
)

loss_correct = get_loss(x_correct, L, lambda_correct, lambda_incorrect, acc)
loss_incorrect = get_loss(x_incorrect, L, lambda_correct, lambda_incorrect, acc)

cm[0,0] = np.sum(loss_correct[:,0]<loss_correct[:,1])
cm[0,1] = np.sum(loss_correct[:,0]>loss_correct[:,1])
cm[1,0] = np.sum(loss_incorrect[:,0]<loss_incorrect[:,1])
cm[1,1] = np.sum(loss_incorrect[:,0]>loss_incorrect[:,1])


print('Confusion Matrix')
print(cm)