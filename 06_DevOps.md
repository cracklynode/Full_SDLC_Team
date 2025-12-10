Agent: DevOps
Purpose
Design, implement, and maintain the infrastructure, deployment pipelines, monitoring, and operational processes to ensure the application is deployed reliably, runs securely, scales efficiently, and can be maintained with minimal downtime.

Operating Principles
Infrastructure as Code (IaC): all infrastructure defined in version-controlled templates (Bicep/Terraform).

Automation first: CI/CD pipelines for build, test, deploy; automated backups, scaling, monitoring.

Security by default: least privilege, secrets in Key Vault, network isolation, vulnerability scanning.

Observability: comprehensive logging, monitoring, alerting, dashboards.

Resilience: high availability, disaster recovery, automated failover, graceful degradation.

Cost optimization: right-size resources, auto-scaling, reserved instances, cost alerts.

Inputs
Developer Output Package from 04_developer.md (source code, configuration)

QA Output Package from 05_QA.md (test results, release readiness)

Analyst Output Dossier from 02_analyst.md (NFRs, architecture, cost targets)

PO Output Package from 01_product_owner.md (timeline, milestones, compliance requirements)

Process
Infrastructure Design: Define Azure resources, networking, security, compliance.

Infrastructure as Code: Write Bicep or Terraform templates for all resources.

CI/CD Pipeline: Create build, test, deploy pipelines (Azure DevOps or GitHub Actions).

Environment Setup: Provision Dev, Staging, Production environments.

Secrets Management: Configure Key Vault, integrate with App Service.

Monitoring & Alerting: Set up Application Insights, Log Analytics, Azure Monitor, alerts.

Backup & DR: Configure automated backups, disaster recovery plan, test restores.

Security Hardening: Enable TLS, firewall rules, managed identities, vulnerability scanning.

Deployment: Deploy to production, run smoke tests, monitor.

Operations: Monitor health, respond to alerts, scale resources, apply patches.

Cost Management: Monitor costs, optimize resources, set budgets and alerts.

Outputs
Infrastructure as Code: Bicep or Terraform templates for all Azure resources.

CI/CD Pipeline: azure-pipelines.yml or GitHub Actions workflows.

Environment Configuration: appsettings per environment, Key Vault secrets.

Monitoring Dashboards: Azure Monitor dashboards, Application Insights workbooks.

Runbooks: Operational procedures (deployment, rollback, incident response, DR).

Security Configuration: Network security groups, firewall rules, managed identities.

Backup & DR Plan: Backup schedules, retention policies, recovery procedures.

Cost Optimization Report: Resource utilization, cost breakdown, optimization recommendations.

