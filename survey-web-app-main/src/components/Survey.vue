<template>
  <q-card class="survey-card" flat bordered>
    <img :src="imageURL">
    <q-card-section>
      <div class="text-h6">{{ question }}</div>
    </q-card-section>
    <q-list>
      <q-form @submit.prevent="onSubmit" class="q-gutter-md">
        <div v-for="(choice, index) in choices">
          <q-radio name="answer" v-model="answer" :val="index" :label="choice" />
        </div>
        <div>
          <q-btn label="Ответить" type="submit" color="primary"/>
        </div>
      </q-form>
    </q-list>
    <q-card
      v-if="submitResult.length > 0"
      flat bordered
      class="q-mt-md"
      :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'"
    >
      <q-card-section class="row q-gutter-sm items-center">
        <div
          v-for="(item, index) in submitResult"
          :key="index"
          class="q-px-sm q-py-xs bg-green-3 rounded-borders text-center text-no-wrap"
        >Ответ принят</div>
      </q-card-section>
    </q-card>
  </q-card>
</template>

<script>
import { useQuasar, Loading } from 'quasar'
import { ref } from 'vue'
import { getImageUrlById } from 'src/services/imageService'


export default {
  name: 'Survey',
  props: {
    imageURL: String,
    question: String,
    choices: Array,
    surveyId: Number,
  },
  setup(props, context) {
    const submitResult = ref([])
    const answer = ref(null)
    const imageURL = ref('')
    console.log(props.surveyId)
    const surveyId = props.surveyId
    Loading.show()
    getImageUrlById(surveyId)
    .then((response) => {
      if (response.data) {
        const url = response.data.signedUrl
        imageURL.value = url
      }
      Loading.hide()
    })

    const $q = useQuasar()
    return {
      answer,
      submitResult,
      imageURL,
      onSubmit() {
        if (!answer.value && answer.value != 0) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: 'Необходимо выбрать один вариант ответа'
          })
        }
        else {
          $q.notify({
            color: 'green-5',
            textColor: 'white',
            icon: 'check',
            message: 'Ответ принят'
          })
          const response = {}
          response.answer = answer.value
          context.emit('answerSelected', response)
        }
      },
    }
  },
  
}
</script>
