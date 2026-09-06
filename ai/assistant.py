"""SmartCampus AI - Assistant Response Engine Module
Local, deterministic AI assistant powered by keyword analysis, fuzzy matching,
curriculum heuristics, and the local AI Knowledge Base.
Operates completely offline with zero external API dependencies.
"""

import re
from typing import Dict, Any, Optional
from ai.knowledge_base import get_topic, search_topic, get_all_topics


def get_ai_response(query: str, student_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Processes user query and returns a structured academic or conceptual response.

    Args:
        query: User input string.
        student_context: Optional student analysis dictionary for contextual performance queries.

    Returns:
        Dict with 'title', 'category', 'difficulty', 'response', and optional metadata.
    """
    clean_q = query.strip().lower()
    if not clean_q:
        return {
            "title": "SmartCampus AI",
            "category": "Assistant",
            "difficulty": "General",
            "response": "Please enter a question! You can ask me about search algorithms (BFS, DFS, A*), game playing (Minimax, Alpha-Beta), Expert Systems, or study tips."
        }

    # ------------------------------------------------------------
    # 1. PERSONAL PERFORMANCE & ADVISORY INTENT
    # ------------------------------------------------------------
    if any(p in clean_q for p in ["how am i doing", "my performance", "my grades", "my score", "am i at risk", "my standing"]):
        if student_context:
            score = student_context.get("performance", 75)
            level = student_context.get("level", "Good")
            risk = student_context.get("risk", "LOW")
            strengths = student_context.get("strengths", [])
            weaknesses = student_context.get("weaknesses", [])
            
            resp_lines = [
                f"### Your Academic Status Overview",
                f"• **Overall Score:** {score}% ({level} Standing)",
                f"• **Academic Risk Tier:** **{risk}**",
                f"• **Attendance:** {student_context.get('attendance', 80)}%",
                f"• **Daily Study Hours:** {student_context.get('study_hours', 3.0)} hrs/day\n"
            ]
            if strengths:
                resp_lines.append(f"✅ **Key Strength:** {strengths[0]}")
            if weaknesses:
                resp_lines.append(f"⚠️ **Key Focus Area:** {weaknesses[0]}")
            resp_lines.append("\nCheck the **Recommendations** and **Study Planner** tabs for customized daily study schedules.")
            
            return {
                "title": "Academic Health Diagnostic",
                "category": "Student Advisory",
                "difficulty": "Personalized",
                "response": "\n".join(resp_lines)
            }
        else:
            return {
                "title": "Academic Health Diagnostic",
                "category": "Student Advisory",
                "difficulty": "General",
                "response": "Your overall standing is tracked under the **Dashboard** and **Performance** pages. Review your personalized attendance, study hours, and recommendations there!"
            }

    # ------------------------------------------------------------
    # 2. STUDY TIPS & STRATEGY INTENT
    # ------------------------------------------------------------
    if any(p in clean_q for p in ["study tip", "how to study", "exam prep", "how to prepare", "how should i prepare", "pass exam", "advice"]):
        return {
            "title": "Evidence-Based Engineering Study Strategy",
            "category": "Study Methodology",
            "difficulty": "Advisory",
            "response": (
                "Here is the recommended 4-step engineering study method:\n\n"
                "1. **Spaced Retrieval Practice**: Don't just re-read slides. Close your notes and write out the algorithm (e.g., BFS vs. DFS queue operations) from memory.\n\n"
                "2. **The Feynman Technique**: Explain tricky concepts (such as A* admissibility or Alpha-Beta pruning) in simple words as if teaching a classmate.\n\n"
                "3. **Time-Blocked Focus**: Use 45-minute deep focus sprints followed by mandatory 10-minute rest intervals (use our Study Planner tool).\n\n"
                "4. **Past Midterm Drills**: Solve previous semester question papers under strict timed conditions."
            )
        }

    # ------------------------------------------------------------
    # 3. CURRICULUM SUBJECT QUERIES (Networking, DBMS, Mathematics)
    # ------------------------------------------------------------
    if any(k in clean_q for k in ["networking", "osi model", "tcp/ip", "tcp vs udp", "subnet"]):
        return {
            "title": "Computer Networking Core Concepts",
            "category": "Curriculum Support",
            "difficulty": "Intermediate",
            "response": (
                "**Essential Computer Networking Revision Points:**\n\n"
                "• **OSI 7-Layer Reference Model:**\n"
                "  1. Physical (bits, cables)\n"
                "  2. Data Link (frames, MAC addresses, Ethernet)\n"
                "  3. Network (packets, IP addressing, routing)\n"
                "  4. Transport (segments, TCP reliable byte stream / UDP datagrams)\n"
                "  5. Session (dialog control, token management)\n"
                "  6. Presentation (data formatting, SSL/TLS encryption, compression)\n"
                "  7. Application (HTTP, DNS, SMTP, FTP)\n\n"
                "• **TCP vs. UDP:** TCP ensures reliable in-order delivery with 3-way handshakes (SYN, SYN-ACK, ACK) and congestion control. UDP provides low-latency, connectionless transmission without delivery guarantees (ideal for streaming and VoIP)."
            )
        }

    if any(k in clean_q for k in ["dbms", "database", "normalization", "bcnf", "acid"]):
        return {
            "title": "Database Management Systems (DBMS) Revision",
            "category": "Curriculum Support",
            "difficulty": "Intermediate",
            "response": (
                "**Essential DBMS Concepts for Examination:**\n\n"
                "• **ACID Properties of Transactions:**\n"
                "  - **Atomicity:** All operations complete or the transaction rolls back completely.\n"
                "  - **Consistency:** Database transitions only between valid states conforming to all integrity constraints.\n"
                "  - **Isolation:** Concurrent transactions execute without mutual interference (enforced via locks/2PL).\n"
                "  - **Durability:** Committed changes persist safely even across system crashes.\n\n"
                "• **Normalization Levels:**\n"
                "  - **1NF:** Atomic attribute values; no repeating groups.\n"
                "  - **2NF:** 1NF + elimination of partial functional dependencies (all non-key attributes depend on whole candidate key).\n"
                "  - **3NF:** 2NF + elimination of transitive dependencies (X -> Y, Y -> Z).\n"
                "  - **BCNF:** For every non-trivial functional dependency X -> Y, X must be a superkey."
            )
        }

    if any(k in clean_q for k in ["math", "mathematics", "linear algebra", "discrete"]):
        return {
            "title": "Engineering Mathematics for AI",
            "category": "Curriculum Support",
            "difficulty": "Foundational",
            "response": (
                "**Mathematical Foundations in AI & Computer Science:**\n\n"
                "• **Linear Algebra:** Vectors represent state spaces, feature embeddings, and neural activations. Matrices perform spatial transformations, coordinate rotations, and dimensionality reductions (PCA).\n"
                "• **Probability & Statistics:** Bayes' Theorem underpins probabilistic reasoning and Bayesian networks: P(A|B) = [P(B|A) * P(A)] / P(B).\n"
                "• **Discrete Mathematics:** Graph theory (V, E) forms the basis for state space trees, BFS/DFS traversals, topological sorts, and Dijkstra/A* shortest paths."
            )
        }

    # ------------------------------------------------------------
    # 4. KNOWLEDGE BASE SEARCH & TOPIC MAPPING
    # ------------------------------------------------------------
    # Direct alias matching
    topic_alias_map = {
        "bfs": "BFS",
        "breadth": "BFS",
        "breadth first search": "BFS",
        "dfs": "DFS",
        "depth": "DFS",
        "depth first search": "DFS",
        "a*": "A*",
        "a star": "A*",
        "astar": "A*",
        "heuristic search": "A*",
        "greedy": "Greedy Search",
        "greedy search": "Greedy Search",
        "greedy best first": "Greedy Search",
        "hill climbing": "Hill Climbing",
        "hill climb": "Hill Climbing",
        "local search": "Hill Climbing",
        "genetic": "Genetic Algorithms",
        "genetic algorithm": "Genetic Algorithms",
        "genetic algorithms": "Genetic Algorithms",
        "minimax": "Minimax",
        "mini max": "Minimax",
        "adversarial search": "Minimax",
        "alpha beta": "Alpha-Beta Pruning",
        "alpha-beta": "Alpha-Beta Pruning",
        "pruning": "Alpha-Beta Pruning",
        "expert system": "Expert Systems",
        "expert systems": "Expert Systems",
        "rule based": "Expert Systems",
        "rule engine": "Expert Systems",
        "intelligent agent": "Intelligent Agents",
        "intelligent agents": "Intelligent Agents",
        "agent": "Intelligent Agents",
        "agents": "Intelligent Agents",
        "game playing": "Game Playing",
        "game playing in ai": "Game Playing",
        "python": "Python for AI",
        "python for ai": "Python for AI",
        "ai": "Artificial Intelligence",
        "artificial intelligence": "Artificial Intelligence"
    }

    matched_topic_name = None
    
    # Check normalized keywords in query
    for alias, canonical_name in sorted(topic_alias_map.items(), key=lambda x: len(x[0]), reverse=True):
        # Use regex boundary matching where appropriate or word containment
        if re.search(r'\b' + re.escape(alias) + r'\b', clean_q):
            matched_topic_name = canonical_name
            break

    # If not matched directly, query search_topic
    if not matched_topic_name:
        search_hits = search_topic(clean_q)
        if search_hits:
            matched_topic_name = search_hits[0]["name"]

    # If topic found in knowledge base, format comprehensive response
    if matched_topic_name:
        topic = get_topic(matched_topic_name)
        if topic:
            concepts_formatted = "\n".join([f"• {c}" for c in topic.get("concepts", [])])
            apps_formatted = "\n".join([f"• {a}" for a in topic.get("applications", [])])
            
            response_text = (
                f"### {topic['name']}\n\n"
                f"**Definition:**\n{topic['definition']}\n\n"
                f"**Key Concepts:**\n{concepts_formatted}\n\n"
                f"**Real-World Applications:**\n{apps_formatted}\n\n"
                f"**Practical Example:**\n{topic.get('example', '')}\n\n"
                f"**Complexity / Characteristics:**\n{topic.get('complexity', '')}"
            )

            return {
                "title": topic["name"],
                "category": topic["category"],
                "difficulty": topic.get("difficulty", "Intermediate"),
                "response": response_text
            }

    # ------------------------------------------------------------
    # 5. UNSUPPORTED TOPIC FALLBACK (EXPLICIT USER SPECIFICATION)
    # ------------------------------------------------------------
    return {
        "title": "SmartCampus Assistant",
        "category": "General",
        "difficulty": "Notice",
        "response": (
            f"I received your question: '{query}'.\n\n"
            "I don't have this topic in my current knowledge base. Try asking about:\n"
            "• **BFS & DFS** (Graph Search Algorithms)\n"
            "• **A* Search** & Heuristics\n"
            "• **Greedy Search & Hill Climbing**\n"
            "• **Minimax & Alpha-Beta Pruning**\n"
            "• **Genetic Algorithms**\n"
            "• **Expert Systems & Rule Engines**\n"
            "• **Intelligent Agents** (Reflex, Model, Goal, Utility)\n"
            "• **Python for AI** (NumPy, Pandas, Plotly)\n"
            "• **Curriculum Revisions** (Networking OSI/TCP, DBMS Normalization/ACID)"
        )
    }
