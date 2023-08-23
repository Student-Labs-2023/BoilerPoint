<template>
  <q-page class="bg-grey-3 column items-center">
    <Survey
    :surveyData="surveyData"
    @answersSelected="(answers) => sendSelectedAnswers(answers)"
    />
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Survey from 'src/components/Survey.vue'

export default {
  name: 'PreviewPage',
  components: {
    Survey
  },
  setup() {
    const route = useRoute()
    const surveyData = ref([])
    surveyData.value = JSON.parse(route.query.json).surveyData
    

    onMounted(() => {
      // WebApp.ready();
      window.Telegram.WebApp.MainButton.show()
      window.Telegram.WebApp.MainButton.text = "Отправить"
    })
    return {
      // question,
      // choices,
      // correctAnswer,
      // surveyId,
      surveyData,

      sendSelectedAnswers(answers) {
        console.log(JSON.stringify(answers))
        window.Telegram.WebApp.sendData(JSON.stringify(answers))
      }
    }
  }
}
</script>
