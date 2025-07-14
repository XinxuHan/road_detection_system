<template>
  <div class="llm-result-box markdown-body" :style="customStyle">
    <div v-if="!props.content || props.content.trim() === ''" class="placeholder">
      {{ props.placeholder || 'The LLM analysis results will be displayed here' }}
    </div>
    <div v-else v-html="renderedContent"></div>
  </div>
</template>


<script setup lang="ts">
import { computed } from "vue";
import { marked } from "marked";

const props = defineProps<{
  content: string;
  style?: string | Record<string, string>;
  placeholder?: string;
}>();


const renderedContent = computed(() => marked.parse(props.content || ""));

// 样式支持对象或字符串
const customStyle = computed(() =>
  typeof props.style === "string" ? props.style : {
    border: "1px solid #ccc",
    borderRadius: "6px",
    padding: "16px",
    fontFamily: "monospace",
    whiteSpace: "pre-wrap",
    backgroundColor: "#fafafa",
    ...props.style,
  }
);
</script>

<style scoped>
.markdown-body h1,
.markdown-body h2 {
  font-weight: bold;
  border-bottom: 1px solid #ddd;
  padding-bottom: 4px;
  margin-top: 16px;
}

.markdown-body ul {
  padding-left: 20px;
  list-style-type: disc;
  margin: 10px 0;
}

.markdown-body code {
  background: #f4f4f4;
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 90%;
}
</style>