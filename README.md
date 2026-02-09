# Climate Resilience Platform (Soacha)

## **1. LOGICAL VIEW: Alert Generation and Intervention Lifecycle State Diagram**

```mermaid
---
config:
  theme: neo
  look: neo
  layout: elk
---
stateDiagram
  direction TB
  [*] --> MonitoringWeather
  MonitoringWeather --> AnalyzingConditions:Weather Data Received
  AnalyzingConditions --> RiskAssessment:Data Valid
  AnalyzingConditions --> DiscardingData:Data Invalid
  DiscardingData --> MonitoringWeather
  RiskAssessment --> LowRisk:Risk < 30%
  RiskAssessment --> MediumRisk:30% ≤ Risk < 60%
  RiskAssessment --> HighRisk:60% ≤ Risk < 80%
  RiskAssessment --> CriticalRisk:Risk ≥ 80%
  LowRisk --> MonitoringWeather:Continue monitoring
  MediumRisk --> NotifyStakeholders:Issue Yellow Alert
  HighRisk --> NotifyStakeholders:Issue Orange Alert
  CriticalRisk --> NotifyStakeholders:Issue Red Alert
  NotifyStakeholders --> AlertActive:Notifications Sent
  AlertActive --> TrackingEscalation:Conditions Monitored
  TrackingEscalation --> EscalationNeeded:Risk Increased
  TrackingEscalation --> DeescalationNeeded:Risk Decreased
  TrackingEscalation --> EventOccurred:Disaster Happens
  EscalationNeeded --> NotifyStakeholders
  DeescalationNeeded --> AlertResolved:Risk < 30%
  EventOccurred --> DisasterResponse:Activate Emergency Protocol
  AlertResolved --> MonitoringWeather
  DisasterResponse --> ImpactAssessment:Event Duration Complete
  ImpactAssessment --> RecoveryTracking:Assess Damage
  RecoveryTracking --> MonitoringWeather
  [*] --> Planned
  Planned --> Approved:Leadership Review
  Planned --> Rejected:Insufficient Funds
  Rejected --> [*]
  Approved --> Active:Start Date
  Active --> OnTrack:Achieving Goals
  Active --> AtRisk:Behind Schedule
  OnTrack --> Completed:All Beneficiaries Reached
  AtRisk --> Adjustment:Resource Reallocation
  Adjustment --> OnTrack:Resumed Progress
  Adjustment --> Suspended:Critical Issues
  Suspended --> Resumed:Issues Resolved
  Resumed --> OnTrack
  Completed --> Evaluation:End Date
  Evaluation --> Successful:Goals Met
  Evaluation --> PartialSuccess:Partial Goals Met
  Successful --> [*]
  PartialSuccess --> [*]
```

---

## **2. PROCESS VIEW: Activity & Sequence Diagrams**

### **2.1 Climate Alert Generation, Intervention Effectiveness Analysis and Zone Risk Recalculation Activity Diagram**

