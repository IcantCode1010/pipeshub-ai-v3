# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

PipesHub is a workplace AI platform built with a modular microservices architecture. The system consists of:

### Core Services
- **Frontend**: React/TypeScript with Material-UI, real-time chat interface, PDF/document viewers
- **Backend Python**: FastAPI-based AI service handling LLM interactions, embeddings, and document processing
- **Backend Node.js**: Express-based service for user management, authentication, and business logic
- **Connector Services**: Extensible connectors for Google Workspace, Microsoft 365, Slack, etc.

### Data Layer
- **ArangoDB**: Primary knowledge graph database storing documents, relationships, and metadata
- **Redis**: Caching, session management, and real-time data
- **Kafka**: Event streaming between services
- **Qdrant**: Vector database for embeddings and semantic search
- **MongoDB**: User data, conversations, and business logic storage

### AI Pipeline Architecture
The AI service follows a retrieval-augmented generation (RAG) pattern:
1. **Ingestion**: Documents from connectors → parsing → chunking → embedding
2. **Indexing**: Vector storage in Qdrant + metadata in ArangoDB
3. **Retrieval**: Hybrid search (semantic + keyword) → reranking → context assembly
4. **Generation**: LLM inference with streaming responses and citation tracking

### Multi-Provider AI Support
The platform supports 15+ LLM providers through a unified interface:
- **OpenAI**: GPT-4, GPT-3.5 models
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Haiku/Opus
- **Google**: Gemini 1.5 Pro/Flash, Gemini 2.5 Flash, Vertex AI
- **AWS Bedrock**: Claude, Titan models
- **Others**: Cohere, Mistral, Groq, Fireworks, Together, xAI, Ollama
- **Embedding models**: OpenAI, Voyage, JinaAI, Mistral, Cohere, local models

## Development Commands

### Frontend (React/TypeScript)
```bash
cd frontend
yarn dev                # Development server at localhost:3000
yarn dev:host          # Development server accessible on network
yarn build             # Production build
yarn lint              # ESLint check
yarn lint:fix          # Fix linting issues
yarn fm:check          # Prettier format check
yarn fm:fix            # Fix formatting
yarn re:start          # Clean reinstall and dev
yarn re:build          # Clean reinstall and build
```

### Backend Python (AI Service)
```bash
cd backend/python
# No pip/poetry commands - uses Docker exclusively
ruff check .           # Lint check
ruff format .          # Format code
# Note: Python service runs on ports 8000 (query), 8091 (indexing), 8088 (connectors)
```

### Backend Node.js
```bash
cd backend/nodejs/apps
npm run dev            # Development with nodemon (port 3001)
npm run build          # TypeScript compilation
npm run lint           # ESLint check
npm run format         # Prettier formatting
npm test               # Run Mocha tests

# Manual cleanup for stuck records (when needed)
node manual-cleanup-stuck-record.js
```

### Docker Development
```bash
cd deployment/docker-compose

# Development build (with source mounting and hot reload)
docker compose -f docker-compose.dev.yml -p pipeshub-ai up --build -d

# Production deployment
docker compose -f docker-compose.prod.yml -p pipeshub-ai up -d

# Stop services
docker compose -f docker-compose.dev.yml -p pipeshub-ai down

# View logs
docker compose -f docker-compose.dev.yml -p pipeshub-ai logs -f [service-name]

# Ollama development (for local LLM testing)
docker compose -f docker-compose.ollama-dev.yml -p pipeshub-ai up -d
```

### Service Ports
- **Frontend**: 3000
- **Backend Node.js**: 3001 (internal)
- **Python AI Service**: 8000 (query), 8091 (indexing), 8088 (connectors)
- **ArangoDB**: 8529
- **MongoDB**: 27017
- **Redis**: 6379
- **Qdrant**: 6333 (HTTP), 6334 (gRPC)
- **Kafka**: 9092

## Code Architecture

### LLM Integration Patterns
- **Multi-provider support**: Unified interface in `backend/python/app/utils/aimodels.py` supporting OpenAI, Anthropic, Gemini, Cohere, etc.
- **Streaming responses**: Server-sent events (SSE) implementation in `backend/python/app/utils/streaming.py`
- **Model-specific optimizations**: Provider-specific configurations and message formatting
- **Structured output**: Pydantic models for consistent response schemas

### Frontend State Management
- **Redux Toolkit**: Global state for authentication and user data
- **Streaming Manager**: Singleton class managing real-time chat state across conversations
- **React Query (SWR)**: Server state management for API calls
- **Component isolation**: Each major feature (chat, knowledge base, settings) has isolated state

### Authentication & Authorization
- **Multi-provider auth**: JWT, Google OAuth, Microsoft Azure AD, SAML SSO
- **Role-based access**: Admin, user, and organization-level permissions
- **Source-level security**: Document access controlled by original platform permissions