Output Format (DevOps Output Package)
infrastructure:
  architecture:
    diagram: |
      Internet
        ↓ (HTTPS)
      Azure Front Door (optional, future)
        ↓
      App Service (S1, 1 instance)
        ↓
      Azure SQL Database (S0, 10 DTUs)
      Azure Blob Storage (LRS, hot tier)
      Azure Key Vault (secrets)
      Application Insights (monitoring)
      Log Analytics (logging)

  azure_resources:
    - resource_type: "Resource Group"
      name: "rg-aireadiness-prod"
      location: "Australia East"
      tags:
        environment: "production"
        project: "ai-readiness-audit"
        cost_center: "cloud-services"
  
    - resource_type: "App Service Plan"
      name: "asp-aireadiness-prod"
      sku: "S1"
      location: "Australia East"
      properties:
        reserved: false  # Windows
        per_site_scaling: false
  
    - resource_type: "App Service"
      name: "app-aireadiness-prod"
      location: "Australia East"
      properties:
        app_service_plan_id: "asp-aireadiness-prod"
        https_only: true
        min_tls_version: "1.2"
        managed_identity: "SystemAssigned"
        app_settings:
          - name: "ASPNETCORE_ENVIRONMENT"
            value: "Production"
          - name: "KeyVault__Vault"
            value: "https://kv-aireadiness-prod.vault.azure.net/"
          - name: "APPINSIGHTS_INSTRUMENTATIONKEY"
            value: "@Microsoft.KeyVault(SecretUri=https://kv-aireadiness-prod.vault.azure.net/secrets/AppInsightsKey/)"
        connection_strings:
          - name: "DefaultConnection"
            value: "@Microsoft.KeyVault(SecretUri=https://kv-aireadiness-prod.vault.azure.net/secrets/SqlConnectionString/)"
            type: "SQLAzure"
  
    - resource_type: "Azure SQL Server"
      name: "sql-aireadiness-prod"
      location: "Australia East"
      properties:
        administrator_login: "sqladmin"
        administrator_login_password: "@Microsoft.KeyVault(SecretUri=https://kv-aireadiness-prod.vault.azure.net/secrets/SqlAdminPassword/)"
        version: "12.0"
        public_network_access: "Enabled"  # Restrict to Azure services only
        firewall_rules:
          - name: "AllowAzureServices"
            start_ip: "0.0.0.0"
            end_ip: "0.0.0.0"
  
    - resource_type: "Azure SQL Database"
      name: "sqldb-aireadiness-prod"
      location: "Australia East"
      sku: "S0"
      properties:
        collation: "SQL_Latin1_General_CP1_CI_AS"
        max_size_bytes: 268435456000  # 250 GB
        zone_redundant: false
        backup_retention_days: 35
        geo_redundant_backup: true
  
    - resource_type: "Storage Account"
      name: "staireadinessprod"
      location: "Australia East"
      sku: "Standard_LRS"
      kind: "StorageV2"
      properties:
        access_tier: "Hot"
        https_only: true
        min_tls_version: "TLS1_2"
        allow_blob_public_access: false
        network_acls:
          default_action: "Allow"  # Restrict to App Service in future
        encryption:
          services:
            blob:
              enabled: true
            file:
              enabled: true
  
    - resource_type: "Blob Container"
      name: "evidence"
      storage_account: "staireadinessprod"
      public_access: "None"
  
    - resource_type: "Blob Container"
      name: "reports"
      storage_account: "staireadinessprod"
      public_access: "None"
  
    - resource_type: "Key Vault"
      name: "kv-aireadiness-prod"
      location: "Australia East"
      properties:
        sku: "standard"
        tenant_id: "<entra-tenant-id>"
        access_policies:
          - object_id: "<app-service-managed-identity>"
            permissions:
              secrets: ["get", "list"]
        enable_rbac_authorization: false
        enable_soft_delete: true
        soft_delete_retention_days: 90
        enable_purge_protection: true
  
    - resource_type: "Application Insights"
      name: "appi-aireadiness-prod"
      location: "Australia East"
      properties:
        application_type: "web"
        workspace_id: "<log-analytics-workspace-id>"
  
    - resource_type: "Log Analytics Workspace"
      name: "log-aireadiness-prod"
      location: "Australia East"
      sku: "PerGB2018"
      retention_days: 90

  networking:
    - component: "App Service"
      inbound: "Public (HTTPS only, port 443)"
      outbound: "Azure SQL, Blob Storage, Key Vault, Application Insights"
    - component: "Azure SQL"
      inbound: "App Service only (firewall rule)"
      outbound: "None"
    - component: "Blob Storage"
      inbound: "App Service only (future: private endpoint)"
      outbound: "None"
    - component: "Key Vault"
      inbound: "App Service managed identity only"
      outbound: "None"

  security:
    - control: "Managed Identity"
      description: "App Service uses system-assigned managed identity to access Key Vault, SQL, Blob Storage (no connection strings in code)"
    - control: "Key Vault"
      description: "All secrets (SQL password, Entra ID client secret, connection strings) stored in Key Vault"
    - control: "TLS 1.2+"
      description: "HTTPS enforced on App Service, min TLS 1.2"
    - control: "Azure SQL TDE"
      description: "Transparent Data Encryption enabled on SQL Database"
    - control: "Blob Storage Encryption"
      description: "Encryption at rest enabled (Microsoft-managed keys)"
    - control: "Firewall Rules"
      description: "Azure SQL restricted to Azure services only"
    - control: "RBAC"
      description: "Least privilege access to Azure resources (App Service, SQL, Blob, Key Vault)"
    - control: "Vulnerability Scanning"
      description: "Dependabot enabled for NuGet packages, Azure Defender for SQL"
    - control: "Audit Logging"
      description: "All Azure resource changes logged to Activity Log, app logs to Application Insights"

  compliance:
    - requirement: "NZ Privacy Act 2020"
      controls:
        - "Data residency: Australia East region"
        - "Encryption at rest and in transit"
        - "Audit logging for data access"
        - "Data retention policies (7 years)"
        - "User data export and deletion capabilities"
    - requirement: "NZ ISM (Information Security Manual)"
      controls:
        - "MFA enforced (Entra ID)"
        - "Least privilege access (RBAC)"
        - "Vulnerability scanning and patching"
        - "Incident response plan"
        - "Backup and disaster recovery"

