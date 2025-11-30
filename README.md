#  Smart Task Analyzer  
An intelligent task-prioritization system with multiple scoring strategies, circular dependency detection, business-day urgency logic, animated UI, and a clean REST API backend.

---
## Project Structure
```yaml
project_structure:
  backend:
    - backend/
    - tasks/
      - scoring.py
      - validator.py
      - dependency_check.py
      - date_intel.py
      - config.py
      - views.py
      - tests.py
  frontend:
    - index.html
    - styles.css
    - script.js
```

##  Features

```yaml
core_features:
  - Add tasks (title, due date, effort, importance, dependencies)
  - Analyze tasks using multiple strategies
  - Smart Balance scoring with explanation
  - Detect circular dependencies
  - Validate missing/invalid fields
  - Business-day urgency calculation
  - Modern animated frontend UI
  - Priority color indicators (High/Med/Low)
  - Responsive design
bonus_features:
  - Eisenhower Matrix View
  - Date intelligence (weekend-aware urgency)
  - Top-3 task suggestions
  - Configurable backend behavior
  - Toast notifications + loading states
```

**Smart Balance Strategy**
```yaml
smart_balance:
  description: "Primary scoring algorithm balancing urgency, importance, effort, and dependency cost."
  weights:
    urgency: 0.5
    importance: 0.4
    effort_penalty: 0.1
    dependency_penalty: 0.1
  overdue_behavior: "Overdue tasks receive maximum urgency"
```

**Fastest Wins Strategy**
```yaml
fastest_wins:
  description: "Prioritize low-effort tasks to maximize quick wins."
  formula: "score = 1 / (estimated_hours + 1)"
```

**High Impact Strategy**
```yaml
high_impact:
  description: "Importance dominates all other factors."
  formula: "score = importance"
```
**Deadline Driven Strategy**
```yaml
deadline_driven:
  description: "Tasks closer to deadline receive higher priority."
  formula: "score = -days_until_due"
```

**Critical Considerations & How They Are Handled**
```yaml
past_due_dates:
  handled: true
  behavior: "Tasks overdue by any number of days receive maximum urgency."

missing_or_invalid_data:
  handled: true
  validator_checks:
    - title required
    - date must be YYYY-MM-DD
    - estimated_hours >= 0
    - importance between 1 and 10
    - dependencies must be a list of strings
  error_response_example:
    error: "Invalid task data"
    details: "importance must be between 1 and 10"

circular_dependencies:
  handled: true
  method: "Depth-First Search cycle detection"
  backend_example:
    error: "Circular dependency detected"
    has_cycle: true
    cycle_nodes: ["A", "B", "C", "A"]
  frontend_visual: "Prominent red banner above results"

configurability:
  file: "backend/tasks/config.py"
  settings:
    - CHECK_CIRCULAR_DEPENDENCIES
    - WEEKEND_AWARE_URGENCY
    - DEFAULT_STRATEGY

priority_balancing:
  description: >
    Smart Balance intelligently weighs urgency, importance, effort, and dependency count
    to resolve competing priorities realistically.
```
## API Endpoints
**Analyze Tasks**
```yaml
POST /api/tasks/analyze/?strategy=[smart|fastest|high_impact|deadline]

request_example:
  - title: "Fix login bug"
    due_date: "2025-11-30"
    estimated_hours: 3
    importance: 8
    dependencies: []

response_example:
  tasks: [...]
  has_cycle: false
  cycle_nodes: []
```
**Suggest Tasks (Top 3)**
```yaml
POST /api/tasks/suggest/

response_example:
  suggested_tasks: [...]
  note: "Top 3 tasks using Smart Balance scoring."
```
## Bonus Features
```yaml
bonus_features:
  - Business-day urgency system
  - Circular dependency banner visualization
  - Eisenhower Matrix
  - Strategy dropdown selector
  - Animated UI and task cards
  - Top-3 smart suggestions
  - Frontend validation + bulk import
  - Configurable backend scoring weights
```
## Frontend Features
```yaml
  components:
    - Task creation form
    - JSON bulk input box
    - Strategy dropdown
    - Animated task result cards
    - Priority chips (High/Medium/Low)
    - Toast notifications
    - Loading indicators
    - Scrollable results section
    - Eisenhower Matrix popup
  visualization:
    eisenhower_matrix:
      quadrants:
        Q1: "Urgent + Important"
        Q2: "Not Urgent + Important"
        Q3: "Urgent + Not Important"
        Q4: "Neither"
    cycle_warning_banner:
      message_example: "Circular dependency: A → B → C → A"
```
