<template>
  <div class="toe-description-page">
    <div class="page-header">
      <h1>TOE Description</h1>
      <p class="page-subtitle">Configure the Target of Evaluation details for your assessment</p>
      <div class="save-status">
        <span v-if="saveStatus === 'saving'" class="status-saving">💾 Saving...</span>
        <span v-else-if="saveStatus === 'saved'" class="status-saved">✅ Saved</span>
        <span v-else-if="saveStatus === 'error'" class="status-error">❌ Error saving</span>
      </div>
    </div>

    <div class="form-container">
      <form @submit.prevent="saveTOEDescription" class="toe-form">
        <!-- Basic Information Section -->
        <div class="form-section">
          <h2>Basic Information</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="toe_name" class="form-label">TOE Name</label>
              <input
                id="toe_name"
                v-model="formData.toe_name"
                type="text"
                class="form-input"
                placeholder="Enter TOE name"
                @input="debouncedSave"
              />
            </div>

            <div class="form-group">
              <label for="toe_vendor" class="form-label">TOE Vendor</label>
              <input
                id="toe_vendor"
                v-model="formData.toe_vendor"
                type="text"
                class="form-input"
                placeholder="Enter vendor name"
                @input="debouncedSave"
              />
            </div>

            <div class="form-group">
              <label for="evaluation_date" class="form-label">Evaluation Date</label>
              <input
                id="evaluation_date"
                v-model="formData.evaluation_date"
                type="text"
                class="form-input"
                placeholder="e.g., January 2024"
                @input="debouncedSave"
              />
            </div>

            <div class="form-group">
              <label for="laboratory_name" class="form-label">Laboratory Name</label>
              <input
                id="laboratory_name"
                v-model="formData.laboratory_name"
                type="text"
                class="form-input"
                placeholder="Enter laboratory name"
                @input="debouncedSave"
              />
            </div>

            <div class="form-group">
              <label for="laboratory_address" class="form-label">Laboratory Address</label>
              <textarea
                id="laboratory_address"
                v-model="formData.laboratory_address"
                class="form-input form-textarea"
                placeholder="Enter laboratory address"
                @input="debouncedSave"
              ></textarea>
            </div>

            <div class="form-group">
              <label for="toe_version" class="form-label">TOE Version</label>
              <input
                id="toe_version"
                v-model="formData.toe_version"
                type="text"
                class="form-input"
                placeholder="e.g., v1.0.0"
                @input="debouncedSave"
              />
            </div>

            <div class="form-group">
              <label for="common_criteria_version" class="form-label">Common Criteria Version</label>
              <input
                id="common_criteria_version"
                v-model="formData.common_criteria_version"
                type="text"
                class="form-input"
                placeholder="e.g., 3.1 Release 5"
                @input="debouncedSave"
              />
            </div>
          </div>
        </div>

        <!-- Rich Text Sections -->
        <div class="form-section">
          <h2>Detailed Information</h2>
          
          <WysiwygEditor
            v-model="formData.vendor_address"
            label="Vendor Address"
            placeholder="Enter detailed vendor address and contact information..."
            @update:modelValue="debouncedSave"
          />

          <WysiwygEditor
            v-model="formData.evaluation_personnel"
            label="Evaluation Personnel"
            placeholder="List evaluation team members, roles, and qualifications..."
            @update:modelValue="debouncedSave"
          />

          <WysiwygEditor
            v-model="formData.protection_profile_module"
            label="Protection Profile Module"
            placeholder="Describe the protection profile and security functional requirements..."
            @update:modelValue="debouncedSave"
          />

          <WysiwygEditor
            v-model="formData.toe_description"
            label="TOE Description"
            placeholder="Provide a comprehensive description of the Target of Evaluation..."
            @update:modelValue="debouncedSave"
          />
        </div>

        <!-- Save Button -->
        <div class="form-actions">
          <button 
            type="submit" 
            class="save-button"
            :disabled="saveStatus === 'saving'"
          >
            <span v-if="saveStatus === 'saving'">Saving...</span>
            <span v-else>Save TOE Description</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { debounce } from 'lodash-es'
import WysiwygEditor from '../../components/WysiwygEditor.vue'
import ApiService from '../../services/api'

interface TOEDescriptionData {
  id?: string
  toe_name: string
  toe_vendor: string
  evaluation_date: string
  laboratory_address: string
  laboratory_name: string
  toe_version: string
  common_criteria_version: string
  vendor_address: string
  evaluation_personnel: string
  protection_profile_module: string
  toe_description: string
}

const formData = reactive<TOEDescriptionData>({
  toe_name: '',
  toe_vendor: '',
  evaluation_date: '',
  laboratory_address: '',
  laboratory_name: '',
  toe_version: '',
  common_criteria_version: '',
  vendor_address: '',
  evaluation_personnel: '',
  protection_profile_module: '',
  toe_description: ''
})

const saveStatus = ref<'idle' | 'saving' | 'saved' | 'error'>('idle')
const currentToeId = ref<string | null>(null)

// Load existing TOE description on mount
onMounted(async () => {
  try {
    const existingToe = await ApiService.getTOEDescription()
    if (existingToe) {
      Object.assign(formData, existingToe)
      currentToeId.value = existingToe.id
    }
  } catch (error) {
    console.error('Error loading TOE description:', error)
  }
})

// Save TOE description
const saveTOEDescription = async () => {
  saveStatus.value = 'saving'
  try {
    let result
    if (currentToeId.value) {
      // Update existing
      result = await ApiService.updateTOEDescription(currentToeId.value, formData)
    } else {
      // Create new
      result = await ApiService.createTOEDescription(formData)
      currentToeId.value = result.id
    }
    
    saveStatus.value = 'saved'
    
    // Reset status after 3 seconds
    setTimeout(() => {
      if (saveStatus.value === 'saved') {
        saveStatus.value = 'idle'
      }
    }, 3000)
  } catch (error) {
    console.error('Error saving TOE description:', error)
    saveStatus.value = 'error'
    
    // Reset status after 5 seconds
    setTimeout(() => {
      if (saveStatus.value === 'error') {
        saveStatus.value = 'idle'
      }
    }, 5000)
  }
}

// Debounced auto-save function
const debouncedSave = debounce(() => {
  saveTOEDescription()
}, 2000) // Save 2 seconds after user stops typing
</script>

<style scoped>
.toe-description-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #6b7280;
  font-size: 1.1rem;
  margin: 0;
}

.save-status {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  min-width: 120px;
  justify-content: flex-end;
}

.form-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.toe-form {
  padding: 2rem;
}

.form-section {
  margin-bottom: 3rem;
}

.form-section:last-child {
  margin-bottom: 0;
}

.form-section h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 14px;
  line-height: 1.5;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  font-family: 'Inter', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.form-actions {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
}

.save-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
  font-family: 'Inter', sans-serif;
}

.save-button:hover:not(:disabled) {
  background-color: #2980b9;
}

.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive design */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .save-status {
    margin-top: 1rem;
    justify-content: flex-start;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .toe-form {
    padding: 1.5rem;
  }
}
</style>