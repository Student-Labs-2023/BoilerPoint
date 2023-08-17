<template>
  <q-page class="bg-grey-3 column items-center">
    <Survey 
    :imageURL="imageURL"
    :question="question"
    :choices="choices"
    :surveyId="surveyId"
    @answerSelected="(choice) => sendSelectedAnswer(choice)"
    />
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Survey from 'src/components/Survey.vue'
import { WebApp } from "@grammyjs/web-app";

console.log(WebApp.initData);
// same as
console.log(window.Telegram.WebApp.initData);

export default {
  name: 'PreviewPage',
  components: {
    Survey
  },
  setup() {
    const route = useRoute()
    const question = ref('')
    const choices = ref([])
    const correctAnswer = ref(null)
    const surveyId = ref(null)
    const imageURL = ref('')

    const queryParams = route.query
    imageURL.value = queryParams.imageURL
    question.value = queryParams.question
    choices.value = queryParams.choices.split('|')
    surveyId.value = Number(queryParams.surveyId)

    onMounted(() => {
      WebApp.ready();
    })
    return {
      question,
      choices,
      correctAnswer,
      imageURL,
      surveyId,

      sendSelectedAnswer(choice) {
        window.Telegram.WebApp.sendData(JSON.stringify(choice))
      }
    }
  }
}
</script>
