<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToSection = (section: string) => {
  switch(section) {
    case 'testing':
      router.push('/tools')
      break
    case 'documentation':
      router.push('/documentation')
      break
    case 'database':
      router.push('/settings/database')
      break
  }
}
</script>

<template>
  <div class="home-page">
    <div class="welcome-section">
      <h1>Welcome to NGE AI Testing Platform</h1>
      <p class="subtitle">
        Your comprehensive solution for AI device testing based on Common Criteria standards
      </p>
    </div>

    <div class="main-actions">
      <div class="action-card" @click="navigateToSection('testing')">
        <div class="card-icon">🔧</div>
        <h2>Testing Tools</h2>
        <p>Access various testing tools including network diagnostics, security tests, and AI model validation</p>
        <div class="card-features">
          <span class="feature">• Ping Test</span>
          <span class="feature">• Network Analysis</span>
          <span class="feature">• Security Scanning</span>
        </div>
        <button class="action-button">Get Started</button>
      </div>

      <div class="action-card" @click="navigateToSection('documentation')">
        <div class="card-icon">📚</div>
        <h2>Common Criteria Documentation</h2>
        <p>Comprehensive documentation management for Common Criteria compliance and evaluation</p>
        <div class="card-features">
          <span class="feature">• TOE Description</span>
          <span class="feature">• Security Requirements</span>
          <span class="feature">• Assurance Activities</span>
        </div>
        <button class="action-button">View Docs</button>
      </div>

      <div class="action-card" @click="navigateToSection('database')">
        <div class="card-icon">💾</div>
        <h2>Database</h2>
        <p>Manage test data, device profiles, and results with advanced search and analytics capabilities</p>
        <div class="card-features">
          <span class="feature">• Test Cases</span>
          <span class="feature">• Device Profiles</span>
          <span class="feature">• Results Analysis</span>
        </div>
        <button class="action-button">Manage Data</button>
      </div>
    </div>

    <div class="stats-section">
      <h2>Platform Overview</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">24</div>
          <div class="stat-label">Active Test Cases</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">12</div>
          <div class="stat-label">Registered Devices</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">156</div>
          <div class="stat-label">Tests Completed</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">98%</div>
          <div class="stat-label">Success Rate</div>
        </div>
      </div>
    </div>

    <div class="quick-access">
      <h2>Quick Access</h2>
      <div class="quick-links">
        <router-link to="/tools/ping" class="quick-link">
          <span class="link-icon">📡</span>
          <span>Ping Test</span>
        </router-link>
        <router-link to="/documentation/toe-description" class="quick-link">
          <span class="link-icon">📋</span>
          <span>TOE Description</span>
        </router-link>
        <router-link to="/settings" class="quick-link">
          <span class="link-icon">⚙️</span>
          <span>Settings</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
}

.welcome-section h1 {
  margin: 0 0 15px 0;
  font-size: 2.5em;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2em;
  opacity: 0.9;
  margin: 0;
  max-width: 600px;
  margin: 0 auto;
}

.main-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
  margin-bottom: 50px;
}

.action-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.card-icon {
  font-size: 3em;
  margin-bottom: 20px;
  text-align: center;
}

.action-card h2 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.5em;
  text-align: center;
}

.action-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
  text-align: center;
}

.card-features {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 25px;
}

.feature {
  color: #555;
  font-size: 0.9em;
  padding-left: 10px;
}

.action-button {
  width: 100%;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.stats-section {
  margin-bottom: 40px;
}

.stats-section h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 2em;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
}

.stat-number {
  font-size: 2.5em;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 10px;
}

.stat-label {
  color: #666;
  font-size: 0.9em;
  font-weight: 500;
}

.quick-access {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.quick-access h2 {
  margin: 0 0 25px 0;
  color: #333;
  text-align: center;
}

.quick-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.quick-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px 20px;
  background: #f8f9fa;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.quick-link:hover {
  background: #e9ecef;
  border-color: #667eea;
  color: #667eea;
}

.link-icon {
  font-size: 1.2em;
}

@media (max-width: 768px) {
  .main-actions {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .quick-links {
    grid-template-columns: 1fr;
  }
  
  .welcome-section h1 {
    font-size: 2em;
  }
  
  .subtitle {
    font-size: 1em;
  }
}
</style>