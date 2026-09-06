"""SmartCampus AI - Knowledge Base Module
Local Python-based knowledge base storing core concepts in Artificial Intelligence,
search algorithms, adversarial reasoning, expert systems, and student curriculum topics.
No external API calls or cloud dependencies.
"""

from typing import Dict, List, Any, Optional

KNOWLEDGE_TOPICS: Dict[str, Dict[str, Any]] = {
    "Artificial Intelligence": {
        "name": "Artificial Intelligence",
        "category": "Core Foundations",
        "difficulty": "Fundamental",
        "icon": "🤖",
        "definition": "The branch of computer science dedicated to building hardware and software systems capable of performing tasks that typically require human intelligence, such as visual perception, decision-making, natural speech processing, and adaptive reasoning.",
        "concepts": [
            "Turing Test & Rational Agent Approach",
            "Symbolic/Rule-Based AI vs. Statistical Machine Learning",
            "Autonomous Decision Making & Problem Formulation",
            "Perception, Actuation, and Dynamic Environment Feedback Loops"
        ],
        "applications": [
            "Autonomous Vehicles & Robotics Navigation",
            "Computer Vision & Diagnostic Medical Imaging",
            "Natural Language Processing & Intelligent Assistants",
            "Recommendation Engines (E-Commerce, Streaming Services)"
        ],
        "example": "A chess engine evaluating 20 moves ahead or an autonomous vacuum cleaner mapping and navigating a floorplan using infrared sensors.",
        "complexity": "Varies by paradigm (from deterministic O(1) state transitions to multi-billion parameter neural representations)."
    },
    "Intelligent Agents": {
        "name": "Intelligent Agents",
        "category": "Agent Architecture",
        "difficulty": "Intermediate",
        "icon": "🧭",
        "definition": "An autonomous computational entity that perceives its environment through sensors and directs its activity through actuators to achieve specific goals (PAGE: Percepts, Actions, Goals, Environment).",
        "concepts": [
            "Simple Reflex Agents (Rule-based condition-action mapping)",
            "Model-Based Reflex Agents (Maintains internal world state)",
            "Goal-Based Agents (Selects actions toward defined objective)",
            "Utility-Based Agents (Optimizes performance/happiness trade-offs)",
            "Learning Agents (Improves decision quality from historical feedback)"
        ],
        "applications": [
            "Automated high-frequency algorithmic trading bots",
            "Smart climate thermostats (e.g., Nest HVAC controller)",
            "Autonomous warehouse inventory robots (AGVs)",
            "Non-Player Characters (NPCs) in video games"
        ],
        "example": "A robotic vacuum cleaner sensing obstacles via bump sensors, maintaining an internal room coordinate grid, and choosing paths that maximize dust collection while conserving battery.",
        "complexity": "Agent loop runs in O(1) to O(b^d) depending on planning horizon."
    },
    "BFS": {
        "name": "Breadth First Search (BFS)",
        "category": "Uninformed Search",
        "difficulty": "Beginner",
        "icon": "🌊",
        "definition": "An uninformed graph and tree search algorithm that begins at the root node and explores all neighbor nodes at the present depth level before moving on to the nodes at the next depth level.",
        "concepts": [
            "First-In-First-Out (FIFO) queue data structure",
            "Systematic level-order node expansion",
            "Uniform step-cost optimality (finds shallowest goal)",
            "Complete if branching factor b is finite and goal exists"
        ],
        "applications": [
            "Shortest path in unweighted graphs (e.g., peer-to-peer routing)",
            "Web crawlers indexing hyperlinks within a hop distance",
            "Social network connection degree calculation (e.g., LinkedIn 2nd/3rd degree)"
        ],
        "example": "Finding the minimum number of friend hops separating two people on a social media network.",
        "complexity": "Time Complexity: O(b^d), Space Complexity: O(b^d) (high memory requirement), where b = branching factor, d = depth of shallowest solution."
    },
    "DFS": {
        "name": "Depth First Search (DFS)",
        "category": "Uninformed Search",
        "difficulty": "Beginner",
        "icon": "🌲",
        "definition": "An uninformed search algorithm that explores as deep as possible along each branch before backtracking to the most recent unexplored fork.",
        "concepts": [
            "Last-In-First-Out (LIFO) stack data structure or recursive function call stack",
            "Linear space requirements relative to maximum depth",
            "Backtracking upon encountering dead-end states",
            "Not optimal (can return a deeper goal before exploring a shallow one)"
        ],
        "applications": [
            "Maze generation and path validation",
            "Topological sorting and cycle detection in Directed Acyclic Graphs (DAGs)",
            "Abstract Syntax Tree (AST) parsing in compilers"
        ],
        "example": "Navigating a labyrinth by following a single path until a wall is reached, then stepping back to the nearest turn.",
        "complexity": "Time Complexity: O(b^m), Space Complexity: O(bm) (memory-efficient), where b = branching factor, m = maximum search depth."
    },
    "A*": {
        "name": "A* Search Algorithm",
        "category": "Informed Search",
        "difficulty": "Intermediate",
        "icon": "⭐",
        "definition": "The premier best-first heuristic search algorithm combining the exact cost incurred from the start node with an estimated heuristic cost to reach the goal state.",
        "concepts": [
            "Evaluation function: f(n) = g(n) + h(n)",
            "g(n) = Exact cumulative path cost from start to current node n",
            "h(n) = Estimated heuristic cost from node n to goal",
            "Admissibility condition: h(n) <= h*(n) (never overestimates true cost)",
            "Consistency (monotonicity): h(n) <= c(n, a, n') + h(n')"
        ],
        "applications": [
            "Real-time GPS turn-by-turn navigation (e.g., Google Maps)",
            "Pathfinding in video games (unit movement on navmesh)",
            "Robotic arm kinematic trajectory planning"
        ],
        "example": "Finding the quickest driving route across a road network where g(n) is actual road miles driven and h(n) is straight-line Euclidean distance to the target city.",
        "complexity": "Time: Exponential in worst case O(b^d), but practically polynomial when heuristic error is small. Space: O(b^d) as all open nodes are tracked."
    },
    "Greedy Search": {
        "name": "Greedy Best-First Search",
        "category": "Informed Search",
        "difficulty": "Intermediate",
        "icon": "⚡",
        "definition": "A heuristic search strategy that expands the node that appears to be closest to the goal based solely on the heuristic evaluation function f(n) = h(n), ignoring the accumulated path cost.",
        "concepts": [
            "Evaluation function: f(n) = h(n)",
            "Prioritizes immediate perceived progress",
            "Susceptible to dead-ends, false leads, and infinite loops",
            "Neither complete nor optimal in general search spaces"
        ],
        "applications": [
            "Rapid approximate path generation under severe compute limits",
            "Greedy geographic packet forwarding in wireless sensor networks"
        ],
        "example": "Navigating toward a city by always driving on the highway that points most directly toward the destination compass bearing, even if it leads to an impassable canyon.",
        "complexity": "Time Complexity: O(b^m) worst case. Space Complexity: O(b^m)."
    },
    "Hill Climbing": {
        "name": "Hill Climbing Search",
        "category": "Local Search",
        "difficulty": "Intermediate",
        "icon": "⛰️",
        "definition": "An iterative mathematical optimization technique that starts with an arbitrary solution and continually moves in the direction of increasing value/elevation (steepest ascent) until no further improvement can be found.",
        "concepts": [
            "Greedy local neighborhood evaluation",
            "Maintains only the current state (O(1) constant memory)",
            "Vulnerable to local maxima, ridges, and flat plateaux",
            "Mitigations: Random-restart hill climbing, simulated annealing"
        ],
        "applications": [
            "8-Queens and N-Queens puzzle solving",
            "Traveling Salesperson Problem (2-opt edge swap optimization)",
            "Printed circuit board component placement"
        ],
        "example": "Attempting to climb to the summit of a mountain in heavy fog by only taking steps that move your elevation upward.",
        "complexity": "Time: O(d * b) where d is steps to peak and b is local branch factor. Space: O(1) constant memory."
    },
    "Genetic Algorithms": {
        "name": "Genetic Algorithms",
        "category": "Evolutionary Computation",
        "difficulty": "Advanced",
        "icon": "🧬",
        "definition": "Stochastic adaptive search heuristics inspired by Charles Darwin's principles of natural selection and biological genetics.",
        "concepts": [
            "Chromosome representation (binary bitstrings, permutation vectors)",
            "Fitness function (objective score guiding survival)",
            "Selection operators (Roulette wheel, tournament selection)",
            "Crossover (genetic recombination between pairs of solutions)",
            "Mutation (random perturbations to maintain genetic diversity)"
        ],
        "applications": [
            "Airfoil and aerodynamic shape optimization for aerospace",
            "University exam scheduling and complex timetable generation",
            "Neural network architecture search (NAS)"
        ],
        "example": "Evolving optimal antenna geometries for deep-space satellites by breeding promising designs over hundreds of generations.",
        "complexity": "Time: O(g * p * f) where g = generations, p = population size, f = fitness evaluation runtime."
    },
    "Minimax": {
        "name": "Minimax Algorithm",
        "category": "Adversarial Search",
        "difficulty": "Intermediate",
        "icon": "♟️",
        "definition": "A recursive backtracking decision algorithm used in two-player zero-sum sequential games with perfect information to determine the optimal move for a player under the assumption that the opponent also plays optimally.",
        "concepts": [
            "MAX nodes seek to maximize the evaluation score",
            "MIN nodes seek to minimize the evaluation score",
            "Terminal payoff evaluation and heuristic evaluation functions",
            "Game tree depth limitation and leaf evaluation"
        ],
        "applications": [
            "Classic board games: Tic-Tac-Toe, Checkers, Connect-Four",
            "Chess and Othello decision engines",
            "Competitive zero-sum market modeling"
        ],
        "example": "A Tic-Tac-Toe bot simulating all possible board states to guarantee at least a draw or a win against any opponent move.",
        "complexity": "Time Complexity: O(b^m), Space Complexity: O(bm) where b is branching factor and m is maximum game depth."
    },
    "Alpha-Beta Pruning": {
        "name": "Alpha-Beta Pruning",
        "category": "Adversarial Search Optimization",
        "difficulty": "Advanced",
        "icon": "✂️",
        "definition": "An optimization algorithm for the standard Minimax procedure that systematically cuts off branches of the game tree that are mathematically proven to be inferior to previously examined options.",
        "concepts": [
            "Alpha (α): The highest (best) value MAX is guaranteed along the path",
            "Beta (β): The lowest (best) value MIN is guaranteed along the path",
            "Pruning Condition: Whenever α >= β, the current branch is pruned",
            "Preserves identical decision output to full Minimax search"
        ],
        "applications": [
            "High-performance Chess engines (Deep Blue, Stockfish evaluation trees)",
            "Checkers world-championship program (Chinook)",
            "Real-time turn-based tactical strategy games"
        ],
        "example": "If MIN already has a move leading to score 3, and in a second branch MAX can force a score of at least 7, MIN will never allow play to reach that second branch, so search terminates immediately.",
        "complexity": "With ideal move ordering, search complexity drops to O(b^(m/2)), effectively doubling the search depth within the same compute budget."
    },
    "Expert Systems": {
        "name": "Expert Systems",
        "category": "Knowledge Engineering",
        "difficulty": "Intermediate",
        "icon": "📚",
        "definition": "Knowledge-intensive AI computer systems designed to solve complex domain problems by formalizing and applying the heuristic decision rules of human subject-matter experts.",
        "concepts": [
            "Knowledge Base: Explicit repository of domain facts and IF-THEN rules",
            "Inference Engine: Reasoning engine applying Forward Chaining or Backward Chaining",
            "Working Memory: Dynamic facts representing current case state",
            "Explanation Facility: Subsystem providing transparent 'Why' and 'How' audit trails"
        ],
        "applications": [
            "MYCIN (bacterial infection diagnosis and antibiotic recommendation)",
            "DENDRAL (organic chemical mass spectrometry analysis)",
            "Credit underwriting and banking fraud detection rules"
        ],
        "example": "Medical triage system: IF temperature > 38.5C AND platelet_count < 100000 AND joint_pain == True THEN Recommend Dengue Antigen Test.",
        "complexity": "Pattern-matching algorithms (e.g., Rete algorithm) achieve linear to quadratic rule evaluation relative to active facts."
    },
    "Game Playing": {
        "name": "Game Playing in AI",
        "category": "Strategic AI",
        "difficulty": "Intermediate",
        "icon": "🎮",
        "definition": "The formal AI methodology of formalizing board, card, and video games as state-space search problems with explicit states, transition models, and utility payoff functions.",
        "concepts": [
            "State Space Representation and ply notation",
            "Heuristic Static Evaluation Functions for non-terminal game states",
            "Horizon Effect & Quiescence Search for volatile positions",
            "Monte Carlo Tree Search (MCTS) for games with enormous branching factors (Go)"
        ],
        "applications": [
            "AlphaGo / AlphaZero (combining MCTS with deep policy networks)",
            "Imperfect information game engines (Poker bots using Counterfactual Regret)",
            "Tactical game AI in RTS titles (StarCraft II, Age of Empires)"
        ],
        "example": "Using Monte Carlo rollouts in Go to simulate thousands of random endgames from a position to compute win probability without evaluating every branch.",
        "complexity": "Game tree complexities: Tic-Tac-Toe ~10^5, Chess ~10^123, Go ~10^360."
    },
    "Python for AI": {
        "name": "Python for Artificial Intelligence",
        "category": "Programming Foundations",
        "difficulty": "Fundamental",
        "icon": "🐍",
        "definition": "The dominant high-level programming language used across artificial intelligence, machine learning, and data science owing to its clean readability, rich mathematical libraries, and extensive scientific computing ecosystem.",
        "concepts": [
            "NumPy: High-performance N-dimensional array processing and vector math",
            "Pandas: Data structures, tabular dataframes, and analytical data wrangling",
            "Matplotlib & Plotly: Interactive 2D/3D visualizations and academic charting",
            "Scikit-learn: Classical machine learning algorithms, classification, and regression",
            "PyTorch & TensorFlow: Autograd computation and deep neural network training"
        ],
        "applications": [
            "Data preprocessing and feature engineering pipelines",
            "AI model training, hyperparameter search, and inference backends",
            "Web dashboard deployment via Streamlit and interactive notebooks"
        ],
        "example": "Loading student academic records with pandas.read_csv(), computing statistical risk with NumPy, and generating interactive performance charts using Plotly.",
        "complexity": "Python interpreted speed is offset by C/Fortran optimized library bindings."
    }
}

