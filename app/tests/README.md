# Testing Documentation

This folder contains unit and integration tests covering the full data pipeline for the Health Habit Hub application.

## Test Types

### Unit Tests
- Test individual components and functions in isolation
- Do not require external services
- Run quickly and reliably

### Integration Tests
- Test interactions with external services (databases, APIs)
- Require actual service instances to be running
- More comprehensive but require setup

## Services Tested

- **Translation service** (LibreTranslate API)
- **Fuseki RDF store** (SPARQL inserts/reads)
- **Neo4j graph database** (with n10s plugin for RDF import)
- **MongoDB** (surveys + results storage)

## Quick Start

### 1. Start Required Services

From the repository root, start the services via Docker Compose:

```bash
docker compose up -d proxy fuseki neo4j mongo translate
```

### 2. Install Dependencies

```bash
cd app && npm install
```

### 3. Run Tests

#### All Unit Tests (Default)
```bash
npm run test:unitTests
```
This runs all tests. Integration tests that require `ENABLE_INTEGRATION=1` will be skipped.

#### Individual Integration Tests
```bash
npm run test:neo4j      # Neo4j integration tests
npm run test:fuseki     # Fuseki integration tests  
npm run test:mongo      # MongoDB integration tests
npm run test:translate  # Translation service tests
```

#### All Integration Tests
```bash
npm run test:integration
```

#### Full Test Suite (with linting)
```bash
npm test
```

## ENABLE_INTEGRATION Environment Variable

The `ENABLE_INTEGRATION` environment variable controls whether certain integration tests run or are skipped:

- **When NOT set** (default): Integration tests in `SparqlDatabase.test.js` are skipped
- **When set to `1` or `true`**: All integration tests run

### What It Controls

Currently, `ENABLE_INTEGRATION` only affects tests in `SparqlDatabase.test.js`:
- `Insert open data (integration)`
- `Insert closed data (integration)`

Other integration tests (Neo4j, Fuseki, MongoDB, Translation) run by default but gracefully skip if services are unavailable.

### Why Use It?

The `ENABLE_INTEGRATION` flag allows for:
- **Fast unit test runs** during development (skip integration tests)
- **Selective integration testing** when only specific services are available
- **CI/CD flexibility** where integration tests can be enabled/disabled per environment

## Test Files Overview

| Test File | Type | Services Required | Description |
|-----------|------|-------------------|-------------|
| `SparqlDatabase.test.js` | Unit + Integration | Fuseki (if `ENABLE_INTEGRATION=1`) | Tests DbClient class and SPARQL operations |
| `FusekiDatabase.integration.test.js` | Integration | Fuseki | End-to-end Fuseki insertion and verification |
| `Neo4jDatabase.test.js` | Integration | Neo4j | Neo4j connection and data insertion tests |
| `Mongo.test.js` | Integration | MongoDB | MongoDB CRUD operations for surveys |
| `TranslateService.test.js` | Integration | LibreTranslate | Translation API functionality |

## Configuration

### Environment Variables

Tests use the following environment variables (with defaults):

#### Neo4j
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j  
NEO4J_PASSWORD=neo4j_password_change_me
```

#### Fuseki
```bash
FUSEKI_HOST=localhost
FUSEKI_PORT=3030
FUSEKI_DATASET=hhh
FUSEKI_USER=admin
FUSEKI_PASSWORD=admin
```

#### MongoDB  
```bash
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=admin
MONGO_DB=test_surveyjs
MONGO_AUTH_SOURCE=admin
```

#### Translation Service
```bash
TRANSLATE_HOST=localhost
TRANSLATE_PORT=5000
```

### Configuration Files

- Environment variables are loaded from the root `.env` file
- Service configurations are centralized in `app/utils/config.js`
- MongoDB configuration is handled in `app/models/survey.js`

## Test Behavior

### Graceful Degradation

Tests are designed to handle service unavailability gracefully:

- **Service unavailable**: Test is skipped with informative message
- **Authentication failure**: Test is skipped (not failed) 
- **Connection timeout**: Test fails fast (no hanging)
- **Network errors**: Test is skipped with error details

### Connection Management

- All database connections are properly closed after tests
- Timeouts prevent tests from hanging indefinitely
- Connection cleanup prevents event loop issues

### Test Isolation

- Tests clean up their own data
- No dependencies between test runs
- Each test uses unique identifiers to avoid conflicts

## Troubleshooting

### Common Issues

#### Tests Hanging
- **Fixed**: All hanging issues have been resolved with proper connection cleanup and timeouts

#### MongoDB Authentication Failed
- Ensure MongoDB is running: `docker compose up -d mongo`
- Verify credentials in root `.env` file match MongoDB setup
- Check MongoDB is accessible: `mongosh "mongodb://admin:admin@localhost:27017/?authSource=admin"`

#### Neo4j Connection Failed  
- Ensure Neo4j is running: `docker compose up -d neo4j`
- Verify Bolt port 7687 is accessible
- Check credentials in `.env` file

#### Fuseki Not Reachable
- Ensure Fuseki is running: `docker compose up -d fuseki`
- Verify dataset `hhh` exists and is writable
- Check admin/admin credentials work

#### Translation Service Timeout
- Ensure LibreTranslate is running: `docker compose up -d translate`
- Wait a few seconds after container startup (model loading)
- Check service is responding: `curl -X OPTIONS http://localhost:5000/translate`

### Debugging Tips

1. **Check service logs**:
   ```bash
   docker compose logs [service-name]
   ```

2. **Verify service connectivity**:
   ```bash
   # MongoDB
   mongosh "mongodb://admin:admin@localhost:27017/?authSource=admin"
   
   # Neo4j (in browser)
   open http://localhost:7474
   
   # Fuseki (in browser)  
   open http://localhost:3030
   
   # Translation service
   curl http://localhost:5000/translate
   ```

3. **Run individual tests**:
   ```bash
   node --test tests/[specific-test-file].js
   ```

4. **Enable debug output**:
   ```bash
   DEBUG=* npm run test:unitTests
   ```

## Recent Improvements

### Fixed Issues
- ✅ Resolved hanging tests by implementing proper connection cleanup
- ✅ Added graceful error handling for service unavailability  
- ✅ Implemented proper timeouts to prevent infinite waits
- ✅ Fixed MongoDB configuration and authentication
- ✅ Improved test isolation and cleanup
- ✅ Enhanced error messages for better debugging

### Best Practices Implemented
- Proper resource management (connection cleanup)
- Consistent error handling patterns
- Clear, descriptive test failure messages
- Test data cleanup and isolation
- Timeout management for external services
- Graceful handling of service dependencies

## Test Results Interpretation

### Success Indicators
```
✔ Test Name (duration)     # Passed
﹣ Test Name (duration) # Message   # Skipped (expected when service unavailable)
```

### Failure Indicators  
```
✖ Test Name (duration)     # Failed (investigate issue)
```

### Typical Results
When all services are running:
- **8-10 tests passing**
- **0-2 tests skipped** (depending on ENABLE_INTEGRATION)
- **0 tests failing**

When services are unavailable:
- **5-7 tests passing** (unit tests)
- **3-5 tests skipped** (integration tests)
- **0 tests failing** (graceful degradation)