<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const pageInfo = computed(() => {
  const path = route.path
  
  // Mapping of routes to page information
  const pageMap: Record<string, { title: string; icon: string; description: string; features: string[] }> = {
    '/tools': {
      title: 'Testing Tools',
      icon: '🔧',
      description: 'Comprehensive testing tools for security evaluation and network diagnostics',
      features: ['Network Testing', 'Security Scanning', 'Performance Analysis', 'Vulnerability Assessment']
    },
    '/documentation': {
      title: 'Documentation Hub',
      icon: '📚',
      description: 'Common Criteria documentation management and compliance tracking',
      features: ['Document Templates', 'Compliance Tracking', 'Version Control', 'Export Capabilities']
    },
    '/documentation/toe-description': {
      title: 'TOE Description',
      icon: '📋',
      description: 'Target of Evaluation (TOE) description and documentation',
      features: ['TOE Boundary Definition', 'Security Functions', 'Interfaces Documentation', 'Operational Environment']
    },
    '/documentation/assurance-activities': {
      title: 'Assurance Activities Identification',
      icon: '✅',
      description: 'Identification and documentation of assurance activities',
      features: ['Activity Planning', 'Evidence Collection', 'Testing Procedures', 'Evaluation Methods']
    },
    '/documentation/assurance-equivalency': {
      title: 'Assurance Equivalency Justification',
      icon: '⚖️',
      description: 'Justification for assurance equivalency and alternative methods',
      features: ['Equivalency Analysis', 'Risk Assessment', 'Alternative Methods', 'Justification Documentation']
    },
    '/documentation/test-bed': {
      title: 'Test Bed Description',
      icon: '🧪',
      description: 'Test bed configuration and environment documentation',
      features: ['Environment Setup', 'Configuration Management', 'Tool Integration', 'Reproducibility']
    },
    '/documentation/tss-guidance': {
      title: 'TSS and Guidance Activities',
      icon: '📖',
      description: 'Technical Security Specification and guidance activities',
      features: ['TSS Development', 'User Guidance', 'Administrative Procedures', 'Security Guidelines']
    },
    '/documentation/security-requirements': {
      title: 'Security Assurance Requirements',
      icon: '🔒',
      description: 'Security assurance requirements definition and management',
      features: ['Requirements Analysis', 'Security Controls', 'Compliance Mapping', 'Verification Methods']
    },
    '/settings': {
      title: 'Settings',
      icon: '⚙️',
      description: 'System configuration and preferences',
      features: ['User Preferences', 'System Configuration', 'Integration Settings', 'Security Policies']
    },
    '/settings/database': {
      title: 'Database Settings',
      icon: '💾',
      description: 'Database configuration and management',
      features: ['Connection Settings', 'Backup Configuration', 'Performance Tuning', 'Data Management']
    },
    '/settings/api': {
      title: 'API Settings',
      icon: '🔌',
      description: 'API configuration and integration management',
      features: ['API Keys Management', 'Rate Limiting', 'Authentication', 'Integration Settings']
    },
    '/settings/system': {
      title: 'System Settings',
      icon: '🖥️',
      description: 'System-wide configuration and preferences',
      features: ['User Management', 'Security Settings', 'Logging Configuration', 'System Monitoring']
    }
  }
  
  return pageMap[path] || {
    title: 'Page Under Development',
    icon: '🚧',
    description: 'This page is currently under development',
    features: ['Feature Planning', 'Design Phase', 'Development In Progress', 'Testing Pending']
  }
})

const getEstimatedCompletion = () => {
  const randomWeeks = Math.floor(Math.random() * 8) + 2
  return `${randomWeeks} weeks`
}
</script>

