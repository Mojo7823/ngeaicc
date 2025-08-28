# **AI Testing Standard Solution - Complete Project Documentation**

## **Project Overview**
Develop an AI testing standard platform based on Common Criteria, targeting AI-integrated devices with CVE-based test cases and intelligent recommendations.

---

## **Technical Architecture**

### **Technology Stack**
- **Frontend**: Vue.js
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL + pgvector
- **AI Model**: Llama3 (local API)
- **Deployment**: No Docker initially (due to USB/serial port requirements)

### **Architecture Flow**
```
Frontend (Vue.js) ↔ Backend (FastAPI) ↔ Local AI API (Llama3)
                                    ↕
                            PostgreSQL + pgvector
```

---

## **Core Features**

### **1. Testing Approach**
- **Dual Mode**: API-based testing + Physical device testing (USB/serial)
- **CVE-Based**: Real-world vulnerability test cases
- **Custom Tests**: User-defined test creation capability
- **Framework**: MITRE ATT&CK/ATLAS integration

### **2. Common Criteria Implementation**
- **Scope**: All EAL levels (EAL1-7)
- **Forms**: Online CC-compliant device profiling
- **Output**: Professional SAR documentation

### **3. AI Integration (RAG)**
- **Test Recommendations**: AI suggests relevant tests based on device profile
- **Smart Assistance**: "Autocomplete for testing" throughout platform
- **Report Generation**: AI-enhanced analysis and insights
- **Human-in-the-Loop**: User approval required for AI recommendations

---

## **MVP Development Plan**

### **Phase 1: Foundation**
- Basic FastAPI ↔ Vue.js communication
- Simple authentication (login page)
- Database setup with basic schema

### **Phase 2: Single Test + Report**
- One working test case (API-based)
- Basic report generation (Word/PDF export)
- Proof of concept validation

### **Phase 3: AI Integration** (Future)
- Llama3 integration
- RAG implementation (chunking, searching, indexing module)
- Smart recommendations

---

## **Key Design Decisions**
- **No Docker initially** (hardware access complexity)
- **Local AI API** (all AI interactions via own endpoints)
- **CVE-driven testing** (real vulnerability focus)
- **Human approval required** (no automatic test execution)
- **Exportable reports** (Word document format)

---

## **Architecture Diagrams**

### **High-Level Architecture**
```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Vue.js Frontend]
        AUTH[Authentication]
        FORMS[CC Forms]
        DASH[Dashboard]
    end
    
    subgraph "Backend Layer"
        API[FastAPI Backend]
        TEST[Test Execution Module]
        AI[AI/RAG Module]
        REPORT[Report Generator]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL + pgvector)]
        LLAMA[Llama3 Local API]
    end
    
    subgraph "External Interfaces"
        CVE[CVE Database]
        DEVICE[Physical Devices<br/>USB/Serial]
        VENDOR[Vendor APIs]
    end
    
    UI --> API
    AUTH --> API
    FORMS --> API
    DASH --> API
    
    API --> TEST
    API --> AI
    API --> REPORT
    
    TEST --> DB
    AI --> DB
    AI --> LLAMA
    REPORT --> DB
    
    TEST --> DEVICE
    TEST --> VENDOR
    AI --> CVE
```

### **Data Flow**
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant AI_Module
    participant Database
    participant Test_Engine
    participant Device_API
    
    User->>Frontend: Fill CC Device Profile
    Frontend->>Backend: Submit Profile Data
    Backend->>Database: Store Device Profile
    Backend->>AI_Module: Request Test Recommendations
    AI_Module->>Database: Query Similar Profiles (RAG)
    AI_Module->>Backend: Return Suggested Tests
    Backend->>Frontend: Display Recommendations
    Frontend->>User: Show AI Suggestions
    User->>Frontend: Approve Selected Tests
    Frontend->>Backend: Execute Approved Tests
    Backend->>Test_Engine: Run Test Cases
    Test_Engine->>Device_API: Execute Tests
    Device_API-->>Test_Engine: Test Results
    Test_Engine->>Database: Store Results
    Backend->>AI_Module: Generate Report Insights
    AI_Module->>Backend: Return Analysis
    Backend->>Frontend: Display Results
    Frontend->>User: Show Report + Export Option
```

### **Database Schema**
```mermaid
erDiagram
    DEVICE_PROFILES {
        uuid id
        string name
        string device_type
        string ai_model_type
        json cc_evaluation_level
        text description
        timestamp created_at
        vector embedding
    }
    
    TEST_DEFINITIONS {
        uuid id
        string cve_id
        string test_name
        string mitre_technique
        json test_parameters
        string difficulty_level
        text description
        vector embedding
    }
    
    TEST_EXECUTIONS {
        uuid id
        uuid device_profile_id
        uuid test_definition_id
        string status
        json results
        timestamp executed_at
        text ai_analysis
    }
    
    REPORTS {
        uuid id
        uuid device_profile_id
        string report_type
        json test_summary
        text ai_insights
        string export_format
        timestamp generated_at
    }
    
    DEVICE_PROFILES ||--o{ TEST_EXECUTIONS : "tested_with"
    TEST_DEFINITIONS ||--o{ TEST_EXECUTIONS : "defines"
    DEVICE_PROFILES ||--o{ REPORTS : "generates"
    TEST_EXECUTIONS ||--o{ REPORTS : "includes"
```
