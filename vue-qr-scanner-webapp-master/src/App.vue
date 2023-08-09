<template>
  <div>
    <div class="layout">
      <v-progress-circular :size="100" :width="10" color="grey" indeterminate></v-progress-circular>
    </div>
  </div>
</template>

<script setup>
import ConsoleOutput from './ConsoleOutput.vue'
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import { WebApp } from "@grammyjs/web-app";

const result = ref();

const onDecode = ({ data }) => {
  if (data === result.value) {
    return
  }

  result.value = data;
  WebApp.HapticFeedback.impactOccurred('medium')
  WebApp.closeScanQrPopup()
};

const onSave = () => {
  WebApp.sendData(result.value)
}

const onCancel = () => {
  WebApp.showScanQrPopup({})
}

watch(result, async (newValue) => onSave())

onMounted(() => {
  WebApp.expand()
  WebApp.onEvent("qrTextReceived", onDecode);
  WebApp.showScanQrPopup({})
})

onBeforeUnmount(() => {
  WebApp.offEvent('qrTextReceived', onDecode)
})
</script>

<style scoped>
.layout {
  height: var(--tg-viewport-height);
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading {
  color: var(--tg-theme-text-color);
  font-weight: bold;
  font-size: 2rem;
  text-align: center;
}
</style>