```mermaid
---
config:
  theme: neo
  look: neo
---
flowchart TB
 subgraph subGraph0["Climate Alert Generation"]
        FetchWeather["🌐 Fetch Weather Data<br>from IDEAM/OpenWeather"]
        Start(["Monthly Analysis Task"])
        ValidateData{"Data Valid?"}
        LogError["Log Error & Retry"]
        EnrichData["Enrich with Historical Data<br>&amp; AVCA Assessment"]
        CalculateRisk["Calculate Risk Score<br>by Zone"]
        AssessFlood["Assess Flood Risk:<br>Precipitation + Drainage"]
        AssessTemp["Assess Heat Risk:<br>Temp + Vulnerable Population"]
        QueryZones["Query Affected Zones<br>Risk &gt; Threshold"]
        GetPopulation["Get Population Count<br>by Zone &amp; Vulnerability"]
        GenerateAlerts["Generate Alert Objects<br>for Each At-Risk Zone"]
        StoreAlerts["Store Alerts in Database<br>&amp; Mark as Active"]
        CheckEscalation{"Alert Level<br>Changed?"}
        NotifyLeaders["🔔 Notify Community Leaders<br>via SMS/App/Email"]
        NotifyVolunteers["🔔 Notify Volunteers<br>via App Only"]
        ClearOldAlerts["Clear Previous Alerts<br>from System"]
        UpdateDashboard["⚡ Update Dashboard<br>Real-time Map Highlight"]
        LogMetrics["Log Metrics:<br>Response Time, Accuracy"]
        End(["Analysis Complete"])
  end
 subgraph subGraph1["Intervention Effectiveness Analysis"]
        GetInterventions["Retrieve Active<br>Interventions"]
        GetTargetPop["Get Target Population<br>per Intervention"]
        GetBeneficiaries["Get Actual Beneficiaries<br>from Field Data"]
        CalculateReach["Calculate Reach Rate<br>= Actual / Target"]
        GetEvents["Retrieve Climate Events<br>in Intervention Period"]
        GetAffected["Get Affected Population<br>per Event &amp; Zone"]
        CrossReference["Cross-reference:<br>Beneficiaries ∩ Affected"]
        CalculateProtection["Calculate Protection Rate<br>= Beneficiaries in Event / Total Affected"]
        AnalyzeCohesion["Analyze Cohesion Impact:<br>Response time improvement"]
        GenerateMetrics["Generate Metrics:<br>- Reach (%)<br>- Protection (%)<br>- Cost/Person<br>- Satisfaction (survey)"]
        CreateReport["Create Intervention<br>Effectiveness Report"]
        StoreResults["Store in Database<br>&amp; Cache"]
        NotifyStakeholders["Notify Program Manager<br>via Email &amp; Dashboard"]
  end
 subgraph Input["Input Data Sources"]
        A["IDEAM Climate API<br>(daily)"]
        B["Building Assessments<br>(AVCA monthly)"]
        C["Historical Events<br>(database)"]
        D["Community Feedback<br>(reports)"]
  end
 subgraph Calculate["Risk Calculation"]
        E["Aggregate Climate Data<br>30-day window"]
        F["Load Infrastructure<br>Vulnerabilities"]
        G["Analyze Historical<br>Patterns"]
        H["Apply ML Model<br>Prediction"]
  end
 subgraph Output["Risk Outputs"]
        I["Update Zone Risk Scores<br>in Database"]
        J["Generate Alerts if<br>Risk Escalates"]
        K["Update Dashboard<br>Heat Map"]
  end
 subgraph subGraph5["Zone Risk Recalculation Process"]
        Input
        Calculate
        Output
  end
    Start --> FetchWeather & GetInterventions
    FetchWeather --> ValidateData
    ValidateData -- No --> LogError
    LogError --> FetchWeather
    ValidateData -- Yes --> EnrichData
    EnrichData --> CalculateRisk
    CalculateRisk --> AssessFlood
    AssessFlood --> AssessTemp
    AssessTemp --> QueryZones
    QueryZones --> GetPopulation
    GetPopulation --> GenerateAlerts
    GenerateAlerts --> StoreAlerts
    StoreAlerts --> CheckEscalation
    CheckEscalation -- Escalated --> NotifyLeaders
    CheckEscalation -- Same --> NotifyVolunteers
    CheckEscalation -- Deescalated --> ClearOldAlerts
    NotifyLeaders --> UpdateDashboard
    NotifyVolunteers --> UpdateDashboard
    ClearOldAlerts --> UpdateDashboard
    UpdateDashboard --> LogMetrics
    LogMetrics --> End
    GetInterventions --> GetTargetPop
    GetTargetPop --> GetBeneficiaries
    GetBeneficiaries --> CalculateReach
    CalculateReach --> GetEvents
    GetEvents --> GetAffected
    GetAffected --> CrossReference
    CrossReference --> CalculateProtection
    CalculateProtection --> AnalyzeCohesion
    AnalyzeCohesion --> GenerateMetrics
    GenerateMetrics --> CreateReport
    CreateReport --> StoreResults
    StoreResults --> NotifyStakeholders
    NotifyStakeholders --> End
    A --> E
    B --> F
    C --> G
    D --> H
    E --> H
    F --> H
    G --> H
    H --> I
    I --> J & K
```

### **2.2 Population Impact Assessment; Field Data Collection & Reporting Sequence Diagram**

