AlphaGo (the 2016 version) and especially its successor AlphaGo Zero (2017) used a combination of deep neural networks and Monte Carlo Tree Search (MCTS), trained primarily through self-play reinforcement learning. The user’s description of a “recursive arena environment” where inferior builds are discarded, winning ones are kept, and they play against novel builds matches AlphaGo Zero almost exactly—it is a pure self-play system that iteratively improves itself without any human game data.
I’ll give a concise summary first, then dive into the detailed training pipelines for both versions (with references to the original papers), the software/methodologies, and finally how to broadly replicate this kind of self-play RL environment yourself.
Quick Summary

Original AlphaGo (2016): Started with supervised learning on ~30 million human expert moves to bootstrap a policy network, then used reinforcement learning (RL) via self-play to refine it. Separate policy and value networks guided an enhanced MCTS. It beat the European Go champion 5-0 but still relied on human knowledge.
AlphaGo Zero (2017): Pure RL from scratch (random weights, only the rules of Go). A single neural network (policy + value heads) is trained solely on games it generates by playing against itself. MCTS uses the network to guide search; the network is then updated to match the stronger MCTS-improved moves and the actual game outcome. An “arena/evaluator” continuously compares new network checkpoints against the current best player—if the new one wins ≥55% of evaluation games, it becomes the new best and all future self-play uses it (inferior checkpoints are discarded). This creates a recursive improvement loop that rapidly discovers superhuman strategies.

AlphaGo Zero trained for ~3 days (20-block network) or 40 days (40-block) on modest hardware (4 TPUs) and generated millions of self-play games. It beat the original AlphaGo 100-0.
Detailed Training of Original AlphaGo (2016)
Paper: “Mastering the game of Go with deep neural networks and tree search” (Nature, 2016).

Supervised Learning (SL) phase
Policy network (deep CNN) trained on human professional games (~30M positions).
Objective: predict the move the human actually played (cross-entropy loss).
This gave a strong initial move-selection prior.

Reinforcement Learning (RL) via self-play
The policy network plays games against itself (or slightly older versions).
Policy gradient (REINFORCE) updates the policy to maximize win rate: reward = +1 (win) or -1 (loss).
A separate value network is trained via temporal-difference learning to predict the expected outcome from any board position.

MCTS integration (during both training and play)
MCTS is guided by the policy network (priors for move selection) and value network (leaf evaluation, reducing expensive random rollouts).
Selection uses a variant of PUCT (Predictor + Upper Confidence bound for Trees).
This hybrid search is far stronger than pure MCTS or pure neural nets.


Result: AlphaGo reached superhuman level and defeated Fan Hui 5-0 in 2015.
Detailed Training of AlphaGo Zero (2017) — Matches Your Description Perfectly
Paper: “Mastering the game of Go without human knowledge” (Nature, 2017).
AlphaGo Zero is tabula rasa (blank slate) and uses a single iterative loop:

Initialize a deep residual CNN with random weights θ. It takes a raw 19×19 board (17 feature planes: stones, history, color-to-play) and outputs:
Policy head p: probability distribution over legal moves.
Value head v: scalar win probability for the current player.

Self-play game generation (the “recursive arena”)
The current best network plays against itself.
Every move is selected by running MCTS (1,600 simulations per move, ~0.4 s thinking time).
MCTS uses the network for:
Priors (policy head) + Dirichlet noise at the root for exploration.
Leaf evaluation (value head) — no random rollouts needed.

First 30 moves use temperature τ=1 (high exploration, sampling from visit counts); later τ→0 (greedy).
Game ends → outcome z = +1 or -1 (or draw, but rare).
Store training data: (board state s, MCTS-improved probabilities π, outcome z).

Network training
Sample mini-batches from the most recent self-play games.
Loss: (z − v)² (value) + −π log p (policy, cross-entropy) + L2 regularization.
Train with SGD + momentum and learning-rate annealing.
This makes the raw network better at predicting both the strong moves found by search and the true winner.

