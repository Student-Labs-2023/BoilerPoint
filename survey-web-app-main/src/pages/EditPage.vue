<template>
  <q-page class="bg-grey-3 column items-center">
    <SurveyEdit
    :question="question"
    :correctAnswer="correctAnswer"
    :choices="choices"
    :imageURL="imageURL"
    :surveyId="surveyId"
    @saveSurveyChanges="(changes) => sendSurveyChanges(changes)"
    />
  </q-page>
</template>

<script>
import SurveyEdit from 'src/components/SurveyEdit.vue'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { WebApp } from "@grammyjs/web-app";

export default {
  name: 'EditPage',
  components: {
    SurveyEdit
  },
  setup() {
    const route = useRoute()
    const imageURL = ref('')
    const question = ref('')
    const choices = ref([])
    const correctAnswer = ref(null)
    const surveyId = ref(null)
    
    const queryParams = route.query
    imageURL.value = queryParams.imageURL
    question.value = queryParams.question
    if (queryParams.choices) {
      choices.value = queryParams.choices.split('|')
    }
    correctAnswer.value = Number(queryParams.correctAnswer)
    surveyId.value = Number(queryParams.surveyId)

    // mount происходит вначале в child, а потом в parent
    onMounted(() => {
      WebApp.ready();
    })
    return {
      question,
      choices,
      correctAnswer,
      imageURL,
      surveyId,

      sendSurveyChanges(changes) {
        console.log(changes)
        window.Telegram.WebApp.sendData(JSON.stringify(changes))
      }
    }
  }
}
</script>