```mermaid
---
config:
  theme: neo
  look: neo
---
sequenceDiagram
    autonumber
    actor Leader as Community Leader
    participant UI as Dashboard UI
    participant DB as Geospatial Database
    participant Analytics as Analytics Engine
    participant Cache as Redis Cache

    actor Volunteer as Volunteer (Field)
    participant Mobile as Mobile App<br/>React Native
    participant LocalDB as Local Storage<br/>SQLite
    participant MainDB as Main Database
    participant API as API Server
    Leader->>UI: Select Event & Zone
    UI->>API: POST /impact-analysis<br/>{eventId, zoneId}
    API->>Cache: Check cached results
    Cache-->>API: Cache Miss
    API->>DB: Query(Buildings in Zone)
    DB-->>API: Return{building[], geometry}
    API->>DB: Query(AVCA interventions<br/>in Zone)
    DB-->>API: Return{familiesLinked}
    API->>DB: Query(Population in<br/>ClimateEvent.affectedZone)
    DB-->>API: Return{totalAffected}
    API->>Analytics: Calculate metrics<br/>{linked, affected, ratio}
    Analytics-->>API: Metrics{<br/>reachRate: 45%<br/>vulnerablePercentage: 62%<br/>}
    API->>Cache: Store results<br/>TTL: 1 hour
    API-->>UI: Return ImpactReport
    UI->>UI: Render charts<br/>& statistics
    UI-->>Leader: Display<br/>• Families affected: 2,340<br/>• Families linked: 1,080<br/>• Reach rate: 46%<br/>
    Leader->>UI: Export Report
    UI->>API: GET /export/pdf<br/>{reportId}
    API-->>UI: Return PDF Stream
    UI-->>Leader: Download impact_2024-02.pdf
    Volunteer->>Mobile: Open Field Report<br/>Offline Mode
    Mobile->>LocalDB: Load cached zone<br/>& building list
    LocalDB-->>Mobile: Return cached data
    Volunteer->>Mobile: Enter Report:<br/>- Building status<br/>- People count<br/>- Damage level<br/>- Photo
    Mobile->>Mobile: Validate input
    Mobile->>LocalDB: Store report<br/>with timestamp
    LocalDB-->>Mobile: Report queued
    Volunteer->>Mobile: Network available?
    Note over Mobile: Check connectivity
    alt Network Available
        Mobile->>API: POST /reports<br/>{reportData, photos}
        API->>MainDB: Insert Report<br/>& attachments
        MainDB-->>API: Report ID: 4527
        API-->>Mobile: Success {reportId}
        Mobile->>LocalDB: Mark uploaded<br/>& archive
    else Offline
        Mobile->>LocalDB: Keep report in<br/>pending queue
        Note over Volunteer: Will auto-sync<br/>when connected
    end
    Volunteer->>Mobile: Continue field work
```

---

## **3. DEVELOPMENT VIEW: Component Architecture and Package (Module dependencies) Diagram**