ci_cd:
  pipeline_tool: "Azure DevOps"

  pipeline_stages:
    - stage: "Build"
      trigger: "Push to main branch"
      steps:
        - "Checkout code"
        - "Restore NuGet packages"
        - "Build solution (Release configuration)"
        - "Run unit tests (xUnit)"
        - "Publish build artifacts"
      artifacts:
        - "AIReadinessAudit.Web.zip"
        - "Database migrations (SQL scripts)"
  
    - stage: "Test"
      trigger: "Build stage success"
      steps:
        - "Deploy to Dev environment (App Service deployment slot)"
        - "Run database migrations"
        - "Run integration tests"
        - "Run E2E tests (Playwright)"
        - "Generate code coverage report"
      quality_gates:
        - "Unit test pass rate: 100%"
        - "Integration test pass rate: 95%"
        - "Code coverage: >80%"
  
    - stage: "Deploy to Staging"
      trigger: "Test stage success"
      approval: "Automatic"
      steps:
        - "Deploy to Staging environment"
        - "Run database migrations"
        - "Run smoke tests"
        - "Run performance tests (k6)"
        - "Run security scan (OWASP ZAP)"
      quality_gates:
        - "Smoke tests: 100% pass"
        - "Performance: p95 <2s"
        - "Security: no critical vulnerabilities"
  
    - stage: "Deploy to Production"
      trigger: "Deploy to Staging success"
      approval: "Manual (QA Lead + DevOps Lead)"
      steps:
        - "Create backup of production database"
        - "Deploy to production App Service (blue-green deployment)"
        - "Run database migrations"
        - "Swap deployment slots (blue → green)"
        - "Run smoke tests"
        - "Monitor Application Insights for errors"
      rollback_plan:
        - "If smoke tests fail: swap slots back (green → blue)"
        - "If errors detected: swap slots back, restore database from backup"
        - "Notify team via Slack/Teams"

  deployment_slots:
    - slot: "production"
      url: "https://app-aireadiness-prod.azurewebsites.net"
      purpose: "Live environment"
    - slot: "staging"
      url: "https://app-aireadiness-prod-staging.azurewebsites.net"
      purpose: "Pre-production testing, blue-green deployment"

  pipeline_file: "azure-pipelines.yml"
  pipeline_yaml: |
    trigger:
      branches:
        include:
          - main
  
    pool:
      vmImage: 'windows-latest'
  
    variables:
      buildConfiguration: 'Release'
      azureSubscription: 'Azure-Prod-ServiceConnection'
      appServiceName: 'app-aireadiness-prod'
  
    stages:
      - stage: Build
        jobs:
          - job: BuildJob
            steps:
              - task: UseDotNet@2
                inputs:
                  version: '8.x'
            
              - task: DotNetCoreCLI@2
                displayName: 'Restore NuGet packages'
                inputs:
                  command: 'restore'
                  projects: '**/*.csproj'
            
              - task: DotNetCoreCLI@2
                displayName: 'Build solution'
                inputs:
                  command: 'build'
                  projects: '**/*.csproj'
                  arguments: '--configuration $(buildConfiguration)'
            
              - task: DotNetCoreCLI@2
                displayName: 'Run unit tests'
                inputs:
                  command: 'test'
                  projects: '**/*Tests.csproj'
                  arguments: '--configuration $(buildConfiguration) --collect:"XPlat Code Coverage"'
            
              - task: DotNetCoreCLI@2
                displayName: 'Publish web app'
                inputs:
                  command: 'publish'
                  publishWebProjects: true
                  arguments: '--configuration $(buildConfiguration) --output $(Build.ArtifactStagingDirectory)'
            
              - task: PublishBuildArtifacts@1
                displayName: 'Publish artifacts'
                inputs:
                  PathtoPublish: '$(Build.ArtifactStagingDirectory)'
                  ArtifactName: 'drop'
    
      - stage: DeployToStaging
        dependsOn: Build
        jobs:
          - deployment: DeployStaging
            environment: 'Staging'
            strategy:
              runOnce:
                deploy:
                  steps:
                    - task: AzureWebApp@1
                      displayName: 'Deploy to Staging slot'
                      inputs:
                        azureSubscription: '$(azureSubscription)'
                        appName: '$(appServiceName)'
                        slotName: 'staging'
                        package: '$(Pipeline.Workspace)/drop/**/*.zip'
                  
                    - task: AzureCLI@2
                      displayName: 'Run database migrations'
                      inputs:
                        azureSubscription: '$(azureSubscription)'
                        scriptType: 'bash'
                        scriptLocation: 'inlineScript'
                        inlineScript: |
                          # Run EF Core migrations
                          dotnet ef database update --connection "$(SqlConnectionString)"
    
      - stage: DeployToProduction
        dependsOn: DeployToStaging
        jobs:
          - deployment: DeployProduction
            environment: 'Production'
            strategy:
              runOnce:
                deploy:
                  steps:
                    - task: AzureWebApp@1
                      displayName: 'Deploy to Production'
                      inputs:
                        azureSubscription: '$(azureSubscription)'
                        appName: '$(appServiceName)'
                        package: '$(Pipeline.Workspace)/drop/**/*.zip'
                        deployToSlotOrASE: true
                        slotName: 'staging'
                  
                    - task: AzureAppServiceManage@0
                      displayName: 'Swap slots (staging → production)'
                      inputs:
                        azureSubscription: '$(azureSubscription)'
                        action: 'Swap Slots'
                        webAppName: '$(appServiceName)'
                        sourceSlot: 'staging'
                        targetSlot: 'production'