### Document Processing Pipeline
1. **Connector ingestion**: Platform-specific APIs pull documents with metadata
2. **Format detection**: MIME type analysis and appropriate parser selection
3. **Content extraction**: Text extraction with structure preservation (headings, lists, tables)
4. **Chunking strategy**: Semantic chunking with overlap for context preservation
5. **Embedding generation**: Configurable embedding models with fallback support
6. **Metadata enrichment**: Source tracking, permissions, and relationship mapping

### Real-time Features
- **WebSocket connections**: Socket.io for live updates and notifications
- **SSE streaming**: Chat responses streamed in chunks with citation updates
- **Event-driven updates**: Kafka events trigger UI updates for document indexing status

### Conversation & Message Flow
**Critical Data Models:**
- **IConversation**: MongoDB schema in `backend/nodejs/apps/src/modules/enterprise_search/schema/conversation.schema.ts`
- **IMessage**: Embedded documents with strict validation (messageType, content required)
- **ICitation**: Separate collection with metadata linking to ArangoDB records

**Message Processing Pipeline:**
1. **User message**: Added to conversation via `backend/nodejs/apps/src/modules/enterprise_search/controller/es_controller.ts`
2. **AI request**: Forwarded to Python service with conversation history
3. **Streaming response**: SSE events processed and filtered (complete events intercepted)
4. **Response validation**: Multiple fallback layers ensure schema compliance
5. **Citation processing**: Individual saves with error handling
6. **Conversation update**: Transaction-safe with session management

**Key Files for Conversation Logic:**
- `backend/nodejs/apps/src/modules/enterprise_search/utils/utils.ts`: Core message building functions
- `backend/nodejs/apps/src/modules/enterprise_search/controller/es_controller.ts`: Streaming and non-streaming endpoints
- `frontend/src/sections/qna/chatbot/chat-bot.tsx`: Frontend streaming manager and error handling

## Critical Implementation Details

### LLM Provider Specific Issues & Solutions

**Gemini 2.5 Flash Optimizations:**
- Extended timeout settings (120s for Flash models) in `backend/python/app/utils/aimodels.py`
- Enhanced error handling with fallback to non-streaming mode in `backend/python/app/utils/streaming.py`
- Message format adjustments (human/assistant roles instead of system messages) in `backend/python/app/api/routes/chatbot.py`
- Flexible response parsing supporting both JSON and plain text formats
- **Critical**: Response validation and fallback handling in `backend/nodejs/apps/src/modules/enterprise_search/utils/utils.ts`
- **New**: Improved streaming response handling for Gemini 2.5 Flash with better error recovery

**Common LLM Integration Issues:**
- **Response format validation**: The `buildAIResponseMessage` function handles multiple response formats and ensures schema compliance
- **Citation processing failures**: Individual citation saves are wrapped with error handling to prevent conversation save failures
- **Confidence level mapping**: Ensures LLM confidence values match MongoDB schema requirements ('Very High', 'High', 'Medium', 'Low', 'Unknown')
- **Streaming connection timeouts**: Frontend implements 30-second connection timeouts with graceful fallback

### Security Considerations
- **No secrets in code**: All API keys and credentials via environment variables
- **Input sanitization**: DOMPurify for markdown rendering, XSS prevention
- **Access control**: Document-level permissions inherited from source platforms
- **Data isolation**: Organization-level data separation in multi-tenant setup

### Performance Patterns
- **Lazy loading**: Document viewers and large components loaded on demand
- **Caching strategies**: Redis for API responses, browser cache for static assets
- **Parallel processing**: Concurrent document processing and embedding generation
- **Connection pooling**: Database connections optimized for high throughput

### Testing Strategy
- **Frontend**: Component testing with React Testing Library patterns
- **Backend Node.js**: Mocha test suite with Sinon for mocking
- **Python service**: Integration tests for AI pipeline components
- **E2E**: Manual testing workflows for critical user paths

## Environment Configuration

Development requires these key environment variables:
- `JWT_SECRET`: Authentication token signing
- `FRONTEND_PUBLIC_URL`: For CORS and webhook callbacks
- `CONNECTOR_PUBLIC_URL`: For external service integration
- LLM API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.
- Database connections: ArangoDB, Redis, Qdrant endpoints

Refer to `env.template` files in each service directory for complete configuration options.

## Debugging & Troubleshooting

### Common Issues & Solutions

**"Failed to save AI response" Error:**
- Check MongoDB schema validation in conversation.schema.ts
- Verify confidence values match allowed enum values
- Examine buildAIResponseMessage function for format compatibility
- Review logs for citation processing failures

**Streaming Connection Issues:**
- Frontend timeout handling in chat-bot.tsx (30s connection timeout)
- Backend SSE implementation filters 'complete' events before forwarding
- AbortController cleanup on client disconnect

