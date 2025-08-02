# PipesHub AI - User Experience & Navigation Flow

## Overview

PipesHub AI is a knowledge management and AI assistant platform that helps users manage documents, search knowledge bases, and interact with an AI chatbot. The application supports both individual users and business/organization accounts with different feature sets and navigation paths.

## Entry Points & Authentication

### 1. Sign-In Flow (`/auth/sign-in`)
Users can authenticate using multiple methods:
- **Email + Password**
- **Email + OTP (One-Time Password)**
- **Google OAuth**
- **Microsoft OAuth**
- **Azure AD**
- **SAML SSO** (for configured organizations)

### 2. Sign-Up Flow (`/auth/sign-up`)
New users create accounts with:
- Account type selection (Individual or Business/Organization)
- Profile setup
- Authentication method configuration

### 3. Password Reset (`/reset-password`)
Self-service password recovery flow

## Post-Authentication Navigation

After successful authentication, users are directed to the main dashboard (`/`) which serves as the **AI Assistant/Chatbot** interface.

## Main Application Areas

### 1. AI Assistant (Home - `/`)
- **Primary landing page after sign-in**
- Interactive chatbot interface for Q&A
- Conversation history (`/:conversationId`)
- Document references and citations
- Real-time AI-powered responses

### 2. Knowledge Base (`/knowledge-base`)
Two main sections:

#### Knowledge Base Details (`/knowledge-base/details`)
- View all uploaded documents
- Document management
- File organization
- Upload new documents

#### Knowledge Search (`/knowledge-base/search`)
- Advanced search across all documents
- Filter and sort capabilities
- Preview search results
- Access document details

### 3. Record/Document Details (`/record/:recordId`)
- Individual document viewer
- PDF highlighting and annotations
- Text extraction display
- Document metadata

## Account Management

The account section branches based on user type:

### For Business/Organization Accounts

#### Company Profile & Settings
- **Company Profile** (`/account/company-settings/profile`)
- **Personal Profile** (`/account/company-settings/personal-profile`)

#### Admin-Only Features (if user is admin)
- **Users & Groups Management**
  - Users list (`/account/company-settings/users`)
  - Groups list (`/account/company-settings/groups`)
  - User profile details (`/account/company-settings/user-profile/:id`)
  - Group details (`/account/company-settings/groups/:id`)
  - Invitations (`/account/company-settings/invites`)

- **Settings** (`/account/company-settings/settings/`)
  - Authentication settings (`/authentication`)
  - SAML SSO configuration (`/authentication/saml`)
  - Connector settings (`/connector`)
  - Google Workspace configuration (`/connector/googleWorkspace`)
  - Services settings (`/services`)
  - AI Models configuration (`/ai-models`)

### For Individual Accounts

#### Profile & Settings
- **My Profile** (`/account/individual/profile`)
- **Settings** (`/account/individual/settings/`)
  - Authentication settings (`/authentication`)
  - Connector settings (`/connector`)
  - Google Workspace configuration (`/connector/googleWorkspace`)
  - Services settings (`/services`)
  - AI Models configuration (`/ai-models`)

## Navigation Menu Structure

### Sidebar Navigation
1. **Overview Section**
   - Assistant (Home/Chatbot)
   - Knowledge Base
   - Knowledge Search

2. **Administration Section** (Business Admin only)
   - Connector Settings

3. **Settings Section** (Individual users)
   - Connector Settings

### Account Menu (Top Right)
- **Business Users:**
  - Company Profile
  - My Profile
  - Settings (Admin only)

- **Individual Users:**
  - My Profile
  - Settings

## User Journey Examples

### Individual User Journey
1. Sign in → AI Assistant
2. Upload documents via Knowledge Base
3. Search and interact with documents
4. Configure personal settings and connectors
5. Use AI chat for document Q&A

### Business Admin Journey
1. Sign in → AI Assistant
2. Set up company profile
3. Configure authentication (SAML/SSO)
4. Invite team members
5. Create and manage user groups
6. Configure connectors and AI models
7. Monitor team usage

### Business Non-Admin Journey
1. Sign in → AI Assistant
2. Access shared knowledge base
3. Use AI chat for document Q&A
4. View company profile
5. Manage personal profile only

## Error Pages
- **404** - Page not found
- **403** - Access forbidden
- **500** - Server error
- **Maintenance** - System maintenance page

## Guards & Access Control

### Authentication Guards
- **GuestGuard**: Prevents authenticated users from accessing auth pages
- **AuthGuard**: Protects authenticated routes
- **AdminGuard**: Restricts access to admin features
- **FullNameGuard**: Ensures user profile completion

### Account Type Guards
- **BusinessRouteGuard**: Business/Organization only routes
- **IndividualRouteGuard**: Individual account only routes
- **AdminRouteGuard**: Business admin only routes

## Key Features by User Type

### All Users
- AI-powered chatbot
- Document upload and management
- Knowledge base search
- Personal profile management

### Business/Organization Users
- Company profile management
- Multi-user support
- Shared knowledge bases

### Business Admins (Additional)
- User and group management
- Authentication configuration (SAML SSO)
- Connector configuration
- AI model selection
- Service settings

### Individual Users
- Personal knowledge base
- Individual connector settings
- Simplified settings interface