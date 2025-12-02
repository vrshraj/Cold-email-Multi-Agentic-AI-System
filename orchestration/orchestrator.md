# Orchestrator

## Purpose
The orchestrator is the AI decision-making layer that reads directives, determines which agents to invoke, manages state transitions, and handles the overall pipeline execution.

## How It Works

### 1. Initialization
- Load workflow plan from `workflow_plans/`
- Read relevant directives from `directives/`
- Initialize state machine from `state_machine.json`
- Set up execution context

### 2. Decision Making
The orchestrator makes decisions based on:
- Current pipeline state
- Available data and resources
- Error conditions and retries
- Business rules and constraints
- Performance metrics

### 3. Agent Routing
Uses `agent_router.md` to determine:
- Which agent/tool to call next
- What parameters to pass
- How to handle the response
- When to transition states

### 4. State Management
- Track current state in pipeline
- Validate state transitions
- Persist state for recovery
- Handle rollbacks if needed

### 5. Error Handling
- Detect failures at each stage
- Apply retry logic with backoff
- Route to error recovery agents
- Escalate critical issues

## Execution Flow

```
1. Read workflow plan
2. Load initial state
3. While pipeline not complete:
   a. Determine next action from current state
   b. Read relevant directive
   c. Route to appropriate agent/tool
   d. Execute action
   e. Validate output
   f. Update state
   g. Log results
   h. Check for errors
4. Generate execution report
5. Trigger learner if configured
```

## AI Prompting Strategy

When the AI reads this orchestrator file, it should:
1. Understand the overall workflow from the plan
2. Read the directive for the current stage
3. Use the agent router to select the right tool
4. Execute the tool with proper parameters
5. Validate the output against directive success criteria
6. Decide next action based on state machine
7. Handle errors according to directive guidelines

## Integration Points

- **Directives**: What to do (objectives, process, success criteria)
- **Agent Router**: Which agent to use
- **State Machine**: Valid transitions and states
- **Workflow Plans**: Specific pipeline configurations
- **Execution Tools**: Actual implementation scripts

## Example Decision Process

```
Current State: "scraped_data_available"
Directive: "extract_contacts.md"
Decision: Call extraction/extract_emails.py
Output: List of email addresses
Validation: Check against success criteria
Next State: "contacts_extracted"
Next Action: Route to "validate_lead.md"
```

## Monitoring and Logging

- Log all state transitions
- Record decision rationale
- Track execution time per stage
- Monitor resource usage
- Collect metrics for learner
