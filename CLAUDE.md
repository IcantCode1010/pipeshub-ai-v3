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

### AI Pipeline Architecture
The AI service follows a retrieval-augmented generation (RAG) pattern:
1. **Ingestion**: Documents from connectors � parsing � chunking � embedding
2. **Indexing**: Vector storage in Qdrant + metadata in ArangoDB
3. **Retrieval**: Hybrid search (semantic + keyword) � reranking � context assembly
4. **Generation**: LLM inference with streaming responses and citation tracking

## Development Commands

### Frontend (React/TypeScript)
```bash
cd frontend
yarn dev                # Development server
yarn build             # Production build
yarn lint              # ESLint check
yarn lint:fix          # Fix linting issues
yarn fm:check          # Prettier format check
yarn fm:fix            # Fix formatting
```

### Backend Python (AI Service)
```bash
cd backend/python
# No pip/poetry commands - uses Docker
ruff check .           # Lint check
ruff format .          # Format code
```

### Backend Node.js
```bash
cd backend/nodejs/apps
npm run dev            # Development with nodemon
npm run build          # TypeScript compilation
npm run lint           # ESLint check
npm run format         # Prettier formatting
npm test               # Run Mocha tests
```

### Docker Development
```bash
cd deployment/docker-compose

# Development build (with source mounting)
docker compose -f docker-compose.dev.yml -p pipeshub-ai up --build -d

# Production deployment
docker compose -f docker-compose.prod.yml -p pipeshub-ai up -d

# Stop services
docker compose -f docker-compose.dev.yml -p pipeshub-ai down
```

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
- `backend/python/app/utils/aimodels.py`: LLM provider configurations
- `backend/nodejs/apps/src/modules/enterprise_search/schema/`: MongoDB schemas
- `deployment/docker-compose/`: Development and production environments