Arena / Evaluator (the “discard inferior builds” step)
After training a new checkpoint, it plays a 400-game tournament against the current best player (using MCTS, no temperature).
If the new network wins ≥55% of games, it becomes the new best player and all future self-play uses it.
Otherwise, discard it and keep training from the old best.
This ensures monotonic improvement and prevents regression.

Iteration
Repeat: self-play → train → evaluate → promote (or discard).
The system becomes its own teacher; each generation produces higher-quality data for the next.


Hardware (for the published runs): single machine with 4 TPUs for the 20-block (3-day) version; same setup scaled for the 40-day run. Self-play actors, learner, and evaluator ran asynchronously.
Key insight: MCTS acts as a powerful “policy improvement operator.” The raw network suggests moves; search finds even better ones. Training the network to match the search makes future searches even stronger — a virtuous cycle.
Software and Methodologies Involved

Neural network framework: TensorFlow (original DeepMind implementation). Later open-source clones use PyTorch or TensorFlow.
MCTS: Highly optimized, custom implementation (likely C++ for speed). No separate rollout policy in Zero — the neural net does everything.
Distributed system: Self-play actors (many parallel game generators), learner (trains on replay buffer), evaluator (arena tournaments). Data flows through a replay buffer of recent games.
Go rules engine: Custom, extremely fast board representation (bitboards, etc.).
Evaluation: Elo ratings from tournaments, plus direct head-to-head win rates.

AlphaGo Zero rediscovered classic Go concepts (e.g., ladders, ko, openings) purely from self-play and even invented new ones.
How to Broadly Replicate This Environment (Agent vs. Agent, Iterate)
You don’t need DeepMind’s compute budget to experiment — many open-source projects and tutorials exist for smaller games (Connect4, Othello, chess, etc.). The pattern is the same for any perfect-information two-player game:

Game environment: Write (or use) a fast simulator that can play legal moves, detect win/loss/draw, and provide board state as input (e.g., 2D array or tensor). Libraries: OpenSpiel, Gym, or custom Python/C++.
Neural network: A CNN (or ResNet) with two heads — policy (softmax over moves) + value (scalar). Frameworks: PyTorch or Keras/TensorFlow.
MCTS implementation:
Nodes store visit counts N, action values Q, priors P.
Selection: PUCT formula.
Expansion & backup using the network.
Output improved policy π from visit counts.

Self-play loop (the recursive arena):
Use current best network + MCTS to generate games (parallel actors for speed).
Store (s, π, z) tuples.
Train network on these examples.
Arena evaluation: New network plays N games (e.g., 400) vs. current best. If it wins enough, promote it; else discard.

Practical open-source starters:
Leela Zero — the most faithful open-source AlphaGo Zero clone for Go (C++). You can train your own networks from scratch (though full 19×19 superhuman level takes massive compute).
Minigo (TensorFlow) and other community forks.
Tutorials for smaller games (run on a single GPU in hours/days):
David Foster’s “How to build your own AlphaZero using Python and Keras” (Connect4) — complete GitHub repo with self-play, MCTS, training, and evaluator.
PyTorch Connect4/chess implementations (e.g., geochri/AlphaZero_Chess, plkmo/AlphaZero_Connect4).
OpenSpiel’s AlphaZero example (Google’s library, supports many games out of the box).



High-level pseudocode (the core loop):
textwhile True:
    # 1. Self-play with current best
    games = generate_self_play_games(best_network, num_games=25_000)
    replay_buffer.add(games)  # (s, π_MCTS, z)

    # 2. Train
    new_network = train_network(replay_buffer)

    # 3. Arena: compare
    win_rate = evaluate(new_network, best_network, num_games=400)
    if win_rate >= 0.55:
        best_network = new_network  # promote, discard old if desired
This exact pattern (MCTS-guided self-play + policy/value training + arena) is what made AlphaGo Zero revolutionary and is now standard in game-playing RL.
Papers & further reading (all freely available):

Original AlphaGo: https://www.nature.com/articles/nature16961
AlphaGo Zero: https://www.nature.com/articles/nature24270 (or the unformatted PDF: https://discovery.ucl.ac.uk/10045895/1/agz_unformatted_nature.pdf)
DeepMind blog on Zero: https://deepmind.google/blog/alphago-zero-starting-from-scratch