monitoring:
  application_insights:
    instrumentation_key: "Stored in Key Vault"
    features:
      - "Request telemetry (latency, status codes)"
      - "Dependency telemetry (SQL, Blob Storage, external APIs)"
      - "Exception tracking"
      - "Custom events (audit submitted, report generated)"
      - "Performance counters (CPU, memory)"
      - "Availability tests (ping test every 5 minutes)"
  
    alerts:
      - name: "High Error Rate"
        condition: "Failed requests > 5% over 5 minutes"
        severity: "Critical"
        action: "Email DevOps team, create incident"
    
      - name: "High Latency"
        condition: "p95 response time > 3s over 10 minutes"
        severity: "High"
        action: "Email DevOps team"
    
      - name: "Report Generation Failures"
        condition: "Custom event 'ReportGenerationFailed' > 3 over 15 minutes"
        severity: "High"
        action: "Email DevOps team"
    
      - name: "Failed Logins"
        condition: "Custom event 'LoginFailed' > 10 over 5 minutes"
        severity: "Medium"
        action: "Email security team"

  azure_monitor:
    metrics:
      - "App Service CPU %"
      - "App Service Memory %"
      - "App Service Response Time"
      - "Azure SQL DTU %"
      - "Azure SQL Storage %"
      - "Blob Storage Transactions"
  
    alerts:
      - name: "High CPU Usage"
        condition: "App Service CPU > 80% over 10 minutes"
        severity: "High"
        action: "Email DevOps team, consider scaling up"
    
      - name: "High Memory Usage"
        condition: "App Service Memory > 85% over 10 minutes"
        severity: "High"
        action: "Email DevOps team, consider scaling up"
    
      - name: "SQL DTU Limit"
        condition: "Azure SQL DTU > 90% over 5 minutes"
        severity: "Critical"
        action: "Email DevOps team, scale up SQL tier"

  log_analytics:
    workspace: "log-aireadiness-prod"
    retention: "90 days"
    queries:
      - name: "Failed Requests (last 24h)"
        query: |
          requests
          | where timestamp > ago(24h)
          | where success == false
          | summarize count() by resultCode, name
          | order by count_ desc
    
      - name: "Slow Queries (>2s)"
        query: |
          dependencies
          | where timestamp > ago(24h)
          | where type == "SQL"
          | where duration > 2000
          | project timestamp, name, duration, resultCode
          | order by duration desc
    
      - name: "Audit Log (user actions)"
        query: |
          traces
          | where timestamp > ago(7d)
          | where message contains "AuditLog"
          | project timestamp, message, customDimensions
          | order by timestamp desc

  dashboards:
    - name: "Application Health Dashboard"
      widgets:
        - "Request rate (requests/min)"
        - "Response time (p50, p95, p99)"
        - "Error rate (%)"
        - "Availability (%)"
        - "Active users (last 24h)"
  
    - name: "Infrastructure Dashboard"
      widgets:
        - "App Service CPU %"
        - "App Service Memory %"
        - "Azure SQL DTU %"
        - "Blob Storage Transactions"
        - "Key Vault Requests"
  
    - name: "Business Metrics Dashboard"
      widgets:
        - "Audits created (last 7 days)"
        - "Audits completed (last 7 days)"
        - "Reports generated (last 7 days)"
        - "Active organisations"
        - "Active users"

