This article presents the work of Wiering and van Hasselt in "Ensemble Algorithms in Reinforcement Learning" [reference]. 
Ensemble methods merge multiple reinforcement learning (RL) algorithms into a single agent 
with the objectif of increasing the learning speed and the obtained reward. 
While ensemble methods have already been used in the context of reinforcement learning for representing 
and learning a single value function [references 14-16 in paper], 
Wiering and van Hasselt introduce a novel technique that combines the policy of each RL learning. 
The individual RL algorithms implemented were: Q-learning, Sarsa, Actor-Critic, QV-learning, and ACLA. 
The ensemble methods are majority voting, rank voting, Boltzmann multiplication, and Boltzmann addition. 
They implemented their algorithms for 5 mazes problems with increasing complexity to assess their performance. 
For all the mazes except the first one, the state space is very large, 
therefore a neural network was used for value functions approximation. 
We reimplemented their algorithms and obtained the same results for the first maze. 
For the other mazes, our neural network did not converge. 
Possible causes for this non-convergence are discussed in this article.

# Introduction

Reinforcement learning is a branch of machine learning
in which software agents learn from interacting with their environment.
It is a very general framework that can be used to learn tasks of a sequential decision making nature.
An environment can exists as different states,
and the actions available to the agent depend on the state of this environment.
After every action, the agent receives a reward which might be positive or negative.
Through iterative experience, the agent seeks a policy, 
an idea about which action needs to be performed for every possible state of the environment,
that maximizes the sum of rewards over time.

For simple tasks,
the agent can use a tabular expression to remember values associated with certain states or state-action combinations,
also called state(-action) functions.
For complex games however, there is an explosion of state-action possibilities.
Chess for example, is estimated to have more than $10^{50}$ chess-board configurations.
Not only do we lack the memory to store such a table,
we would need more time than the age of the universe to explore all possible states.
Therefore function approximators are used to approximate such state(-action) functions.
The capture the most essential concepts in order to maximize reward.
Neural networks are an example of such function approximator.
DeepMind's program AlphaZero is an interesting example that combines neural networks with reinforcement learning algorithms to learn chess.
The program was given no domain knowledge except the rules and achieved a superhuman level within 24 hours.
 
Some basic, well known online model-free value-function based reinforcement algorithms are SARSA and Q-learning.
They are both temporal difference (TD) reinforcement learning algorithm that learn by updating a Q-function (action value function).
The difference is that Q-learning is off-policy.
This means that the optimal action-value function is learned independent of the policy that is being followed,
unlike on-policy methods like SARSA, the learning of the action-value does depend on the policy.
The Actor-Critic (AC) is an temporal difference, on-policy learning algorithm.
But where SARSA and Q-learning only keep track of a single Q-function,
AC makes the distinction between a critic value function V that only depends on the state,
and an Actor function which will map for each action the states to preference values.
wiering(2007) explains a more recent and advanced on-policy QV-learning method. 
This algorithm can be seen as mix between Actor-Critic and Q-learning.
As Actor-Critc, it learn the state-value function V and an action-value function.
But unlike Actor-Critic, it learns the Q-function for that.
ACLA is another on-policy RL algorithm derived from Actor-Critic
that learns a state value-function V and Actor function P.
QV-learning and ACLA have been shown to outperform similar, more basic, RL algorithms (wiering2007) and QV-learning even scores higher in certain problem contexts than more recent RL methods (wiering2009).

Reinforcement learning methods, however useful, can take many steps to learn.
Ensemble methods are a powerful method to combine different Reinforcement Learning (RL) algorithms, 
which often result in improved learning speed and final performance.
[1] used ensemble methods to combine multiple reinforcement learning algorithms for multiple agents for which they used Temporal-Difference(TD) and  Residual-Gradient(RG) update methods as well as a policy function.
Other ensemble methods have been used in reinforcement learning to combine value functions stored by function approximators (wiering 2008 [14], [15], [16], [17]).
However, only Rl algorithms with the same value function can be combined in this way.
(Wiering2008) wanted to combine RL methods with different value functions and policies (e.g. Q-learning and ACLA).
It is possible however, 
to combine the different policies that were derived from distinct value functions.
Some algorithms that perform this task and take exploration into account at the same time are Majority voting, Rank voting, Boltzmann multiplication, and Boltzmann addition.
Majority Voting (VM) combines the best action of the RL algorithms and bases the final decision on the number of times that each action was preferred by the different RL methods.
Rank Voting (RV) lets each algorithm rank the different actions and combines these rankings into ﬁnal preferences over actions.
Boltzmann mulplication(BM) multiplies the Boltzmann probabilities
of each action computed by each RL algorithm.
Finally, Boltzmann Addition(BA) is very similar to Boltzmann mulplication, but adds instead of multiplies the Boltzmann probabilities of actions. 
 
In this article, 
we presents the work of Wiering and van Hasselt in "Ensemble Algorithms in Reinforcement Learning".
Five RL algorithms (Q-learning, SARSA, Actor-Critic, QV-learning, and ACLA) 
were compared to 4 ensemble methods (Majority Voting, Rank Voting, Boltzmann multiplication, and Boltzmann Addition).
To this end, they had to solve five mazes of varying complexity.
			
# References
			
	[1]  Stefan FauBer and Friedhelm Schwenker. Ensemble Methods for Reinforcement Learning. with Function Approximation
	[2]  Marco A. Wiering and Hado van Hasselt. The QV Family Compared to Other Reinforcement Learning Algorithms
	[3]  Stefan Fauber and Friedhelm Schwenker. Neural Network Ensembles in Reinforcement Learning
	[4]  Marco A. Wiering and Hado van Hasselt. Two Novel On-policy Reinforcement Learning Algorithms based on TD( λ )-methods

# Methods

## Reinforcement learning

