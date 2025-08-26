# AGENTS.md - Kinic Integration Example

This directory demonstrates how coding agents can use Kinic's semantic memory layer
to enhance their capabilities beyond standard AGENTS.md specifications.

## Kinic Memory Integration

```yaml
kinic:
  enabled: true
  endpoint: http://localhost:5006
  auto_save: true
  semantic_search_before_edit: true
  
  # Automatically search for context before making changes
  context_queries:
    - "similar implementations in codebase"
    - "previous bug fixes related to this"
    - "security considerations for this pattern"
    - "performance optimizations applied before"
  
  # Save patterns after successful implementations
  save_patterns:
    - on_test_pass: true
    - on_build_success: true
    - on_pr_merge: true
  
  # Cross-agent collaboration
  collaboration:
    share_with_agents: ["cursor", "aider", "jules", "codex"]
    discover_from_agents: true
    semantic_similarity_threshold: 0.8
```

## Project Context

This is a demonstration of how Kinic enhances agents.md by adding:
- **Persistent Memory**: Knowledge persists across sessions
- **Semantic Search**: Find code by meaning, not keywords
- **Cross-Agent Collaboration**: Different AI tools share knowledge
- **Blockchain Storage**: Permanent, verifiable knowledge base

## Build Commands

```bash
# Python projects
python -m pytest
ruff check
black .

# JavaScript/TypeScript projects
npm run build
npm run test
npm run lint
```

## Test Commands

```bash
# Run security tests
pytest tests/security/
npm run test:security

# Run integration tests
pytest tests/integration/
npm run test:integration
```

## Code Style Guidelines

### Python (FastAPI/Flask)
- Use type hints for all functions
- Follow PEP 8 conventions
- Async-first for I/O operations
- Comprehensive error handling

### TypeScript (Express/Next.js)
- Strict TypeScript configuration
- Functional components preferred
- Middleware-based architecture
- JWT for authentication

## Security Considerations

Before implementing authentication:
1. Search Kinic for "authentication vulnerabilities"
2. Review OWASP Top 10 patterns
3. Check for existing security implementations
4. Use parameterized queries for database operations

## Performance Guidelines

When optimizing code:
1. Search Kinic for "performance bottlenecks {feature}"
2. Review previous optimization patterns
3. Consider caching strategies
4. Profile before and after changes

## Collaboration Protocol

### Before Starting Work
```python
# Pseudo-code for agent behavior
context = kinic.search("related implementations")
patterns = kinic.search("best practices for {task}")
security = kinic.search("security considerations")
```

### After Completing Work
```python
# Save learned patterns
kinic.save({
  "implementation": code_changes,
  "patterns_used": design_patterns,
  "performance_metrics": benchmarks,
  "security_considerations": security_checks
})
```

## Agent-Specific Instructions

### For Cursor
- Focus on security and authentication patterns
- Always check Kinic for OAuth2/JWT implementations
- Save successful security patterns for other agents

### For Aider
- Focus on API design and documentation
- Search Kinic for RESTful patterns before implementing
- Document error handling strategies

### For Jules
- Focus on frontend optimization
- Check Kinic for React/Vue patterns
- Save performance optimizations

### For Codex
- Focus on algorithm optimization
- Search for existing algorithmic solutions
- Document time/space complexity

## Example Kinic Workflow

1. **Agent receives task**: "Implement user authentication"

2. **Search semantic memory**:
   ```bash
   kinic search "authentication implementation JWT OAuth2"
   ```

3. **Discover relevant knowledge**:
   - Previous JWT implementations
   - OAuth2 flow documentation
   - Security best practices
   - Error handling patterns

4. **Implement solution** using discovered patterns

5. **Save new knowledge**:
   ```bash
   kinic save "Implemented OAuth2 with refresh tokens"
   ```

6. **Other agents benefit** from this knowledge immediately

## Metrics & Impact

With Kinic integration, expect:
- **5x faster** implementation through knowledge reuse
- **90% reduction** in security vulnerabilities
- **Zero context loss** between sessions
- **Instant onboarding** for new agents

## Support & Documentation

- Kinic API: http://localhost:5006
- Documentation: [kinic.io](https://kinic.io)
- GitHub: [github.com/hshadab/kinic-api](https://github.com/hshadab/kinic-api)