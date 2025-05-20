# Banking API Application

A comprehensive full-stack banking platform built using FastAPI and modern frontend frameworks (React, Svelte, Vue). This system facilitates user authentication, secure financial transactions, and integration with real-world banking APIs using proper certification and authorization protocols.

## Features

- User registration, login, and JWT-based authentication
- Bank account generation with valid routing/account numbers
- Initial balance of $40 for new accounts
- Deposit and withdrawal functionalities
- Full transaction history for each account
- Secure API endpoints with OAuth2 + PKCE for frontend integration
- Modern frontend support (React, Svelte, Vue)
- Swagger/OpenAPI documentation
- Password hashing using bcrypt
- Environment-based configuration (.env)
- Role-based access control (admin, user)
- Audit logs and security event tracking

## Compliance & Certifications

- HTTPS/TLS encryption
- OAuth2 with client credentials and authorization code flow
- PCI-DSS awareness for handling financial data
- MFA integration capabilities (email/SMS-based 2FA)
- Audit trails and secure logging
- CSRF, CORS, and XSS protection best practices
- Integration-ready with banking APIs using Open Finance standards (e.g., Plaid, Yodlee)

## Project Structure

```
project/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── crud.py
│   ├── auth.py
│   └── routes/
│       ├── users.py
│       ├── transactions.py
│       └── auth.py
├── react-app/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── vue-app/
│   └── ...
├── svelte-app/
│   └── ...
├── html/           # React build output (SPA)
│   ├── index.html
│   ├── manifest.json
│   ├── service-worker.js
│   └── assets/
├── requirements.txt
├── .env
└── README.md
```

## Setup

1. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate  # Windows
   ```

2. **Install backend dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   Create `.env` with the following:
   ```env
   DATABASE_URL=sqlite:///./bank.db
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   OAUTH_CLIENT_ID=...
   OAUTH_CLIENT_SECRET=...
   REDIRECT_URI=http://localhost:8080/callback
   ```

4. **Initialize DB**:
   ```bash
   alembic upgrade head
   ```

5. **Run FastAPI backend**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Run frontend (example React)**:
   ```bash
   cd frontend/react
   npm install
   npm start
   ```

## Testing

### Backend (FastAPI)
- Run all tests:
  ```bash
  pytest app/
  ```
- Or with unittest:
  ```bash
  python -m unittest discover app/
  ```

### Frontend (React)
- From `react-app/`:
  ```bash
  npm test
  ```
- For coverage:
  ```bash
  npm run test -- --coverage
  ```

## Implementation Notes
- Main backend code is in `app/`.
- Main frontend code is in `react-app/` (SPA, PWA-enabled).
- All new features and bugfixes should be covered by tests.
- API endpoints are consumed via the centralized API service in `react-app/src/api.js`.
- For local development, ensure `.env` contains all required variables (see example above).

## Usage Workflow

### Account Creation
- **Frontend**: user registers with name, email, password
- **Backend**: hashes password, creates user + default account, returns JWT token

### Login/Auth
- **Frontend**: form POSTs to `/auth/token`
- **Backend**: verifies credentials, returns JWT access + refresh tokens
- **Frontend**: stores token securely (HttpOnly cookie/localStorage)

### Deposit/Withdraw
- **Frontend**: sends `POST` to `/users/{user_id}/deposit` or `/withdraw` with token
- **Backend**: authenticates JWT, validates amount, updates balance, logs transaction

### Transaction History
- **Frontend**: fetches from `/accounts/{account_id}/transactions`
- **Backend**: returns structured JSON list with timestamps, type, amount

### Secure Auth Flow
- Uses OAuth2PasswordBearer for token auth
- Optional frontend uses OAuth2 Authorization Code Flow w/ PKCE
- Supports client credentials for server-to-server access

## Key API Endpoints

- `POST /users/`: Register user
- `POST /auth/token`: Get access token
- `GET /users/{user_id}`: Fetch user profile
- `POST /users/{user_id}/deposit`: Deposit funds
- `POST /users/{user_id}/withdraw`: Withdraw funds
- `GET /users/{user_id}/account`: Get account details
- `GET /accounts/{account_id}/transactions`: View history

## Certifications and Authorizations

- **OAuth2 Authorization Code Flow** for banking-level security
- **JWT tokens** w/ expiry and rotation
- **TLS Certificate Handling** (using FastAPI middleware or reverse proxy)
- **Financial Data Protection**:
  - Token encryption
  - Masked account info display
  - Session timeouts & inactivity logouts

## Future Features

- Bank-to-bank transfers
- Reconciliation dashboard
- Admin control panel
- ACH integration
- Biometric auth support (via WebAuthn)
- Frontend widgets for financial insights
- WebSocket live updates for transactions