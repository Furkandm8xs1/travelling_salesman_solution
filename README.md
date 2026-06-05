# High-Scale Maximum City Visit Algorithm Design

## Problem Definition

Each city is represented by:

```text
(id, x, y, open_time, close_time)
```

Where:

* `x, y` are city coordinates.
* `open_time` is the earliest visit time.
* `close_time` is the latest visit time.
* Travel time between cities equals the rounded Euclidean distance.

### Objective

Primary objective:

```text
Maximize visited city count
```

Secondary objective:

```text
Minimize total route length
```

Visiting more cities is always more important than producing a shorter route.

---

# Design Goals

The algorithm must:

* Scale to 50,000+ cities.
* Avoid exhaustive search.
* Handle time windows efficiently.
* Maximize total visited cities.
* Produce high-quality routes within practical execution times.

---

# 1. Spatial Indexing

Searching all cities at every step is infeasible.

Use one of:

* Grid Index
* KD-Tree
* R-Tree

Target complexity:

```text
O(log N)
```

instead of:

```text
O(N)
```

for candidate retrieval.

Only nearby feasible cities should be considered.

---

# 2. Beam Search Core

Avoid single-path greedy routing.

Maintain multiple route candidates simultaneously.

Example:

```text
Beam Width = 50–200
```

At each expansion step:

1. Generate candidate moves.
2. Expand all beam states.
3. Score resulting routes.
4. Keep only the best beam states.

Benefits:

* Avoids early bad decisions.
* Preserves route diversity.
* Produces significantly higher visit counts.

---

# 3. Multi-Factor Candidate Scoring

Do not rank cities solely by distance.

Each candidate should receive a score based on:

```text
Candidate Score =
Distance Component
+ Urgency Component
+ Opportunity Component
+ Density Component
```

### Distance Component

Prefer nearby cities.

### Urgency Component

Prefer cities whose time windows are closing soon.

### Opportunity Component

Estimate future reachable cities after visiting this city.

### Density Component

Reward cities located in dense reachable regions.

---

# 4. Lookahead Evaluation

Before selecting a city:

Simulate several future moves.

Recommended depth:

```text
3–5 steps
```

Evaluate:

* Expected future city count.
* Future feasibility.
* Remaining opportunities.

Purpose:

Avoid local optima created by greedy decisions.

---

# 5. Cluster-Based Planning

Large datasets should be divided into regions.

Possible methods:

* K-Means
* Grid Clustering
* Spatial Partitioning

Example:

```text
100–500 clusters
```

Workflow:

1. Build clusters.
2. Determine cluster visitation order.
3. Solve locally within clusters.
4. Connect cluster routes.

Benefits:

* Reduces long-distance jumps.
* Improves route consistency.
* Scales better to large datasets.

---

# 6. Opportunity Density Heuristic

For each city calculate:

```text
Reachable cities within radius R
```

Example:

```text
R = 500
```

Metrics:

* Reachable city count.
* Average remaining slack.
* Future cluster density.

Cities located in high-opportunity areas should receive higher scores.

---

# 7. Adaptive Strategy Switching

Use different strategies during different route phases.

### Early Phase

Goal:

```text
Reach dense regions.
```

Priority:

* Opportunity Density
* Cluster Access

### Middle Phase

Goal:

```text
Collect as many cities as possible.
```

Priority:

* Density
* Future Reachability

### Late Phase

Goal:

```text
Rescue remaining feasible cities.
```

Priority:

* Urgency
* Closing Time

---

# 8. Local Search Optimization

After constructing a route:

Apply:

* 2-opt
* 3-opt
* Or-opt
* Segment Relocation

Purpose:

* Reduce unnecessary travel.
* Create room for additional city insertions.
* Improve route efficiency.

---

# 9. Multi-Start Exploration

Avoid dependence on a single starting city.

Generate routes from:

* Early-opening cities
* Late-closing cities
* Dense regions
* Central cities
* Random cities

Recommended:

```text
500–1000 starting points
```

Keep the best solutions discovered.

---

# 10. Elite Solution Pool

Maintain a pool of top solutions.

Example:

```text
Top 20–50 routes
```

Store:

* Visited city count
* Route length
* Completion time

Use elite routes for:

* Further local optimization
* Route merging
* Diversification

---

# 11. Final Optimization Objective

Optimization priority:

```text
1. Maximize Visited Cities
2. Minimize Route Length
3. Minimize Completion Time
```

Formal objective:

```text
maximize:
visited_city_count

then minimize:
route_length

then minimize:
completion_time
```

---

# Recommended Architecture

```text
Spatial Index
      ↓
Cluster Planning
      ↓
Beam Search
      ↓
Lookahead Evaluation
      ↓
Opportunity Density Scoring
      ↓
Adaptive Routing
      ↓
Local Search Optimization
      ↓
Elite Solution Pool
```

This architecture is designed specifically for very large city sets (50,000+ nodes) and prioritizes maximum city collection under time-window constraints.
