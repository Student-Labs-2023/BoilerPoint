<template>
  <div ref="container">
    <pre ref="locator"></pre>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

const locator = ref(null)
const container = ref(null)

onMounted(() => {

  function rewireConsoleOutput() {
    fixLoggingFunc("log");
    fixLoggingFunc("debug");
    fixLoggingFunc("warn");
    fixLoggingFunc("error");
    fixLoggingFunc("info");

    function fixLoggingFunc(name) {
      console["old" + name] = console[name];
      console[name] = function (...args) {
        const output = produceOutput(name, args);
        const eleLog = locator.value;

        const eleContainerLog = container.value;
        const isScrolledToBottom =
          eleContainerLog.scrollHeight - eleContainerLog.clientHeight <=
          eleContainerLog.scrollTop + 1;
        eleLog.innerHTML += output + "<br>";
        if (isScrolledToBottom) {
          eleContainerLog.scrollTop =
            eleContainerLog.scrollHeight - eleContainerLog.clientHeight;
        }

        console["old" + name].apply(undefined, args);
      };
    }

    function produceOutput(name, args) {
      return args.reduce((output, arg) => {
        return (
          output +
          '<span class="log-' +
          typeof arg +
          " log-" +
          name +
          '">' +
          (typeof arg === "object" && (JSON || {}).stringify
            ? JSON.stringify(arg)
            : arg) +
          "</span>&nbsp;"
        );
      }, "");
    }
  }

  rewireConsoleOutput();

  console.log('init...');
})
</script>

<style>
#log-container {
  overflow: auto;
  height: 250px;
}

.log-warn {
  color: orange
}

.log-debug {
  color: pink
}

.log-error {
  color: red
}

.log-info {
  color: skyblue
}

.log-log {
  color: silver
}

.log-warn,
.log-error {
  font-weight: bold;
}
</style>