```mermaid
---
config:
  layout: elk
  theme: neo
  look: neo
---
flowchart LR
subgraph subGraph123["Component Architecture"]
 subgraph subGraph0["Presentation Layer"]
        WebUI["🖥️ Web UI Component<br>React + TypeScript"]
        MobileUI["📱 Mobile UI Component<br>React Native"]
        Widgets["UI Widgets Library<br>Maps, Charts, Forms"]
  end
 subgraph subGraph1["API Layer"]
        GeoAPI["Geo API<br>Express/FastAPI"]
        AlertAPI["Alert API<br>WebSocket + REST"]
        ReportAPI["Report API<br>File handling"]
  end
 subgraph subGraph2["Business Logic"]
        GeoService["GeoService<br>Spatial queries"]
        AlertService["AlertService<br>Risk calculation"]
        ImpactService["ImpactService<br>Population analysis"]
        AuthService["AuthService<br>JWT tokens"]
  end
 subgraph subGraph3["Data Access Layer"]
        GeoRepo["GeoRepository<br>PostGIS queries"]
        EventRepo["EventRepository<br>CRUD operations"]
        CacheLayer["Cache Layer<br>Redis"]
  end
 subgraph subGraph4["External Integrations"]
        IDEAMAdapter["IDEAM Adapter<br>Weather API"]
        OpenWeatherAdapter["OpenWeather Adapter<br>Fallback data"]
        OSMAdapter["OSM Adapter<br>Map tiles"]
        NotificationAdapter["Notification Adapter<br>SMS/Email/Push"]
  end
 subgraph subGraph5["Data Tier"]
        GeoDatabase["PostgreSQL +<br>PostGIS"]
        TimeSeries["TimescaleDB"]
        FileStorage["S3 / Local<br>Storage"]
  end
  end
    WebUI --> GeoAPI & AlertAPI & ReportAPI
    MobileUI --> GeoAPI & AlertAPI & ReportAPI
    Widgets --> WebUI & MobileUI
    GeoAPI --> AuthService & GeoService
    AlertAPI --> AuthService & AlertService & NotificationAdapter
    ReportAPI --> AuthService & ImpactService
    GeoService --> GeoRepo & CacheLayer & OSMAdapter
    AlertService --> GeoRepo & CacheLayer & IDEAMAdapter & OpenWeatherAdapter
    ImpactService --> EventRepo & CacheLayer & FileStorage
    GeoRepo --> GeoDatabase
    EventRepo --> GeoDatabase & TimeSeries
    CacheLayer --> TimeSeries
    subgraph subGraph124["Module Dependencies"]
     subgraph core["🔧 Core Domain"]
        Domain["domain/<br>• Community<br>• Zone<br>• Building<br>• Person"]
        Models["models/<br>• ClimateEvent<br>• Alert<br>• Assessment"]
  end
 subgraph services["⚙️ Services"]
        GeoSvc["services/geo/<br>• spatial-query<br>• risk-calc"]
        AlertSvc["services/alert/<br>• prediction<br>• notification"]
        ReportSvc["services/report/<br>• impact-calc<br>• export"]
        AuthSvc["services/auth/<br>• jwt<br>• permissions"]
  end
 subgraph infra["🗄️ Infrastructure"]
        DBLayer["db/<br>• postgres-adapter<br>• timescale-adapter"]
        CacheLayer["cache/<br>• redis-adapter"]
        ExternalAPI["external/<br>• ideam-client<br>• osm-client"]
  end
 subgraph api["🌐 API Layer"]
        RESTRoutes["routes/<br>• geo.routes<br>• alert.routes<br>• report.routes"]
        Middleware["middleware/<br>• auth<br>• validation<br>• logging"]
        Handlers["handlers/<br>• request-handler<br>• error-handler"]
  end
 subgraph ui["🎨 UI Layer"]
        Components["components/<br>• map<br>• dashboard<br>• alerts"]
        Pages["pages/<br>• zones<br>• impact<br>• reports"]
        State["state/<br>• redux<br>• selectors"]
  end
 subgraph utils["🛠️ Utilities"]
        Helpers["utils/<br>• geo-helpers<br>• formatters"]
        Validators["validators/<br>• schema<br>• rules"]
        Constants["constants/<br>• risk-levels<br>• messages"]
  end
  end
    core --> services
    services --> infra & utils
    infra --> api
    api --> Middleware
    Middleware --> Handlers
    Handlers --> RESTRoutes
    RESTRoutes --> ui
    ui --> Components
    Components --> State
    State --> Helpers
    Validators --> Handlers
    Constants --> services & ui
subgraph subGraph125["Deployment Package Structure"]
     subgraph Docker["🐳 Docker Containers"]
        API["container: api<br>- Node.js 18<br>- Express<br>- Port 3000"]
        Worker["container: worker<br>- Python 3.10<br>- Celery<br>- ML Models"]
        Web["container: web<br>- React 18<br>- Nginx<br>- Port 80"]
  end
 subgraph DataServices["🗄️ Data Services"]
        PG["PostgreSQL 14<br>+ PostGIS<br>+ TimescaleDB<br>Port 5432"]
        Redis["Redis 7<br>Cache/Queue<br>Port 6379"]
  end
 subgraph Orchestration["⚡ Orchestration"]
        K8s["Kubernetes Cluster<br>- Deployment manager<br>- Auto-scaling<br>- Health checks"]
        Compose["Docker Compose<br>(Development)"]
  end
  end
    API --> PG & Redis
    Worker --> PG & Redis
    Web --> API
    K8s -.-> API & Worker & Web
    Compose -.-> API & Worker & Web
```

---

## **4. PHYSICAL VIEW: Production Deployment Architecture and Development Environment Deployment**

---

## **5. USE CASE VIEW: Scenarios (+1)**

### **5.1 Use Case Diagram**

