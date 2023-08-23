<template>
  <q-form>
    <q-card class="survey-card" flat bordered v-for="question in surveyData">
      <div class="column items-center">
        <q-spinner
          v-if="question.isLoading"
          color="primary"
          size="3em"
          :thickness="10"
        />
      </div>
      <img :src="question.imageUrl" :onload="() => { question.isLoading = false }" :class="{ unvisible: question.isLoading }">
      <q-card-section>
        <div class="text-h6">{{ question.question }}</div>
      </q-card-section>
      <q-list>
        <div>
          <div v-for="(choice, index) in question.choices">
            <q-radio name="answer" v-model="question.answer" :val="index" :label="choice" />
          </div>
        </div>
      </q-list>
    </q-card>
    <!-- <div class="column items-center q-my-xl">
      <q-btn label="Сохранить результат" type="submit" color="primary" size="lg"/>
    </div> -->
  </q-form>  
</template>

<script>
import { useQuasar } from 'quasar'
import { ref } from 'vue'
import { setQuestionImageUrl } from 'src/services/imageService'


export default {
  name: 'Survey',
  props: {
    surveyData: Object,
  },
  setup(props, context) {
    const surveyData = ref(null)
    surveyData.value = props.surveyData
    const $q = useQuasar()
    // const answer = ref(null)

    for (let question of surveyData.value) {
      question.isLoading = true
      console.log(question.isLoading)
      question.imageUrl = ref('')
      question.answer = ref(null)
      setQuestionImageUrl(question, question.questionId)
    }
    // const imageURL = ref('')
    // const surveyId = props.surveyId
    
    // Loading.show()
    function checkAnswers() {
      for (let question of surveyData.value) {
        console.log(question.answer)
        if (!question.answer && question.answer !== 0) {
          return false
        }
      }
      return true
    }

    window.Telegram.WebApp.onEvent('mainButtonClicked', async function() {
      if (!checkAnswers()) {
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'Необходимо выбрать все варианты ответа'
        })
      }
      else {
        
        $q.notify({
          color: 'green-5',
          icon: 'check',
          message: 'Ответ принят',
          textColor: 'white',
        })
        console.log(surveyData.value)
        const response = {}
        for (let question of surveyData.value) {
          response[question.questionId] = question.answer
        }
        console.log(response)
        // response.answer = answer.value
        window.Telegram.WebApp.sendData(JSON.stringify(response))
        // context.emit('answersSelected', response)
      }
    })

    return {
      surveyData,
      checkAnswers,
    }
  },
  
}
</script>
<style scoped>
.survey-card {
  max-width: 100vw;
  width: 500px;
}
.unvisible {
  visibility: hidden;
}
</style>
