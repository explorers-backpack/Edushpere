# API Routes Summary

## User Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/user/register` | Register new user |
| POST | `/api/user/login` | Login and get JWT token |
| POST | `/api/user/logout` | Logout current user |
| GET | `/api/user/me` | Get current user info |

## Profile Agent
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/profile/generate` | Generate learning profile |
| GET | `/api/profile/current` | Get current profile |
| PUT | `/api/profile/update` | Update profile |

## Path Agent
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/path/generate` | Generate learning path |
| GET | `/api/path/current` | Get active learning path |
| GET | `/api/path/` | List all paths |

## Resource Agent
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resource/generate` | Generate resources |
| GET | `/api/resource/list` | List resources |
| GET | `/api/resource/{id}` | Get resource details |

## Evaluate Agent
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/evaluate/submit` | Submit for evaluation |
| GET | `/api/evaluate/result/{id}` | Get result |
| GET | `/api/evaluate/history` | Get evaluation history |

## Tutor Agent
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tutor/chat` | Send chat message |
| GET | `/api/tutor/history` | Get chat history |