```mermaid
---
config:
  layout: elk
  theme: neo
  look: neo
---
graph LR
    subgraph Actors["Actors"]
        CommunityLeader["👥 Community Leader"]
        Volunteer["🦸 Volunteer"]
        GovOfficial["🏛️ Government Official"]
        Researcher["🔬 Researcher"]
        System["⚙️ System Background"]
    end
    
    subgraph UseCases["Use Cases"]
        UC1["UC1: Monitor Zone<br/>Risk in Real-time"]
        UC2["UC2: Receive Climate<br/>Alert Notifications"]
        UC3["UC3: Assess Population<br/>Impact"]
        UC4["UC4: Plan Evacuation<br/>Routes"]
        UC5["UC5: Report Field<br/>Damage"]
        UC6["UC6: Export Community<br/>Resilience Report"]
        UC7["UC7: Analyze Intervention<br/>Effectiveness"]
        UC8["UC8: Predict Future<br/>Vulnerable Zones"]
        UC9["UC9: Configure Alert<br/>Thresholds"]
    end
    
    CommunityLeader --> UC1 & UC2 & UC3 & UC4 & UC6
    Volunteer --> UC5 & UC1
    GovOfficial --> UC6 & UC7 & UC8 & UC9
    Researcher --> UC7 & UC8
    System --> UC2 & UC8
```

### **5.2 Detailed Use Case Specifications**

#### **UC1: Monitor Zone Risk in Real-time**

```mermaid
---
config:
  theme: neo
  look: neo
---
graph LR
    A["Community Leader<br/>Opens Dashboard"] --> B["System loads<br/>zone data"]
    B --> C["Display interactive map<br/>with heat layers"]
    C --> D["Leader can:<br/>- Zoom to zone<br/>- View risk score<br/>- See affected population"]
    D --> E{"Want more<br/>details?"}
    E -->|Yes| F["Click on zone<br/>→ View Zone Details Panel"]
    F --> G["Panel shows:<br/>• Risk breakdown<br/>• Buildings count<br/>• Linked vs affected<br/>• Safe routes"]
    E -->|No| H["Continue monitoring"]
    G --> H
    H --> I["Auto-refresh every<br/>5 minutes"]
    I --> J["End use case"]
```

---

#### **UC2: Receive Climate Alert Notifications**

```mermaid
---
config:
  theme: neo
  look: neo
---
graph LR
    A["Weather data<br/>processed hourly"] --> B["System calculates<br/>zone risk scores"]
    B --> C["Any zone exceeds<br/>alert threshold?"]
    C -->|No| D["Continue monitoring<br/>every 60 minutes"]
    C -->|Yes| E["Determine alert level:<br/>Yellow/Orange/Red"]
    E --> F["Yellow Alert?"]
    F -->|Yes| G["Send to app only<br/>+ dashboard update"]
    F -->|No| H["Orange/Red Alert"]
    H --> I["Send SMS/Email to<br/>Community Leaders"]
    I --> J["Send Push + In-app<br/>to all Volunteers"]
    J --> K["Update dashboard<br/>with highlighted zone<br/>& countdown timer"]
    K --> L["Sound alarm<br/>if in Web"]
    L --> M["End"]
```

---

#### **UC3: Assess Population Impact**

```mermaid
---
config:
  theme: neo
  look: neo
---
graph LR
    A["Government Official<br/>selects Event & Date"] --> B["System queries<br/>affected zone geometry"]
    B --> C["Find all buildings<br/>in affected zone"]
    C --> D["Count residents<br/>per building"]
    D --> E["Cross-reference with<br/>AVCA intervention data"]
    E --> F["Calculate metrics:<br/>- Total affected<br/>- Previously linked<br/>- Reach rate"]
    F --> G["Calculate vulnerable ratio:<br/>- Disabled persons<br/>- Elderly<br/>- Children"]
    G --> H["Generate report with:<br/>Charts, tables,<br/>statistics, maps"]
    H --> I["Option: Export to<br/>PDF/Excel"]
    I --> J["End"]
```

---

#### **UC4: Plan Evacuation Routes**