**LLM Response Format Issues:**
- Response validation in `backend/python/app/utils/streaming.py`
- Flexible parsing handles both JSON and plain text
- Fallback mechanisms in utils.ts ensure schema compliance

### Development Workflow
1. **Backend changes**: Use Docker containers for Python service (no local pip setup)
2. **Frontend changes**: Standard React development with hot reload
3. **Integration testing**: Full docker-compose stack required for end-to-end testing
4. **Schema changes**: Update both TypeScript interfaces and MongoDB schemas

### Key Configuration Files
- `backend/python/app/utils/aimodels.py`: LLM provider configurations and model mappings
- `backend/nodejs/apps/src/modules/enterprise_search/schema/`: MongoDB schemas for conversations and messages
- `deployment/docker-compose/`: Development and production Docker environments
- `env.template` files: Environment variable templates in each service directory
- `frontend/src/config-global.ts`: Frontend configuration constants
- `backend/python/pyproject.toml`: Python dependencies and build configuration

### Recent Dependency Updates
**Python Service (pyproject.toml)**:
- **LangChain Ecosystem**: Updated to latest versions (langchain 0.3.19, langgraph 0.3.34)
- **New LLM Providers**: Added xAI integration (langchain-xai 0.2.4)
- **Enhanced Embeddings**: Added Voyage AI and JinaAI support
- **Document Processing**: Upgraded to Docling 2.25.1 for better PDF/document parsing
- **Vector Search**: Qdrant client 1.13.1 with improved performance

**Node.js Service (package.json)**:
- **Enhanced Authentication**: Updated Azure MSAL, SAML, and OAuth implementations
- **Better Error Handling**: Improved with latest axios-retry and async-mutex
- **Database Drivers**: Updated MongoDB (6.14.2) and ArangoDB (10.1.1) drivers
- **Security**: Latest helmet (8.0.0) and crypto implementations

## Project Structure Patterns

### Frontend Architecture
- **src/sections/**: Feature-based organization (qna, knowledgebase, accountdetails)
- **src/components/**: Reusable UI components with TypeScript interfaces
- **src/hooks/**: Custom React hooks for shared logic
- **src/store/**: Redux Toolkit slices for global state
- **src/types/**: TypeScript type definitions for API interfaces

### Backend Python Structure
- **app/api/routes/**: FastAPI route handlers (chatbot.py, search.py, records.py)
- **app/modules/**: Business logic modules (indexing, retrieval, streaming)
- **app/utils/**: Utility functions (aimodels.py, streaming.py, citations.py)
- **app/connectors/**: Source system integrations (Google Drive, Gmail, etc.)
- **app/models/**: Pydantic models and database schemas

### Backend Node.js Structure
- **src/modules/enterprise_search/**: Main search and chat functionality
- **src/modules/enterprise_search/controller/**: API controllers (es_controller.ts)
- **src/modules/enterprise_search/schema/**: Mongoose schemas (conversation.schema.ts)
- **src/modules/enterprise_search/utils/**: Helper functions (utils.ts)

## Testing and Development Workflow

### Frontend Testing
```bash
cd frontend
# Component testing with React Testing Library (when available)
yarn test              # Run tests
yarn test:watch        # Watch mode
```

### Backend Testing
```bash
cd backend/nodejs/apps
npm test               # Mocha tests with Sinon mocking
npm run test:watch     # Watch mode
```

### Development Workflow
1. **Environment Setup**: Copy env.template files and configure API keys
2. **Docker Development**: Use docker-compose.dev.yml for full stack development
3. **Service Development**: Individual services can be developed outside Docker for faster iteration
4. **Database Management**: ArangoDB and MongoDB GUIs available on respective ports
5. **Log Monitoring**: Use docker compose logs for debugging across services

## Migration & Schema Evolution

### Aircraft Metadata Migration
Recent system evolution from department-based to aircraft-based metadata extraction:

**Migration Scripts**:
```bash
cd backend/python

# Database schema migration (dry run first)
python app/scripts/migrate_departments_to_aircraft.py --dry-run
python app/scripts/migrate_departments_to_aircraft.py

# Document reindexing with aircraft metadata
python app/scripts/reindex_documents_aircraft.py --dry-run
python app/scripts/reindex_documents_aircraft.py --batch-size 20
```

**What Changed**:
- **Data Model**: `Departments` interface replaced with `Aircraft` interface
- **Extraction Logic**: Enhanced domain extraction in `backend/python/app/modules/extraction/`
- **Database Schema**: ArangoDB collections migrated from departments to aircraft
- **Frontend Types**: New `aircraft.ts` type definitions with backward compatibility

**Migration Validation**:
- Check aircraft collection has 42+ aircraft types
- Verify documents have populated aircraft metadata
- Confirm old department collections are removed
- Monitor extraction performance post-migration