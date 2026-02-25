# ServiceNow Server CRUD - Quick Reference

## 📋 ServiceNow Parameters Added

| Parameter | Type | Required | Purpose | Example |
|-----------|------|----------|---------|---------|
| `connection_name` | String | **Yes** | Identifier for this connection | `"prod_connection"` |
| `instance_url` | String | **Yes** | ServiceNow instance URL | `"https://dev12345.service-now.com"` |
| `username` | String | **Yes** | ServiceNow login username | `"admin@example.com"` |
| `password` | String | **Yes** | ServiceNow login password | `"SecurePassword123!"` |

---

## 🚀 Quick Start Examples

### Create Server with ServiceNow Details
```bash
curl -X POST "http://localhost:5000/api/servers/create" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "60d5ec49c1234abcd5678900",
    "name": "My ServiceNow Server",
    "hostname": "servicenow.example.com",
    "port": 443,
    "connection_name": "my_connection",
    "instance_url": "https://myinstance.service-now.com",
    "username": "myuser@company.com",
    "password": "MyPassword123!",
    "status": "running"
  }'
```

### Get Server with All Details
```bash
curl -X GET "http://localhost:5000/api/servers/699a01b62c951759d08d1e17"
```

### Update ServiceNow Credentials
```bash
curl -X PUT "http://localhost:5000/api/servers/699a01b62c951759d08d1e17" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser@company.com",
    "password": "NewPassword456!"
  }'
```

### List All Servers with ServiceNow Config
```bash
curl -X GET "http://localhost:5000/api/servers/user/60d5ec49c1234abcd5678900"
```

---

## 📊 Test Run Summary

**Date:** February 22, 2026
**Status:** ✅ ALL TESTS PASSED

### Tests Executed
- ✓ Created 3 servers with ServiceNow parameters
- ✓ Retrieved individual servers
- ✓ Retrieved all servers for a user (3 servers)
- ✓ Retrieved all servers in system
- ✓ Updated ServiceNow parameters on a server
- ✓ Verified updates persisted
- ✓ Deleted servers
- ✓ Verified deletions
- ✓ Validated response structure

### Sample Test Data
```json
{
  "Production ServiceNow Server": {
    "connection_name": "prod_connection",
    "instance_url": "https://dev12345.service-now.com",
    "username": "admin@example.com"
  },
  "Development ServiceNow Server": {
    "connection_name": "dev_connection",
    "instance_url": "https://dev67890.service-now.com",
    "username": "dev_user@example.com"
  },
  "Staging ServiceNow Server": {
    "connection_name": "staging_connection",
    "instance_url": "https://staging12345.service-now.com",
    "username": "staging_user@example.com"
  }
}
```

---

## 🔍 Response Fields

When retrieving a server, you get:

```json
{
  "id": "699a01b62c951759d08d1e17",
  "user_id": "60d5ec49c1234abcd5678900",
  "name": "Production ServiceNow Server",
  "hostname": "servicenow-prod.example.com",
  "port": 443,
  "status": "running",
  "connection_name": "prod_connection",
  "instance_url": "https://dev12345.service-now.com",
  "username": "admin@example.com",
  "password": "SecurePassword123!",
  "created_at": "2026-02-21 19:04:22.180000",
  "updated_at": "2026-02-21 19:04:22.180000"
}
```

---

## 📍 All Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/servers/create` | Create server with ServiceNow config |
| `GET` | `/api/servers/{server_id}` | Get server details |
| `GET` | `/api/servers/user/{user_id}` | List user's servers |
| `GET` | `/api/servers/` | List all servers |
| `PUT` | `/api/servers/{server_id}` | Update server (including credentials) |
| `DELETE` | `/api/servers/{server_id}` | Delete server |
| `DELETE` | `/api/servers/user/{user_id}` | Delete all user's servers |

---

## 🧪 Test Script

Run the complete test suite:
```bash
python test_servers_servicenow.py
```

Expected output includes:
- Server creation tests
- Retrieval with full details
- Update verification
- Deletion verification
- Response structure validation

---

## 📖 Documentation Files

- **SERVICENOW_SERVERS.md** - Complete API documentation
- **test_servers_servicenow.py** - Full test suite with ServiceNow parameters
- **SERVERS.md** - Original server CRUD documentation (updated)

---

## ✨ Key Features

✅ Store ServiceNow connection details with servers
✅ Update credentials without affecting other fields
✅ Retrieve all ServiceNow config for a server
✅ Organize multiple ServiceNow instances per user
✅ Full CRUD support with validation
✅ Proper error handling

---

## 🎯 Real-World Use Cases

1. **Multi-Environment Setup**
   - Store different ServiceNow instances (dev, test, prod)
   - Manage credentials for each environment

2. **Team Collaboration**
   - Multiple users can manage their own ServiceNow servers
   - Centralized credential storage

3. **Integration Management**
   - Store connection configs for automation
   - Update credentials without code changes

4. **Audit Trail**
   - Track when servers were created/updated
   - Maintain timestamp history

---

## 🔐 Security Considerations

Current implementation stores passwords in plaintext. For production:

```python
# TODO: Implement encryption
from cryptography.fernet import Fernet

# Encrypt before storing
encrypted = encrypt_password(password)

# Decrypt when needed
decrypted = decrypt_password(encrypted)
```

---

## 📞 Support

**All endpoints tested and working.** Access interactive docs at:
```
http://localhost:5000/docs
```

Try out any endpoint directly with Swagger UI!