```mermaid
---
config:
  theme: neo
  look: neo
---
graph LR
    A["Community Leader<br/>receives high alert"] --> B["Opens Map<br/>in emergency mode"]
    B --> C["Highlights affected zone<br/>in red"]
    C --> D["System shows 3 pre-calculated<br/>evacuation routes:<br/>- Route A: 2.3 km<br/>- Route B: 3.1 km<br/>- Route C: 4.5 km"]
    D --> E["Each route shows:<br/>- Safe Buildings<br/>- Checkpoints<br/>- Capacity"]
    E --> F["Leader selects<br/>Route A"]
    F --> G["System calculates<br/>evacuation time for<br/>el
derly = 45 min"]
    G --> H["Leader initiates<br/>evacuation protocol<br/>via 'Activate' button"]
    H --> I["System sends<br/>SMS to residents<br/>+ volunteers"]
    I --> J["Dashboard tracks<br/>evacuation progress"]
    J --> K["End"]
```

---

#### **UC5: Report Field Damage**

```mermaid
---
config:
  theme: neo
  look: neo
---
graph LR
    A["Volunteer in field<br/>encounters damage"] --> B["Opens Mobile App<br/>Damage Report Screen"]
    B --> C["App auto-fills:<br/>- GPS location<br/>- Current time<br/>- Zone/Building ID"]
    C --> D["Volunteer enters:<br/>- Damage level<br/>- Damage type<br/>- People count<br/>- Injury status"]
    D --> E["Volunteer takes<br/>3-5 photos"]
    E --> F["Optional: Add voice<br/>comment"]
    F --> G["Save locally"]
    G --> H{"Network<br/>available?"}
    H -->|Yes| I["Upload immediately"]
    H -->|No| J["Queue for upload<br/>when connected"]
    I --> K["Dashboard updates<br/>with field data<br/>in real-time"]
    J --> K
    K --> L["Leader notified<br/>of new reports"]
    L --> M["End"]
```

---

#### **UC6: Export Community Resilience Report**

```mermaid
---
config:
  theme: neo
  look: neo
---
graph LR
    A["Government Official<br/>needs report for<br/>federation"]
    --> B["Selects date range<br/>& zones"]
    B --> C["System aggregates:<br/>- Population statistics<br/>- Intervention reach<br/>- Event impacts<br/>- Risk assessments"]
    C --> D["Generate visualizations:<br/>- Charts (reach %)<br/>- Maps (risk zones)<br/>- Tables (event data)"]
    D --> E["Compile to:<br/>PDF / Excel / GeoJSON"]
    E --> F["Add metadata:<br/>- Generated date<br/>- Data sources<br/>- Legend"]
    F --> G["Download<br/>Resilience_Report_2024_Q1.pdf"]
    G --> H["Share with:<br/>- Mayor's office<br/>- NGOs<br/>- Planning dept"]
    H --> I["End"]
```

---

#### **UC7: Analyze Intervention Effectiveness**

```mermaid
---
config:
  theme: neo
  look: neo
---
graph LR
    A["Data Scientist<br/>opens Analytics Tool"] --> B["Select intervention:<br/>Cohesion Workshop"]
    B --> C["Time range:<br/>Q4 2023 - Q4 2024"]
    C --> D["System queries:<br/>- Workshop participants<br/>- Zones covered<br/>- Climate events in zones<br/>- Affected population"]
    D --> E["Calculate metrics:<br/># reached / # target"]
    E --> F["Correlate with events:<br/># in intervention zone<br/>/ # total affected"]
    F --> G["Statistical analysis:<br/>Did training improve<br/>response time?"]
    G --> H["Visualize with:<br/>- Scatter plots<br/>- Heat maps<br/>- Trend lines"]
    H --> I["Export methodology<br/>& findings"]
    I --> J["Share with<br/>academic partners"]
    J --> K["End"]
```

---

#### **UC8: Predict Future Vulnerable Zones**

```mermaid
---
config:
  theme: neo
  look: neo
---
graph LR
    A["ML Pipeline scheduled<br/>monthly"] --> B["Ingest 5 years of<br/>historical data"]
    B --> C["Train model on:<br/>- Climate patterns<br/>- Building vulnerability<br/>- Socioeconomic factors<br/>- Infrastructure gaps"]
    C --> D["Model: Random Forest<br/>+ ARIMA time series"]
    D --> E["Predict 12-month<br/>risk scores for<br/>all zones"]
    E --> F["Identify zones<br/>with rising risk<br/>trajectory"]
    F --> G["Flag for intervention<br/>planning"]
    G --> H["Create priority list:<br/>1. Zone X<br/>2. Zone Y<br/>3. Zone Z"]
    H --> I["Send to Program<br/>Planning Team"]
    I --> J["End"]
```

