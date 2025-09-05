<template>
  <div class="wysiwyg-editor">
    <label v-if="label" :for="inputId" class="form-label">{{ label }}</label>
    <QuillEditor
      :id="inputId"
      v-model:content="content"
      :options="editorOptions"
      content-type="html"
      @update:content="handleUpdate"
      class="quill-editor"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

interface Props {
  modelValue?: string
  label?: string
  placeholder?: string
  id?: string
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: 'Enter text...',
  id: ''
})

const emit = defineEmits<Emits>()

const content = ref(props.modelValue)
const inputId = computed(() => props.id || `wysiwyg-${Math.random().toString(36).substr(2, 9)}`)

const editorOptions = {
  theme: 'snow',
  placeholder: props.placeholder,
  modules: {
    toolbar: [
      [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'color': [] }, { 'background': [] }],
      [{ 'font': [] }],
      [{ 'align': [] }],
      ['blockquote', 'code-block'],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      [{ 'indent': '-1'}, { 'indent': '+1' }],
      ['link', 'image'],
      ['clean']
    ]
  }
}

const handleUpdate = (value: string) => {
  content.value = value
  emit('update:modelValue', value)
}

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  if (newValue !== content.value) {
    content.value = newValue
  }
})
</script>

<style scoped>
.wysiwyg-editor {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

:deep(.quill-editor) {
  border-radius: 0.375rem;
  border: 1px solid #d1d5db;
}

:deep(.ql-toolbar) {
  border-top: 1px solid #d1d5db;
  border-left: 1px solid #d1d5db;
  border-right: 1px solid #d1d5db;
  border-bottom: none;
  border-top-left-radius: 0.375rem;
  border-top-right-radius: 0.375rem;
}

:deep(.ql-container) {
  border-bottom: 1px solid #d1d5db;
  border-left: 1px solid #d1d5db;
  border-right: 1px solid #d1d5db;
  border-top: none;
  border-bottom-left-radius: 0.375rem;
  border-bottom-right-radius: 0.375rem;
  font-family: 'Inter', sans-serif;
}

:deep(.ql-editor) {
  min-height: 120px;
  font-size: 14px;
  line-height: 1.6;
}

:deep(.ql-editor.ql-blank::before) {
  font-style: normal;
  color: #9ca3af;
}
</style>