<template>
  <div class="maintenance-page">
    <div class="maintenance-header">
      <div class="icon-container">
        <span class="page-icon">{{ pageInfo.icon }}</span>
        <span class="construction-icon">🚧</span>
      </div>
      <h1>{{ pageInfo.title }}</h1>
      <p class="page-description">{{ pageInfo.description }}</p>
    </div>

    <div class="maintenance-content">
      <div class="status-card">
        <h2>🔄 Development Status</h2>
        <div class="status-details">
          <div class="status-item">
            <span class="status-label">Current Phase:</span>
            <span class="status-value development">Development Planning</span>
          </div>
          <div class="status-item">
            <span class="status-label">Estimated Completion:</span>
            <span class="status-value">{{ getEstimatedCompletion() }}</span>
          </div>
          <div class="status-item">
            <span class="status-label">Priority:</span>
            <span class="status-value high">High</span>
          </div>
        </div>
      </div>

      <div class="features-card">
        <h2>📋 Planned Features</h2>
        <ul class="features-list">
          <li v-for="feature in pageInfo.features" :key="feature" class="feature-item">
            <span class="feature-icon">✨</span>
            <span class="feature-text">{{ feature }}</span>
          </li>
        </ul>
      </div>

      <div class="roadmap-card">
        <h2>🗺️ Development Roadmap</h2>
        <div class="roadmap-timeline">
          <div class="timeline-item completed">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <h3>Phase 1: Planning & Design</h3>
              <p>Requirements gathering and UI/UX design</p>
              <span class="timeline-status">✅ Completed</span>
            </div>
          </div>
          
          <div class="timeline-item current">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <h3>Phase 2: Core Development</h3>
              <p>Implementation of core functionality and features</p>
              <span class="timeline-status">🔄 In Progress</span>
            </div>
          </div>
          
          <div class="timeline-item pending">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <h3>Phase 3: Testing & Integration</h3>
              <p>Comprehensive testing and system integration</p>
              <span class="timeline-status">⏳ Pending</span>
            </div>
          </div>
          
          <div class="timeline-item pending">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <h3>Phase 4: Deployment</h3>
              <p>Production deployment and user training</p>
              <span class="timeline-status">⏳ Pending</span>
            </div>
          </div>
        </div>
      </div>

      <div class="contact-card">
        <h2>📞 Need This Feature?</h2>
        <p>If you need this functionality urgently, please contact the development team.</p>
        <div class="contact-actions">
          <button class="btn btn-primary" @click="$router.push('/')">
            🏠 Return to Home
          </button>
          <button class="btn btn-secondary">
            📧 Contact Support
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.maintenance-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.maintenance-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 20px;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
  border-radius: 12px;
  position: relative;
  overflow: hidden;
}

.maintenance-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="white" opacity="0.1"/></svg>') repeat;
  pointer-events: none;
}

.icon-container {
  position: relative;
  display: inline-block;
  margin-bottom: 20px;
}

.page-icon {
  font-size: 4em;
  display: inline-block;
}

.construction-icon {
  position: absolute;
  top: -10px;
  right: -10px;
  font-size: 1.5em;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.maintenance-header h1 {
  margin: 0 0 15px 0;
  font-size: 2.5em;
  font-weight: 700;
  color: #333;
}

.page-description {
  font-size: 1.2em;
  color: #666;
  margin: 0;
  max-width: 600px;
  margin: 0 auto;
}

.maintenance-content {
  display: grid;
  gap: 25px;
}

.status-card,
.features-card,
.roadmap-card,
.contact-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.status-card h2,
.features-card h2,
.roadmap-card h2,
.contact-card h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.5em;
}

.status-details {
  display: grid;
  gap: 15px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.status-label {
  font-weight: 600;
  color: #495057;
}

.status-value {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: 600;
}

.status-value.development {
  background: #fff3cd;
  color: #856404;
}

.status-value.high {
  background: #f8d7da;
  color: #721c24;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 12px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.feature-item:hover {
  background: #e9ecef;
}

.feature-icon {
  font-size: 1.2em;
}

.feature-text {
  color: #495057;
  font-weight: 500;
}

.roadmap-timeline {
  display: grid;
  gap: 20px;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  position: relative;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 12px;
  top: 25px;
  bottom: -20px;
  width: 2px;
  background: #dee2e6;
}

.timeline-marker {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 3px solid #dee2e6;
  background: white;
  flex-shrink: 0;
  margin-top: 5px;
}

.timeline-item.completed .timeline-marker {
  background: #28a745;
  border-color: #28a745;
}

.timeline-item.current .timeline-marker {
  background: #ffc107;
  border-color: #ffc107;
  animation: pulse-timeline 2s infinite;
}

@keyframes pulse-timeline {
  0% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(255, 193, 7, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0); }
}

.timeline-content {
  flex: 1;
}

.timeline-content h3 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 1.1em;
}

.timeline-content p {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 0.9em;
}

.timeline-status {
  font-size: 0.8em;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 12px;
  background: #f8f9fa;
  color: #495057;
}

.contact-card p {
  margin-bottom: 20px;
  color: #666;
  line-height: 1.6;
}

.contact-actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .maintenance-header h1 {
    font-size: 2em;
  }
  
  .contact-actions {
    flex-direction: column;
  }
  
  .btn {
    text-align: center;
    justify-content: center;
  }
  
  .status-item {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}
</style>