With reinforcement learning methods,
agent are able to learn from interactions with their environment.
We assume a Markov Decision Process that is defined by the following parameters.
The state-space $ S =\{s_1, s_2, ... , s_n\}$ with $s_t$ denoting the state at moment t.
$A(s)$ is the set of action that are available to the agent if it is in state s,
$a_t$ is the action executes in state $s_t$ at time t.
The transition function $T(s,a,s')$ maps state-action pairs to a probability over successor states.
Finally, there is also the reward function $R(s,a,s')$ that return a reward for every state-action-state transition.
This reward function can give stochastic rewards.
The goal of an agent is to estimate the optimal policy $\pi^*(s)$.
With $\pi^*(s)$, the agent would know for each state
what the optimal action is to receive the highest possible cumulative discounted reward in future states.

<!---

wiering 2008

Reinforcement learning algorithms are able to let an agent
learn from the experiences generated by its interaction with
an environment. We assume an underlying Markov decision
process (MDP) which does not have to be known by the
agent. A finite MDP is defined as; (1) The state-space S =
{s 1 , s 2 , . . . , s n }, and s t ∈ S denotes the state of the system at
time t; (2) A set of actions available to the agent in each state
A(s), where a t ∈ A(s t ) denotes the action executed at time
t; (3) A transition function T (s, a, s ′ ) mapping state-action
pairs s, a to a probability distribution over successor states s ′ ;
(4) A reward function R(s, a, s ′ ) which denotes the average
reward obtained when the agent makes a transition from state
s to state s ′ using action a, where r t denotes the (possibly
stochastic) reward obtained at time t.

In optimal control or reinforcement learning (RL), we are
interested in computing or learning an optimal policy for
mapping states to actions. An optimal policy can be defined
as the policy that receives the highest possible cumulative
discounted rewards in its future from all states. In order to
learn an optimal policy, value-function-based RL [1] estimates
value-functions using past experiences of the agent. Q π (s, a)
is defined as the expected cumulative discounted future reward
if the agent is in state s, executes action a, and follows policy
π afterwards:

...

where 0 ≤ γ ≤ 1 is the discount factor that values later
rewards less compared to immediate rewards. Another possible
objective is to maximize the average reward intake. If the
optimal Q-function Q ∗ is known, the agent can select optimal
actions by selecting the action with the largest value in a state:
π ∗ (s) = arg max a Q ∗ (s, a).

In the experiments we will use five different online model-
free RL algorithms that optimize the discounted cumulative
future reward intake of an agent while it is interacting with
an (unknown) environment. Q-learning [3], [18] and Sarsa [4],
[5] will not be described here, since they are very well known
methods.
--->

### Q-learning

Q-learning is an off-policy, temporal difference (TD) reinforcement learning algorithm that learns by updating a Q-function.
This action-value function Q directly approximates the optimal action-value function $Q^*$ and it does this independent of the policy that is being followed. 
Q-learning updates with new experience $(s_t, a_t, r_t, s_{t+1})$ in the following way:

$$Q(s_t,a_T) := Q(s_t,a_t) + \alpha ( r_t + \gamma max_a Q(s_{t+1}, a) - Q(s_t,a_t) )$$

With $0 \leq \alpha \leq 1$ being the learning rate, 
and $0 \leq \gamma \leq 1$ being the discount factor.
Higher $\gamma$ values will result in the agent taking into account not only the immediate reward of an action, but also future rewards that will be available in future states as a consequence of this action.
The advantage of tabular Q-learning is that it will always converge to $Q^*$.
It does not matter what behavioral policy is used, 
as long as  each state-action pair is visited an infinite number of times (wiering 2007 [13]).
However, Q-learning combined with function approximators, such as neural networks, have been observed to diverge (wiering 2007).


### SARSA

Like Q-learning, 
SARSA is temporal difference (TD) reinforcement learning algorithm that learns the action-value Q-function (wiering 2007). 
Unlike Q-learning,
SARSA is on-policy,
meaning that the approximation of optimal $Q^*$ values depend on the policy being followed (wiering 2007 [6]).
An experience is defined as the quintuple $(s_t, a_t, r_t, s_{t+1}, a_{t+1})$.
This quintuple is what gave rise to the name SARSA (sutton 2018).
After every transition, Q-values are updated by the following method:

$$Q(s_t,a_T) := Q(s_t,a_t) + \alpha ( r_t + \gamma Q(s_{t+1}, a_{t+1}) - Q(s_t,a_t) )$$

As with tabular Q-learning, tabular SARSA converges towards $Q^*$ if all state-action pairs are visited an infinite number of times.


<!---

wiering 2007

Sarsa. Instead of Q-learning, we can also use the on-policy
algorithm Sarsa [6], [10] for learning Q-values. Sarsa makes
the following update after an experience (s t , a t , r t , s t+1 , a t+1 ):

Q(s t , a t ) := Q(s t , a t ) + α(r t + γQ(s t+1 , a t+1 ) − Q(s t , a t ))

Tabular Sarsa converges in the limit to the optimal policy under
proper learning rate annealing if the exploration policy is GLIE
(greedy in the limit with infinite exploration), which means
that the agent should always explore, but stop exploring after
an infinite number of steps [8].
--->

<!---

sutton 2018

We turn now to the use of TD prediction methods for the control problem. As usual, we
follow the pattern of generalized policy iteration (GPI), only this time using TD methods
for the evaluation or prediction part. As with Monte Carlo methods, we face the need to
trade o↵ exploration and exploitation, and again approaches fall into two main classes:
on-policy and o↵-policy. In this section we present an on-policy TD control method.
The first step is to learn an action-value function rather than a state-value function.
In particular, for an on-policy method we must estimate q ⇡ (s, a) for the current behavior
policy ⇡ and for all states s and actions a. This can be done using essentially the same TD
method described above for learning v ⇡ . Recall that an episode consists of an alternating
sequence of states and state–action pairs:

In the previous section we considered transitions from state to state and learned the
values of states. Now we consider transitions from state–action pair to state–action pair,
and learn the values of state–action pairs. Formally these cases are identical: they are
both Markov chains with a reward process. The theorems assuring the convergence of
state values under TD(0) also apply to the corresponding algorithm for action values:

This update is done after every transition from a nonterminal state S t . If
S t+1 is terminal, then Q(S t+1 , A t+1 ) is defined as zero. This rule uses every
element of the quintuple of events, (S t , A t , R t+1 , S t+1 , A t+1 ), that make up a
transition from one state–action pair to the next. This quintuple gives rise to
the name Sarsa for the algorithm. The backup diagram for Sarsa is as shown
Sarsa
to the right.
It is straightforward to design an on-policy control algorithm based on the Sarsa
prediction method. As in all on-policy methods, we continually estimate q ⇡ for the
behavior policy ⇡, and at the same time change ⇡ toward greediness with respect to q ⇡ .
The general form of the Sarsa control algorithm is given in the box on the next page.
The convergence properties of the Sarsa algorithm depend on the nature of the policy’s
dependence on Q. For example, one could use "-greedy or "-soft policies. Sarsa converges
with probability 1 to an optimal policy and action-value function as long as all state–action
pairs are visited an infinite number of times and the policy converges in the limit to
the greedy policy (which can be arranged, for example, with "-greedy policies by setting
" = 1/t).

--->

### Actor-Critic

The Actor-Critic (AC) is an temporal difference, on-policy learning algorithm.
Where SARSA and Q-learning only keep track on the Q-function,
Actor-Critic will update both a Critic and Actor function (wiering 2008 [1]).
The Critic function assigns values to the states, 
irrespective of the action chosen by the agent.
The Actor function will for each action map the states to preference values (wiering 2008).
An experience is defined as the sequence ($(s_t, a_t, r_t, s_{t+1})$).
After each experience,
the Critic and Actor get updated as follows [wiering 2008[11]]:

$$ \text{Critic: } V(s_t) := V(s_t) + \beta ( r_t + \gamma V(s_{t+1}) - V(s_t) ) $$

$$ \text{Actor: } P(s_t, a_t) := P(s_t, a_t) + \alpha ( r_t + \gamma V(s_{t+1}) - V(s_t) ) $$

Where $\beta$ is the learning rate of the Critic 
and $\alpha$ the learning rate of the Actor.
P-values should not be seen as literal Q-values, 
but instead as preference values.

<!---

wiering 2008 

Actor-Critic. The Actor-Critic (AC) method is an on-policy
algorithm like Sarsa. In contrast to Q-learning and Sarsa, AC
methods keep track of two functions; a Critic that evaluates
states and an Actor that maps states to a preference value
for each action [1]. After an experience (s t , a t , r t , s t+1 ) AC
makes a temporal difference (TD) update to the Critic’s value-
function V :

V (s t ) := V (s t ) + β(r t + γV (s t+1 ) − V (s t ))

where β is the learning rate. AC updates the Actor’s values
P (s t , a t ) as follows:

P (s t , a t ) := P (s t , a t ) + α(r t + γV (s t+1 ) − V (s t ))

where α is the learning rate for the Actor. The P-values should
be seen as preference values and not as exact Q-values.

--->

<!---

wiering 2007

Actor-Critic. Another on-policy algorithm is the Actor-
Critic (AC) method. In contrary to Q-learning and Sarsa, AC
methods keep track of two functions; a Critic that evaluates
states and an Actor that maps states to a preference value
for each action. A number of Actor-Critic methods have been
proposed [1], [4], [11]. Here we will use the Actor-Critic
method described in [11]. After an experience (s t , a t , r t , s t+1 )
AC makes a TD-update to the Critic’s value-function V :

V (s t ) := V (s t ) + β(r t + γV (s t+1 ) − V (s t ))

where β is the learning rate. AC updates the Actor with values
P (s t , a t ) as follows:

P (s t , a t ) := P (s t , a t ) + α(r t + γV (s t+1 ) − V (s t ))

where α is the learning rate for the Actor. The P-values
should be seen as preference values and not as exact Q-values.
Consider a bandit problem with one state and two actions.
Both actions lead to an immediate deterministic reward of 1.
When one action is selected a number of times in a row or
the initial learning rate is 1, the state or V-value and the P-
value for this action converge rapidly to 1. Afterwards the
P-value of the other action can never increase anymore using
AC and will not converge to the underlying Q-value of 1.
A number of Actor-Critic methods have still been proved to
converge to the optimal policy and state value-function for
tabular representations [4].

--->

### QV-learning

QV-learning (wiering 2008[6]) is very similar to Actor-Critic.
It is also a learning method that learns a state value-function V with TD method, 
and an Actor function to map the states for each action to preference values.
However, QV-learning learns actual Q-values as preference values (wiering 2008).
After each experience $(s_t, a_t, r_t, s_{t+1})$,
the V value-function is updates in the same way as in the Actor-Critic method (wiering 2007):

$$ V(s_t) := V(s_t) + \beta ( r_t + \gamma V(s_{t+1}) - V(s_t) )   $$

The update for the Q-function is similar to the Actor update,
but the $- V(s_t)$ at the end is replaced by $- Q(s_t, a_t)$:

$$ \text{Qvalue: } Q(s_t, a_t) := Q(s_t, a_t) + \alpha ( r_t + \gamma V(s_{t+1}) - Q(s_t, a_t))$$



<!---

wiering 2008

QV-learning. QV-learning [6] works by keeping track of
both the Q- and V-functions. In QV-learning the state value-
function V is learned with TD-methods [19]. This is similar
to Actor-Critic methods. The new idea is that the Q-values
simply learn from the V-values using the one-step Q-learning
algorithm. In contrast to AC these learned values can be seen
as actual Q-values and not as preference values. The updates
after an experience (s t , a t , r t , s t+1 ) of QV-learning are the use
of Equation 1 and:

Q(s t , a t ) := Q(s t , a t ) + α(r t + γV (s t+1 ) − Q(s t , a t ))

Note that the V-value used in this second update rule is learned methods have been used for combining function approximators
by QV-learning and not defined in terms of Q-values. There is to store the value function [14], [15], [16], [17], and this can
a strong resemblance with the Actor-Critic method; the only be an efficient way for improving an RL algorithm. In contrast
difference is the second learning rule where V (s t ) is replaced to previous research, we combine different RL algorithms that
by Q(s t , a t ) in QV-learning.

--->

<!---

wiering 2007


Abstract— This paper describes two novel on-policy reinforce-
ment learning algorithms, named QV(λ)-learning and the actor
critic learning automaton (ACLA). Both algorithms learn a state
value-function using TD(λ)-methods. The difference between the
algorithms is that QV-learning uses the learned value function
and a form of Q-learning to learn Q-values, whereas ACLA uses
the value function and a learning automaton-like update rule to
update the actor. We describe several possible advantages of these
methods compared to other value-function-based reinforcement
learning algorithms such as Q-learning, Sarsa, and conventional
Actor-Critic methods. Experiments are performed on (1) small,
(2) large, (3) partially observable, and (4) dynamic maze problems
with tabular and neural network value-function representations,
and on the mountain car problem. The overall results show
that the two novel algorithms can outperform previously known
reinforcement learning algorithms.

QV-learning. The updates after an experience
(s t , a t , r t , s t+1 ) of QV-learning are the following:

V (s t ) := V (s t ) + β(r t + γV (s t+1 ) − V (s t ))

Q(s t , a t ) := Q(s t , a t ) + α(r t + γV (s t+1 ) − Q(s t , a t ))

Note that the V-value used in this second update rule is learned
by QV-learning and not defined in terms of Q-values. There is
a strong resemblance with the Actor-Critic method; the only
difference is the second learning rule where V (s t ) is replaced
by Q(s t , a t ) in QV-learning.
--->



### ACLA (Actor-Critic Learning Automaton)

Actor-Critic Learning Automaton (ACLA)(wiering 2008[6]) is an on-policy learning algorithm that learns a state value-function V and Actor function P.
After each experience 

wiering 2008 $(s_t, a_t, r_t, s_{t+1})$,
the state value-function is updated in the same way as Actor-Critic or QV-learning (wiering 2007):

$$ \delta_t = r_t + \gamma V(s_{t+1}) - V(s_t) $$

$$ V(s_t) := V(s_t) + \beta ( \delta_t ) $$

The actor function maps states to preferences for actions
and is updated by an automaton-like updating rule (wiering 2008 [20])
The policy mapping update depends on the sign of $\delta$:

$\delta_t \geq 0$

$$ a = a_t: P(s_t, a_t) := P(s_t, a_t) + \alpha ( 1 - P(s_t, a_t)) $$

$$ \forall a \neq a_t:  P(s_T, a) := P(s_t, a) + \alpha ( 0 - P(s_t, a))$$


$\delta_t < 0$

$$ a = a_t: P(s_t, a_t) := P(s_t, a_t) + \alpha ( 0 - P(s_t, a_t)) $$

$$ \forall a \neq a_t:  P(s_t, a) := P(s_t, a) + \alpha \left( \frac{P(s_t, a)}{\sum_{b \neq a_t}P(s_t, b)} - P(s_t, a) \right)$$

There are also additional rules to ensure that the target values are between 0 and 1 and existing.
If $P(s_t,a)$ is greater than 1, the value gets changed to 1.
If $P(s_t,a)$ is smaller than 0, the value gets changed to zero.
If the denominator is 0, the new value equals $\frac{1}{|A| -1}$,
with $|A|$ being the number of actions (wiering 2008).

<!---

wiering 2007


Abstract— This paper describes two novel on-policy reinforce-
ment learning algorithms, named QV(λ)-learning and the actor
critic learning automaton (ACLA). Both algorithms learn a state
value-function using TD(λ)-methods. The difference between the
algorithms is that QV-learning uses the learned value function
and a form of Q-learning to learn Q-values, whereas ACLA uses
the value function and a learning automaton-like update rule to
update the actor. We describe several possible advantages of these
methods compared to other value-function-based reinforcement
learning algorithms such as Q-learning, Sarsa, and conventional
Actor-Critic methods. Experiments are performed on (1) small,
(2) large, (3) partially observable, and (4) dynamic maze problems
with tabular and neural network value-function representations,
and on the mountain car problem. The overall results show
that the two novel algorithms can outperform previously known
reinforcement learning algorithms.

Actor Critic Learning Automaton. ACLA learns a state
value-function in the same way as QV-learning, but ACLA
uses a learning automaton-like update rule [5] for changing
the policy mapping states to probabilities (or preferences) for
actions. The updates after an experience (s t , a t , r t , s t+1 ) of
ACLA are the following:

V (s t ) := V (s t ) + β(r t + γV (s t+1 ) − V (s t ))

and, now we use an update rule that examines whether the last
performed action was good (in which case the state-value was
increased) or not. We do this with the following update rule:

if ...
else ...

After which we add ΔP (s t , a) to P (s t , a). For ACLA we used
some additional rules to ensure the targets are always between
0 and 1, independent of the initialization. This is done by using
1 if the target is larger than 1, and 0 if the target is smaller
than 0. If the denominator ≤ 0, all targets in the last part of
1
where |A| is the number of
the update rule get the value |A|−1
actions. The update in case of δ t < 0 is chosen to increase the
preference of actions which are good more than actions that
are considered worse. Above is the ACLA− algorithm, we
also extended ACLA− to ACLA+ which can make multiple
updates relying on the size of δ t = γV (s t+1 ) + r t − V (s t ).

--->

<!---

wiering 2008

ACLA. The Actor Critic Learning Automaton (ACLA) [6]
learns a state value-function in the same way as AC and QV-
learning, but ACLA uses a learning automaton-like update rule
[20] for changing the policy mapping states to probabilities
(or preferences) for actions. The updates after an experience
(s t , a t , r t , s t+1 ) of ACLA are the use of Equation 1, and
now we use an update rule that examines whether the last
performed action was good (in which case the state-value was
increased) or not. We do this with the following update rule:

If δ t ≥ 0
∆P (s t , a t ) = α(1 − P (s t , a t )) and
∀a 6 = a t ∆P (s t , a) = α(0 − P (s t , a))

Else
∆P (s t , a t ) = α(0 − P (s t , a t )) and
...

where δ t = γV (s t+1 ) + r t − V (s t ), and ∆P (s, a) is added to
P (s, a). ACLA uses some additional rules to ensure the targets
are always between 0 and 1, independent of the initialization
(e.g. of neural network weights). This is done by using 1 if
the target is larger than 1, and 0 if the target is smaller than
0. If the denominator is less than or equal to 0, all targets
1
in the last part of the update rule get the value |A|−1
where
|A| is the number of actions. ACLA was shown to outperform
Q-learning and Sarsa on a number of problems when ǫ-greedy
exploration was used [6].

--->

## Ensemble algorithms in RL

Combining single classifiers for which the errors are not strongly correlated can lead to a higher accuracy than what is available for a single classifier.
With this in mind, 
ensemble methods have been used in reinforcement learning to combine value functions stored by function approximators (wiering 2008 [14], [15], [16], [17]).
However, only Rl algorithms with the same value function can be combined in this way.
In our case, want to combine RL methods with different value function and policies (e.g. Q-learning and ACLA).
It is possible however, 
to combine the different policies that were derived from distinct value functions.
Next, we will describe four ensemble methods, designed by (Wiering 2008), that combine  policies and also take into account exploration. 


### Majority voting

Each of the n RL algorithms defines what it thinks to be the best action.
Majority voting will transform these best actions into preferences in the following way:

$$ p_t(s_t, a[i]) = \sum_{j=1}^{n} I(a[i],a_t^j) $$

with $a_t^j$ being the best action according to algorithm j at time t and

$$ x=y: I(x,y) = 1 $$

$$ x \neq y: I(x,y) = 0 $$

The following Boltzmann distribution based ensemble policy is used for actions selection:

$$ \pi_t (s_t, a[i]) = \frac{exp[\frac{p_t(s_t, a[i])}{\tau}]}{\sum_k exp[\frac{p_t(s_t, a[k])}{\tau}]} $$

This policy makes sure that the most probable action is the best action according to most algorithms, but also ensures exploration (wiering 2008).


<!---

wiering 2008

Majority Voting. The preference values calculated by the
majority voting ensemble using n different RL algorithms are

p t (s t , a[i]) =
n
X
I(a[i], a jt )

where I(x, y) is the indicator function that outputs 1 when
x = y and 0 otherwise. The most probable action is simply
the action that is most often the best action according to
the algorithms. This method resembles a bagging ensemble
method for combining classifiers with majority voting, with
the big difference that because of exploration we do not always
select the action which is preferred by most algorithms.

--->

### Rank voting

Preference values of the ensemble are give by:

$$ p_t(s_t, a[i]) = \sum_{j=1}^{n} r_t^j(a[i]) $$

If m actions are possible in state $s_t$,
$r_t^j(a[1])$, $r_t^j(a[2])$, ... , $r_t^j(a[m])$ 
denotes the weights for these actions as determined by RL algorithm j.
The most probable action is weighted m times, the second best m-1 times, and so on...
(wiering 2008).
As with majority voting, 
the rank voting algorithm uses the following Boltzmann distribution based ensemble policy to ensure both exploitation and exploration:

$$ \pi_t (s_t, a[i]) = \frac{exp[\frac{p_t(s_t, a[i])}{\tau}]}{\sum_k exp[\frac{p_t(s_t, a[k])}{\tau}]} $$

<!---

wiering 2008

Rank Voting. Let r t j (a[1]), . . . , r t j (a[m]) denote the weights
according to the ranks of the action selection probabilities,
such that if π t j (a[i]) ≥ π t j (a[k]) then r t j (a[i]) ≥ r t j (a[k]). For
example, the most probable action could be weighted m times,
the second most probable m − 1 times and so on. This is the
weighting we used in our experiments. The preference values
of the ensemble are:

...

--->

### Boltzmann multiplication

Boltzmann multiplication calculates the ensemble preferences by multiplying for each action the action-selection probabilities given by the RL algorithms:

$$ p_t(s_t, a[i]) = \prod_j \pi_t^j (s_t, a[i]) $$

$\pi_t^j(s_t, a[i])$ is the policy for algorithm j at time t for state $s_t$ and action $a[i]$.
Since all the RL algorithms use Boltzmann exploration, 
preference values are never zero.
This is important since if only one RL algorithm return zero,
Boltzmann multiplication would result for a zero probability for that action,
irrespectively of that the other algorithms return high or low probabilities.
The ensemble policy for actions selection is calculated in the following way:

$$ \pi_t (s_t, a[i]) = \frac{ p_t(s_t, a[i])^{\frac{1}{\tau}}}{\sum_k p_t(s_t, a[k])^{\frac{ 1 }{\tau}}} $$

<!---

wiering 2008

Boltzmann Multiplication. Another possibility is multiply-
ing all the action selection probabilities for each action based
on the policies of the algorithms. The preference values of the
ensemble are:

...

A potential problem with this method is that one algorithm
can set the preference values of any number of actions to zero
when it has a zero probability of choosing those actions. Since
all our algorithms use Boltzmann exploration, this was not an
issue in our experiments.

--->

### Boltzmann addition

The formula  of Boltzmann addition looks very similar to Boltzmann multiplication,
with the product being replaced by a sum:

$$ p_t(s_t, a[i]) = \sum_j \pi_t^j (s_t, a[i]) $$

As concept however,
it is a variant of rank voting where $ r_t^j=\pi_t^j $.
The ensemble policy for actions selection is calculated in the same way as Boltzmann multiplication:

$$ \pi_t (s_t, a[i]) = \frac{ p_t(s_t, a[i])^{\frac{1}{\tau}}}{\sum_k p_t(s_t, a[k])^{\frac{ 1 }{\tau}}} $$

<!---

Boltzmann Addition. As a last method, we can also sum
the action selection probabilities of the different algorithms.
Essentially, this is a variant of rank voting, using r t j = π t j .
The preference values of the ensemble are:

...

--->

## Experiments

We compared five different RL algorithms (Q-learning, SARSA, Actor-Critic, QV-learning, ACLA) with each other and with four ensemble methods (Majority Voting, Rank Voting, Boltzmann Multiplication, Boltzmann Addition).
The goal for the agents was to solve five different maze tasks of varying complexity,
In each maze, the agent starts at a certain starting position and needs to reach another goal position.
The dominating objective was to move with each step closer to the goal.
For the first experiment,
the agents learned to solve a small base where start, goal and walls were in static position. 
To do this, they combined RL algorithms with a tabular expression.
For the second to fifth maze,
complexity was increased by adding different dynamic elements to the maze.
To circumvent the combination explosion that would occur in a tabular expression,
neural networks were used as function approximators.
In each tile of the maze, the agent can initiate 4 actions: going North, East, South or West.
These actions are noisy,
meaning that every time an action is taken, there is a 20% chance that the agent performs a random action instead.
For each maze, the rewards were given in the following way.
If the agent moves into the goal tile, 
it receives a reward of 100.
When it tries to move into a wall or border,
it will receive a reward of -2 and remain in the same place (state is not changed).
For every other move (moving from one tile to the next),
the agent receives a reward of -0.1.
Even though it does not collide with a wall or border, 
it gets a negative score to discourage it from wandering around.
An agent learns in different trials.
Such trial starts with the agent in the starting position 
and ends when it reaches the goal positions 
or has wandered for 1000 consecutive action without reaching the goal.


<!---

wiering 2008

We performed experiments with five different maze tasks
(one simple and four more complex problems) to compare the
different ensemble methods to the individual algorithms. In
the first experiment, the RL algorithms are combined with
tabular representations and are compared on a small maze
task. In the second experiment a partially observable maze
is used and neural networks as function approximators. In the
third experiment a dynamic maze is used where the obstacles
are not placed at fixed positions and neural network function
approximators are used. In the fourth experiment a dynamic
maze is used where the goal is not placed at a fixed position
and neural networks are used as function approximators. In
the fifth and final experiment a generalized maze [23] task
is used where the goal and the obstacles are not placed at
fixed positions and again neural networks are used as function
approximators.

--->


### Small Maze experiment

The first experiment was the least complex,
so that the agent could use tabular expression for the different state-action pairs.
We implemented Sutton's Dyna maze,
which consist of 54 tiles (6 rows and 9 columns).
The maze also includes 7 walls, a starting and goal, all in fixed position (Fig. \ref{simpleMaze}).

![Sutton's Dyna maze \label{simpleMaze}](img/simpleMaze.png)
 
In order to compare our results with those of (wiering 2008),
we used the same learning rates, discount factors and greediness (inverse of Boltzmann temperature) parameters.
In their paper, they explain how they tested a wide range of parameters 
to optimize each of the five RL algorithms final performance (by evaluating the average reward).
They wanted to compare the best version of each algorithm,
which was not possible if the same parameters were used.
For the ensemble methods, they used the same parameters as were determined for the single RL algorithms.
(wiering 2008) observed the discount factor to have a major impact on the final and cumulative score.
For the SARSA method, discount factors 0.90 and 0.95,
and for the ACLA method, discount factors 0.99 and 0.90
were compared to each other.
We wanted to confirm these findings, 
so we did simulations with the same discount factors.
    
<!---

wiering 2008

The different ensemble methods: majority voting, rank
voting, Boltzmann addition, and Boltzmann multiplication, are
compared to the 5 individual algorithms: Q-learning, Sarsa,
AC, QV-learning, and ACLA. We performed experiments with
Sutton’s Dyna maze shown in Figure 1(A). This simple maze
consists of 9 × 6 states and there are 4 actions; north, east,
south, and west. The goal is to arrive at the goal state G as
soon as possible starting from the starting state S under the
influence of stochastic (noisy) actions. We kept the maze small,
since we want to compare the results with the experiments on
the more complex maze tasks, which would otherwise cost too
much computational time.

The reward for arriving at the goal
is 100. When the agent bumps against a wall or border of
the environment it stays still and receives a reward of -2.
For other steps the agent receives a reward of -0.1. A trial
is finished after the agent hits the goal or 1000 actions have
been performed. The random replacement (noise) in action
execution is 20%. This reward function and noise is used in
all experiments of this paper.

We used a tabular representation and first performed simu-
lations to find the best learning rates, discount factors, and
greediness (inverse of the temperature) used in Boltzmann
exploration. All parameters were optimized for the single RL
algorithms, where they were evaluated using the average re-
ward intake and the final performance is optimized. Although
in general it can cause problems to learn to optimize the
discounted reward intake while evaluating with the average
reward intake, for the studied problems the dominating ob-
jective is to move each step closer to the goal, which is
optimized using both criteria if the discount factor is large
enough. We also optimize the discount factors, since we found
that they had a large influence on the results. If we would
have always used the same discount factor for all algorithms,
the results of some algorithms would have been much worse,
and therefore it would be impossible to select a fair discount
factor. Since we evaluate all methods using the average reward
criterion, the different discount factors do not influence the
comparison between algorithms. The ensemble methods used
the parameters of the individually optimized algorithms, so
that only the ensemble’s temperature had to be set.

--->

### Neural networks as universal function approximators

Traditionally RL algorithms use tabular expression to represent a state-function or action-function.
In Q-learning for example,
a Q-value is remembered for each state-action combination.
Each time the agent performs an action, gains experience, 
the Q-value of that specific state-action pair is updated.
For complex games however, there is an explosion of state-action possibilities.
Therefore function approximators are used to approximate such state(-action) functions,
which try to capture the essence, most essential concepts in order to maximize reward.
Neural networks are universal function approximators, 
this mean that a neural network with a single hidden layer 
containing a finite number of neurons can approximate 
any mathematical function to any desired accuracy.
For the more complex mazes of experiments 2 to 5,
we implemented a neural network that was trained after each move of the agent.
Weights were updated after each move using gradient descent for one iteration. 
This was done by performing one forward and one backward propagation pass.

<!---

https://www.freecodecamp.org/news/an-introduction-to-q-learning-reinforcement-learning-14ac0b4493cc/

http://www.stokastik.in/neural-networks-function-approximator/

https://www.practicalai.io/teaching-a-neural-network-to-play-a-game-with-q-learning/

--->

### Partially observable maze

For the partially observable maze experiment,
we started from the same Sutton's Dyna maze.
However in this case, the starting position varies and is unknown to the agent.
Additionally, the agent can only observe part of the maze.
After each action,
it receives an observation,
a tuple of four values (representing the tiles North, South, East and West of the agent).
for example, if there is a wall to the North, a border to the East and empty tiles in the other directions,
the observation tuple looks like (1,0,1,0).
In addition to the 20 % noise of action selection,
there is also a 10 % observational noise for each independent tile. 
Because the position is unknown to the agent,
Markov localization is used to keep track of a believe state.
Initially this believe state has a uniform distribution over all the tiles without obstacle.
Updates are performed as following:

$$ b_{t+1}(s) = \eta P(o_{t+1}|s) \sum_{s'}T(s',a_t,s) b_t(s') $$

$a_t:$ action at time t

$b_t(s):$ believe state

$o_{t+1}:$ observation

$\eta:$ normalization factor

$T(s',a_t,s):$ transition function that maps the state-action pairs to a probability function over successor states.

Since there are to many states for tabular expression,
a neural network with 20 sigmoidal hidden neurons was used as function approximator.
As input, the network received the believe state as input, a tuple of length 54.

<!---

wiering 2008

In this experiment we use Markov localization and neural
networks to solve a partially observable Markov decision
process in the case where the model of the environment is
known. We use Markov localization to track the belief state (or
probability distribution over the states) of the agent given an
action and observation after each time-step. This belief state is
then the input for the neural network. We used 20 sigmoidal
hidden neurons in our experiments, and the maze shown in
Figure 1(A) with the goal indicated by P and each state can be
a starting state. The initial belief state is a uniform distribution
where only states that are not obstacles get assigned a non-zero
belief. After each action a t the belief state b t (s) is updated
with the observation o t+1 :

...

where η is some normalization factor. The observations are
whether there is a wall to the north, east, south, and west.
Thus, there are 16 possible observations. We use 20% noise
in the action execution and 10% noise for observing each
independent wall (or empty cell) at the sides. That means that
an observation is correct with probability 0.9 4 = 66%. Note
that we use a model of the environment to be able to compute
the belief state, and the model is based on the uncertainties in
the transition and observation functions.

We performed experiments consisting of 100,000 learning
steps with a neural network representation and the Boltzmann
exploration rule. For evaluation after each 5,000 steps we
measured the average reward intake during that period. Table
II shows that the Boltzmann multiplication ensemble method
learns fastest in this problem. We also experimented with a
Boltzmann multiplication ensemble consisting of five differ-
ently initialized Q-learning algorithms. The performance of
this ensemble was 9.61 ± 0.31 for the final performance and
153.1 ± 8.0 for the total learning performance. This shows
that combining different RL algorithms speeds up learning
performance compared to an ensemble of the best single RL
algorithm. All algorithms converge to a stable performance
within 60,000 learning steps, but the best ensembles reach a
good performance much earlier.i

--->

### Maze with dynamic obstacles

For third experiment,
4 to 8 obstacles (walls) were generated at random locations at the start of each trial.
Start and goal positions were fixed in the same place as Sutton's Dyna maze.
If no possible path exists from start to goal,
the agent would not have to solve it and an new maze was generated instead.
The agent needed to learn the knowledge of a path planner.
For this a neural network was implemented with 60 sigmoidal hidden units.
As input, the network received a tuple of length 108 (since there are 54 tiles in the maze and we want to know from each tile whether an agent or wall is on it).
54 of them depict the agent position (0 or 1 for each tile),
and 54 depict the wall positions (0 or 1 for each tile).

<!---

wiering 2008

We also compared the algorithms on a dynamic maze, where
in each trial there are several obstacles at random locations (see
Fig. 1(b)). In order to deal with this task the agent uses a neural
network that receives as inputs whether a particular state-cell
contains an obstacle (1) or not (0). The neural network uses
2 × 54 = 108 inputs including the position of the agent and
60 sigmoidal hidden units. At the start of each new trial there
are between 4 and 8 obstacles generated at random positions
and it is made sure that a path to the goal exists from the
fixed starting location S. Since there are many instances of
this maze, the neural network has to learn the knowledge of a
path planner. A simulation lasts for 3,000,000 learning steps
and we measure performance after each 150,000 steps.
Table III shows the final and total performance of the
different algorithms. The Boltzmann multiplication ensemble
outperforms the other algorithms on this problem: it reaches
the best final performance and also has the best overall
learning performance. We also experimented with a Boltzmann
multiplication ensemble consisting of five differently initial-
ized Q-learning algorithms. The performance of this ensemble
was 6.87 ± 0.22 for the final performance and 117.0 ± 2.7
for the total learning performance. This shows again that
combining different RL algorithms in an ensemble performs
better than an ensemble consisting of the best single RL
algorithm. The best ensembles reach a better performance at
the end than the single RL algorithms.

--->

### Maze dynamic goal positions

The fourth maze is very similar to the third maze.
Instead of dynamic obstacles, 
there is a dynamic goal position.
Obstacles and starting position are placed as in Sutton's Dyna maze.
This time, a neural network with 20 sigmoidal hidden units and a tuple of length 108 as input was used as function approximator.
This time 54 values represent the agent position,
and the other 54 values the goal position. 

<!---

wiering 2008

In this fourth maze experiment, we use the same small
maze as before (see Figure 1(A)) where the starting position
is indicated by S, but now the goal is placed at a different
location in each trial. To deal with this, we use a neural
network function approximator that receives the position of
the goal as input. Therefore there are 54 × 2 inputs, that
indicate the position of the agent and the position of the goal.
A simulation lasts for 3,000,000 learning steps and we measure
performance after each 150,000 steps. We used feedforward
neural networks with 20 sigmoidal hidden units.
best final performance and also has the best overall learning
performance. We also experimented with a majority voting
ensemble consisting of five differently initialized Sarsa algo-
rithms. The performance of this ensemble was 11.02 ± 0.22
for the final performance and 176.7 ± 4.9 for the total learning
performance. This shows again that a combination of different
RL algorithms in an ensemble learns faster than an ensemble
consisting of the best single RL algorithm, although an en-
semble of the same RL algorithm can also increase the final
performance of that algorithm. The best ensembles reach a
better performance at the end than the single RL algorithms
and initially have a faster learning speed.

--->

### Generalized maze

The last experiment combined the problem of a maze with dynamic obstacles and a maze with dynamic goals positions into a generalized maze experiment (wierling 2008 [23]).
In this maze,
the goal and obstacles are positioned at random positions at the start each trial.
A neural network with 100 sigmoidal hidden units receives 162 (54x3) input values,
54 to describe the agent position,
54 to describe the obstacle positions,
and 54 to describe the goal position.


<!---

wiering 2008

In this last maze experiment, we use the same small
maze as before, but now the goal and walls are placed at
a different location in each trial. This is what Werbos calls
the “Generalized Maze” [23] experiment. To deal with this, a
neural network function approximator receives the position of
the agent, goal and the dynamic walls as input. Therefore there
are 54 × 3 inputs. A simulation lasts for 15,000,000 learning
steps and we measure performance after each 750,000 steps.
The feedforward neural networks have 100 sigmoidal hidden
units.
Table V shows the final and total performance of the differ-
ent algorithms. Here Q-learning obtains the best final results,
but the majority voting ensemble has the best overall learning
performance. It is surprising that Sarsa obtains much worse
results than the other algorithms, even though we optimized all
its learning parameters. We also experimented with a majority
voting ensemble consisting of five Q-learning algorithms. The
performance of this ensemble was 7.20 ± 0.16 for the final
performance and 103.4±0.9 for the total learning performance,
so this ensemble reaches the best final performance, and its
learning speed is almost significantly better than the majority
voting ensemble using different RL algorithms. This is the
only experiment where an ensemble consisting of the same
best single RL algorithm leads to a significantly better final
performance compared to the best ensemble consisting of
different single RL algorithms. This results can be explained
by the fact that in this problem Q-learning performs much
better than the other algorithms. At the end of the learning
trial Q-learning outperforms the best ensembles, although the
ensembles initially have a faster learning speed.
--->
CGT project results

# Results

## Simple Maze

The evaluation was done by noting the Final Reward intake during the last 2500 learning-steps of each simulation. Also the cumulative average reward was calculated after every 2500 learning-steps. Each simulation has 50,000 learning-steps. Table 1 shows the average results and the standard deviation of 500 such simulations.
<br>

| Method          | $\alpha$ | $\beta$ | $\gamma$ | G   | Final          | Cumulative     |
|-----------------|----------|---------|----------|-----|----------------|----------------|
| Q               | 0.2      |    -    | 0.9      | 1   | 5.20 +/- 0.19  | 89.66 +/- 4.82 |
| SARSA           | 0.2      |    -    | 0.9      | 1   | 5.20 +/- 0.18  | 91.08 +/- 4.16 |
| AC              | 0.1      |   0.2   | 0.95     | 1   | 5.21 +/- 0.20  | 95.12 +/- 5.96 |
| QV              | 0.2      |   0.2   | 0.9      | 1   | 5.21 +/- 0.18  | 92.24 +/- 4.08 |
| ACLA            | 0.005    |   0.1   | 0.99     | 9   | 5.18 +/- 0.14  | 85.32 +/- 3.59 |
| Majority Voting |     -    |    -    |     -    | 1.6 | 5.19 +/- 0.19  | 94.46 +/- 3.63 |
| Rank Voting     |     -    |    -    |     -    | 0.6 | 4.89 +/- 0.29  | 88.80 +/- 6.74 |
| Boltzmann Mult. |     -    |    -    |     -    | 0.2 | 5.23 +/- 0.15  | 94.00 +/- 2.99 |
| Boltzmann Add.  |     -    |    -    |     -    | 1   | 5.04 +/- 0.32  | 93.18 +/- 6.97 |

<br>

\begin{table}[]
\begin{tabular}{|l|l|c|l|l|l|l|}
\hline
\multicolumn{1}{|r|}{\textbf{Method}} & $\alpha$               & \multicolumn{1}{l|}{$\beta$} & $\gamma$               & G   & Final         & \textbf{Cumulative} \\ \hline
Q                                     & 0.2                    & -                            & 0.9                    & 1   & 5.20 +/- 0.19 & 89.66 +/- 4.82      \\ \hline
SARSA                                 & 0.2                    & -                            & 0.9                    & 1   & 5.20 +/- 0.18 & 91.08 +/- 4.16      \\ \hline
AC                                    & 0.1                    & 0.2                          & 0.95                   & 1   & 5.21 +/- 0.20 & 95.12 +/- 5.96      \\ \hline
QV                                    & 0.2                    & 0.2                          & 0.9                    & 1   & 5.21 +/- 0.18 & 92.24 +/- 4.08      \\ \hline
ACLA                                  & 0.005                  & 0.1                          & 0.99                   & 9   & 5.18 +/- 0.14 & 85.32 +/- 3.59      \\ \hline
Majority Voting                       & \multicolumn{1}{c|}{-} & -                            & \multicolumn{1}{c|}{-} & 1.6 & 5.19 +/- 0.19 & 94.46 +/- 3.63      \\ \hline
Rank Voting                           & \multicolumn{1}{c|}{-} & -                            & \multicolumn{1}{c|}{-} & 0.6 & 4.89 +/- 0.29 & 88.80 +/- 6.74      \\ \hline
Boltzmann Mult.                       & \multicolumn{1}{c|}{-} & -                            & \multicolumn{1}{c|}{-} & 0.2 & 5.23 +/- 0.15 & 94.00 +/- 2.99      \\ \hline
Boltzmann Add.                        & \multicolumn{1}{c|}{-} & -                            & \multicolumn{1}{c|}{-} & 1   & 5.04 +/- 0.32 & 93.18 +/- 6.97      \\ \hline
\end{tabular}
\end{table}


<br>
It was observed that Majority voting and Boltzmann Multiplication have the best Final as well as the Cumulative reward intakes. In the current experiment, Boltzmann addition has the worst performance. 

In order to examine the effect of the discount factor ($\gamma$) , the SARSA and the ACLA algorithms are rerun with different discount factors. The results are shown in table 2.
<br>

| Method | $\alpha$ | $\beta$ | $\gamma$ | G | Final         | Cumulative      |
|--------|----------|---------|----------|---|---------------|-----------------|
| SARSA  | 0.2      | -       | 0.95     | 1 | 4.96 +/- 0.90 | 87.04 +/- 17.08 |
| ACLA   | 0.005    | 0.1     | 0.9      | 9 | 4.27 +/- 1.8  | 60.87 +/- 29.48 |

<br>

\begin{table}[]
\begin{tabular}{|l|l|l|l|l|l|l|}
\hline
Method & $\alpha$ & $\beta$ & $\gamma$ & G & Final         & Cumulative      \\ \hline
SARSA  & 0.2      & -       & 0.95     & 1 & 4.96 +/- 0.90 & 87.04 +/- 17.08 \\ \hline
ACLA   & 0.005    & 0.1     & 0.9      & 9 & 4.27 +/- 1.8  & 60.87 +/- 29.48 \\ \hline
\end{tabular}
\end{table}

<br>
There is a significant drop in the performance of both algorithms as compared to the previous simulations. 

Figure 1 and 2 plots the total reward obtained by the algorithms vs the timestep. For the sake of clarity results are plotted till 15,000 timesteps. It can be observed that all algorithms converge to a stable performance well within 15,000.
![Figure_1](img/Timestep_vs_Total_reward_simple.png)
![Figure_2](img/Timestep_vs_Total_reward_zoomed_simple.png)

<br>

## Maze with dynamic obstacles

Figure 3 plots the total reward over time steps for a Maze with Dynamic obstacles. None of the algorithms successfully converge to stable values. Consequently the final and the cumulative rewards are negative, which is far below that of simple maze.

![Figure_3](img/Timestep_vs_Total_reward.png)



# Discussion

Although the article of (wiering 2008) is very interesting and shows new insights,
we are of the opinion that they could have taken extra steps to assure reproducibility.
Some methods were ambiguously explained, so that it took some effort to figure out what was meant exactly.
The source was also not available, which would have solved previous remark.
For example,
while implementing the neural network,
it is not clear how the weights are updates.
We decided to update the weights after each move gradient descent for one iteration.
However, it is possible that in the original paper,
they used multiple gradient descent iterations after each move.
Or maybe, action replay as in, "Human-level control through deep reinforcement learning",
from DeepMind where used. 
Here, actions, states and rewards are stored in memory and every so often, the weights are updated by learning from the experiences stored in memory.
This could be one of the reason why our neural networks were not able to converge for the dynamic maze and other more complex maze experiments,
while in the original paper, they did.
Other possible explanation are numerical errors. 

For the small maze experiment,
we observed very similar results to those in the paper.
All final and cumulative values were within the standard deviation.

(Wiering 2008) determined all learning parameters by performing various trials with different parameter values.
They noted in their paper that the discount factor had a major effect on the performance.
To assess this effect,
the SARSA and the ACLA algorithms were trained on the simple maze with changed discount.
We observe a significant change in the final and the cumulative reward,
which highlights the importance of this parameter in the overall performance of the algorithms. 