---

#### **UC9: Configure Alert Thresholds**

```mermaid
---
config:
  theme: neo
  look: neo
---
graph LR
    A["Emergency Coordinator<br/>manages alert config"] --> B["Opens Settings:<br/>Alert Configuration"]
    B --> C["Current settings:<br/>- Generic thresholds<br/>- All zones same"]
    C --> D["Coordinator can:<br/>1. Edit flood risk %<br/>2. Edit heat index<br/>3. Edit alert delays"]
    D --> E["Customize per zone:<br/>El Danubio: 75%<br/>La María: 70%"]
    E --> F["Set notification rules:<br/>- Yellow: Leaders only<br/>- Orange: + Volunteers<br/>- Red: + Media"]
    F --> G["Configure timing:<br/>Advance notice: 24h"]
    G --> H["Save configuration<br/>+ version control"]
    H --> I["System logs:<br/>Who, when, what changed"]
    I --> J["Next alert uses<br/>new thresholds"]
    J --> K["End"]
```

---

## **6. TECHNICAL PATTERNS & DESIGN DECISIONS**

### **Pattern 1: Real-time Alert Distribution**

```
Event: High Risk Detected
├─ Alert object created with ID: ALT-2024-02-08-001
├─ Persisted to database (PostgreSQL)
├─ Published to Redis Pub/Sub channel: "alerts:zone_3"
├─ Subscribers receive (WebSocket):
│  ├─ API Server 1 → broadcast to connected web clients
│  ├─ Notification Worker → dispatch SMS/Email/Push
│  ├─ Logging Service → store for audit trail
│  └─ Analytics Service → model improvement pipeline
└─ State stored in Redis for 7 days (audit + replay)
```

### **Pattern 2: Geofencing for Zone Containment**

```sql
-- Query: Find all buildings within flood risk zone
SELECT b.building_id, b.residents, p.name
FROM buildings b
JOIN persons p ON b.building_id = p.building_id
WHERE ST_DWithin(
    b.geometry,
    (SELECT geometry FROM zones WHERE zone_id = 3),
    0  -- Exactly within zone (no buffer)
)
AND ST_Intersects(b.geometry, event.affected_geometry)
ORDER BY p.age DESC  -- Prioritize monitoring elderly
```

### **Pattern 3: Caching Strategy (Multi-Layer)**

```
Request: Get zone risk scores
├─ L1: Browser localStorage (1 hour) ← Fastest
├─ L2: Redis cache (1 hour) ← Shared across API servers
├─ L3: PostGIS materialized view (10 min) ← Computed cache
└─ L4: Full calculation (every 60 min) ← Slow, authoritative

Strategy: Check L1 → L2 → L3 → L4 (in order)
Invalidation: When weather data refreshed, clear L2+L3
```

### **Pattern 4: Event Sourcing for Accountability**

```
All state changes logged as events:
├─ alert_created
├─ alert_escalated (from YELLOW to ORANGE)
├─ alert_notification_sent (to leader_id: 123)
├─ evacuation_initiated (zone_id: 3)
├─ damage_report_filed (volunteer_id: 456)
├─ intervention_completed
└─ all_events_queried_by_dashboard

Benefits:
- Audit trail of who did what when
- Replay events to test scenarios
- Calculate metrics across time
```

---

## **7. SCALABILITY & PERFORMANCE TARGETS**

| Metric | Target | Current Approach | Scale-up Strategy |
|--------|--------|------------------|-------------------|
| **Zone Risk Calculation** | <30s for all zones | Sequential processing | Parallel by zone (Celery workers) |
| **Alert Delivery** | <2 min to first responder | Direct SMS API calls | Queue-based with retry logic |
| **Dashboard Load Time** | <3s | Data aggregation per view | GraphQL + pre-computed aggregates |
| **Concurrent Users** | 500 volunteers | Single API server | Kubernetes HPA (horizontal pod autoscaling) |
| **Data Ingestion** | Real-time (60m intervals) | Batch hourly | Stream processing (Kafka) for <10m latency |
