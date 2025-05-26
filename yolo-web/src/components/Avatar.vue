<template>





</template>

<script setup lang="ts">
import { reactive, toRefs } from 'vue'
const state = reactive({
  circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
})

const { circleUrl } = toRefs(state)
</script>


<style scoped>

</style>