# Ensure title and key_concepts aliases exist for seamless UI compatibility
for _key, _topic in KNOWLEDGE_TOPICS.items():
    if "title" not in _topic:
        _topic["title"] = _topic.get("name", _key)
    if "key_concepts" not in _topic:
        _topic["key_concepts"] = _topic.get("concepts", [])
    if "concepts" not in _topic:
        _topic["concepts"] = _topic.get("key_concepts", [])


def get_topic(topic_name: str) -> Optional[Dict[str, Any]]:
    """Retrieves full details for a specified knowledge topic."""
    # Try exact match
    if topic_name in KNOWLEDGE_TOPICS:
        return KNOWLEDGE_TOPICS[topic_name]

    # Try case-insensitive and normalized match
    clean_target = topic_name.strip().lower()
    for key, val in KNOWLEDGE_TOPICS.items():
        if clean_target == key.lower():
            return val
        if clean_target == val.get("name", "").lower():
            return val

    # Substring match
    for key, val in KNOWLEDGE_TOPICS.items():
        if clean_target in key.lower() or clean_target in val.get("name", "").lower():
            return val

    return None


def search_topic(query: str) -> List[Dict[str, Any]]:
    """Searches knowledge base by keywords across names, definitions, and concepts."""
    clean_q = query.strip().lower()
    if not clean_q:
        return list(KNOWLEDGE_TOPICS.values())

    results = []
    for key, topic in KNOWLEDGE_TOPICS.items():
        match_score = 0
        name_lower = topic["name"].lower()
        def_lower = topic["definition"].lower()
        cat_lower = topic["category"].lower()
        concepts_str = " ".join(topic.get("concepts", [])).lower()

        if clean_q in name_lower:
            match_score += 10
        if clean_q in def_lower:
            match_score += 5
        if clean_q in cat_lower:
            match_score += 4
        if clean_q in concepts_str:
            match_score += 3

        # Word token matching
        for word in clean_q.split():
            if len(word) > 2:
                if word in name_lower:
                    match_score += 3
                if word in def_lower:
                    match_score += 1

        if match_score > 0:
            results.append((match_score, topic))

    # Sort results by match score descending
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results]


def get_all_topics() -> List[str]:
    """Returns a list of all topic titles."""
    return list(KNOWLEDGE_TOPICS.keys())


def get_all_topic_details() -> Dict[str, Dict[str, Any]]:
    """Returns the complete dictionary of knowledge topics."""
    return KNOWLEDGE_TOPICS