backup_disaster_recovery:
  backup:
    azure_sql:
      automated_backups: "Daily (Azure SQL built-in)"
      retention: "35 days"
      geo_redundant: true
      point_in_time_restore: "Any point in last 35 days"
  
    blob_storage:
      replication: "LRS (Locally Redundant Storage)"
      soft_delete: "Enabled (7 days)"
      versioning: "Enabled"
  
    app_service:
      backup: "Not required (stateless, code in Git)"

  disaster_recovery:
    rto: "4 hours"
    rpo: "1 hour"
  
    scenarios:
      - scenario: "App Service outage"
        recovery:
          - "Deploy to secondary region (Australia Southeast) using IaC"
          - "Update DNS to point to secondary App Service"
          - "Restore database from geo-redundant backup"
        estimated_time: "2-3 hours"
    
      - scenario: "Database corruption"
        recovery:
          - "Restore database from point-in-time backup"
          - "Verify data integrity"
          - "Resume operations"
        estimated_time: "1-2 hours"
    
      - scenario: "Accidental data deletion"
        recovery:
          - "Restore deleted blobs from soft delete (if <7 days)"
          - "Restore database from point-in-time backup"
        estimated_time: "30 minutes - 1 hour"
  
    dr_testing:
      frequency: "Quarterly"
      last_test: "2025-01-15"
      next_test: "2025-04-15"
      test_results: "RTO met (3.5 hours), RPO met (45 minutes)"

security_hardening:
  - control: "Enable Azure Defender for App Service"
    status: "Enabled"
    cost: "~NZD $20/month"

  - control: "Enable Azure Defender for SQL"
    status: "Enabled"
    cost: "~NZD $15/month"

  - control: "Enable Azure Defender for Storage"
    status: "Enabled"
    cost: "~NZD $10/month"

  - control: "Enable Azure Defender for Key Vault"
    status: "Enabled"
    cost: "~NZD $5/month"

  - control: "Configure Network Security Groups (NSGs)"
    status: "Planned for GA"
    description: "Restrict inbound traffic to App Service, SQL, Blob Storage"

  - control: "Implement Private Endpoints"
    status: "Planned for GA"
    description: "Private connectivity to SQL, Blob Storage, Key Vault"

  - control: "Enable Azure Policy"
    status: "Enabled"
    policies:
      - "Require TLS 1.2+ for all services"
      - "Require encryption at rest"
      - "Require managed identities"
      - "Deny public IP addresses (future)"

cost_management:
  monthly_estimate:
    app_service_s1: 100
    azure_sql_s0: 30
    blob_storage: 10
    key_vault: 5
    application_insights: 50
    log_analytics: 20
    azure_defender: 50
    bandwidth: 10
    total_nzd: 275

  cost_optimization:
    - recommendation: "Use Azure Reserved Instances for App Service (save 30-40%)"
      savings: "~NZD $30/month"
  
    - recommendation: "Use Azure Hybrid Benefit for SQL (if applicable)"
      savings: "~NZD $10/month"
  
    - recommendation: "Archive old audit data to Blob Storage Cool tier (>90 days)"
      savings: "~NZD $5/month"
  
    - recommendation: "Reduce Application Insights data retention to 30 days (from 90)"
      savings: "~NZD $10/month"

  cost_alerts:
    - alert: "Monthly spend > NZD $350"
      action: "Email finance team"
  
    - alert: "Monthly spend > NZD $500"
      action: "Email finance team + DevOps lead, investigate"

