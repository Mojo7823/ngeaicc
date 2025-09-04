<template>
  <div class="dashboard">
    <h1>AI Testing Standard Platform</h1>
    <p class="subtitle">Common Criteria Based Testing Dashboard</p>
    
    <div class="main-buttons">
      <router-link to="/tools/ping" class="main-button testing-tools">
        <div class="button-icon">🛠️</div>
        <h3>Testing Tools</h3>
        <p>Ping test, network diagnostics, and security testing tools</p>
      </router-link>
      
      <router-link to="/documentation/toe-description" class="main-button documentation">
        <div class="button-icon">📚</div>
        <h3>Common Criteria Documentation</h3>
        <p>TOE descriptions, assurance activities, and guidance documents</p>
      </router-link>
      
      <router-link to="/settings/database" class="main-button database">
        <div class="button-icon">🗄️</div>
        <h3>Database</h3>
        <p>Database management, settings, and data administration</p>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
// Dashboard home page
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 2.5em;
}

.subtitle {
  text-align: center;
  color: #7f8c8d;
  margin-bottom: 60px;
  font-size: 1.1em;
}

.main-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.main-button {
  background: white;
  border: 2px solid #ecf0f1;
  border-radius: 12px;
  padding: 40px 30px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  display: block;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.main-button:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border-color: #3498db;
}

.testing-tools:hover {
  border-color: #e74c3c;
}

.documentation:hover {
  border-color: #2ecc71;
}

.database:hover {
  border-color: #f39c12;
}

.button-icon {
  font-size: 3em;
  margin-bottom: 20px;
}

.main-button h3 {
  margin: 0 0 15px 0;
  color: #2c3e50;
  font-size: 1.3em;
}

.main-button p {
  margin: 0;
  color: #7f8c8d;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .main-buttons {
    grid-template-columns: 1fr;
  }
  
  h1 {
    font-size: 2em;
  }
}
</style>