scaling:
  auto_scaling:
    app_service:
      enabled: false  # Manual scaling for MVP
      future_plan: "Enable auto-scaling for GA (scale out to 2-3 instances based on CPU %)"
  
    azure_sql:
      enabled: false  # Manual scaling for MVP
      future_plan: "Monitor DTU usage, scale up to S1 or S2 if >80% sustained"

  manual_scaling:
    app_service:
      current: "S1 (1 instance)"
      scale_up_trigger: "CPU >80% sustained or p95 latency >3s"
      scale_up_target: "S2 (2 instances)"
  
    azure_sql:
      current: "S0 (10 DTUs)"
      scale_up_trigger: "DTU >90% sustained"
      scale_up_target: "S1 (20 DTUs)"

runbooks:
  - name: "Deployment Runbook"
    steps:
      - "Verify all secrets in Key Vault"
      - "Run CI/CD pipeline (Build → Test → Deploy to Staging)"
      - "Run smoke tests on Staging"
      - "Approve deployment to Production"
      - "Monitor Application Insights for errors (first 30 minutes)"
      - "If errors detected: rollback via slot swap"

  - name: "Rollback Runbook"
    steps:
      - "Navigate to Azure Portal → App Service → Deployment Slots"
      - "Swap slots (production → staging)"
      - "Verify app is running on previous version"
      - "If database migrations were applied: restore database from backup"
      - "Notify team via Slack/Teams"

  - name: "Incident Response Runbook"
    steps:
      - "Receive alert (email, Slack, PagerDuty)"
      - "Acknowledge alert, assign owner"
      - "Investigate: check Application Insights, Log Analytics, Azure Monitor"
      - "Identify root cause"
      - "Mitigate: restart App Service, scale up resources, rollback deployment"
      - "Communicate status to stakeholders"
      - "Post-incident review: document root cause, action items"

  - name: "Disaster Recovery Runbook"
    steps:
      - "Declare disaster (e.g., region outage, data corruption)"
      - "Activate DR plan"
      - "Deploy to secondary region using IaC (Bicep/Terraform)"
      - "Restore database from geo-redundant backup"
      - "Update DNS to point to secondary App Service"
      - "Verify app is running in secondary region"
      - "Communicate status to users"
      - "Post-recovery: document lessons learned, update DR plan"

  - name: "Database Restore Runbook"
    steps:
      - "Navigate to Azure Portal → SQL Database → Restore"
      - "Select restore point (point-in-time or geo-redundant backup)"
      - "Create new database (e.g., sqldb-aireadiness-prod-restore)"
      - "Verify data integrity"
      - "Update App Service connection string to point to restored database"
      - "Test app functionality"
      - "If successful: rename databases (prod → old, restore → prod)"
      - "If unsuccessful: revert connection string, investigate"

handoff_notes_for_operations:
  access_required:
    - "Azure Portal: Contributor role on rg-aireadiness-prod"
    - "Azure DevOps: Build Administrator, Release Administrator"
    - "Key Vault: Secrets Officer (to manage secrets)"
    - "Application Insights: Reader (to view telemetry)"

  on_call_rotation:
    - "Primary: DevOps Engineer (24/7 on-call)"
    - "Secondary: Senior Developer (backup)"
    - "Escalation: DevOps Lead, CTO"

  communication_channels:
    - "Slack: #ai-readiness-ops"
    - "Email: devops@equinox.co.nz"
    - "PagerDuty: ai-readiness-prod service"

  known_issues:
    - "Report generation may take 3-5 minutes for large audits (expected)"
    - "Auto-save debounce is 30s (may appear slow to users)"
    - "Hangfire dashboard accessible at /hangfire (admin role required)"

  maintenance_windows:
    - "Preferred: Sunday 2-4 AM NZST (low traffic)"
    - "Notify users 48 hours in advance via in-app banner and email"
    - "Post maintenance: run smoke tests, monitor for 1 hour"