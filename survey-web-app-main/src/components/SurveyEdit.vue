<template>
  <q-card class="survey-card" flat bordered>
    <img :src="imageURL" :onload="hideLoading" :onerror="hideLoading">
    <q-form
      ref="questionForm"
      class="q-gutter-md"
    >
      <q-file color="orange" standout bottom-slots
        label="Загрузить изображение для опроса"
        @update:model-value="onImageLoaded"
        v-model="loaderModel"
        class="image-loader"
      >
        <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>
        <template v-slot:after>
          <q-btn round dense flat icon="clear" @click="clearImage()" />
        </template>
        <template v-slot:hint>
          Для удаления изображения нажмите на крестик в правой части загрузчика
        </template>
      </q-file>
      <q-input
        filled
        v-model="question"
        label="Заголовок вопроса *"
        hint=""
        lazy-rules
        :rules="[ val => val && (val.length > 0 || val.value.length > 0) || 'Пожалуйста, введите что-нибудь']"
        counter
        maxlength="64"
      />
      
      <ul class="choices-list bg-grey-2">
        <q-input 
          v-for="(choice, index) in choices"
          filled
          label="Ответ *"
          v-model="choices[index]"
          hint=""
          lazy-rules
          :rules="[ val => val && (val.length > 0 || val.value.length > 0) || 'Пожалуйста, введите что-нибудь']"
          counter
          maxlength="32"
          class="choice"
        >
          <template v-slot:append>
            <q-btn round dense flat icon="close" @click="() => {onDeleteChoice(index)}"/>
          </template>
          <template v-slot:after>
            <q-btn :class="{'bg-green-3': index==correctAnswer}" round dense flat icon="check" @click="() => {onSelectCorrectAnswer(index)}"/>
          </template>
        </q-input>
      </ul>  
      <div class="column items-center">
        <q-btn label="Добавить ответ" color="secondary" class="center" @click="onChoiceAdd"/>
      </div>
      <q-input
        id="number-points"
        v-model.number="numberPoints"
        type="number"
        filled
        style="max-width: 200px"
        hint="Число баллов за верный ответ"
        :rules="[ val => (val || (val === 0 || val.value === 0)) && (val >= 0 || val.value >= 0) || 'Пожалуйста, укажите число баллов за верный ответ']"
      />
      <q-separator />
      <!-- <div>
        <q-btn label="Сохранить" type="submit" color="primary"/>
      </div> -->
    </q-form>
  </q-card>
</template>


<script>
import { useQuasar, Loading } from 'quasar'
import { ref } from 'vue'
import { getImageUrlById, uploadImageById, removeOrIgnoreImageById } from 'src/services/imageService'


export default {
  name: 'SurveyEdit',
  emits: ['saveSurveyChanges'],
  props: {
    surveyData: Object
  }, 
  setup(props, context) {
    const question = ref('')
    const choices = ref([])
    const correctAnswer = ref(null)
    const questionId = ref(null)
    const imageURL = ref('')
    const numberPoints = ref(0)
    const questionForm = ref(null)
    const $q = useQuasar()
    // watch(() => props.question, () => {
    //   question.value = props.question
    // })
    // что-то типо того

    const surveyData = props.surveyData[0]
    console.log(surveyData)
    question.value = surveyData.question 
    for (let choice of surveyData.choices) {
      choices.value.push(choice)  
    };
    correctAnswer.value = surveyData.correctAnswer
    questionId.value = surveyData.questionId
    if (surveyData.numberPoints) {
      numberPoints.value = surveyData.numberPoints
    }
    
    const loaderModel = ref(null)
    Loading.show()
    getImageUrlById(questionId.value) 
    .then((response) => {
      if (response.data) {
        const url = response.data.signedUrl
        imageURL.value = url
      }
      // Loading.hide()
    })
    function checkUniqueChoices() {
      const choicesSet = new Set(choices.value)
      return choices.value.length === choicesSet.size
    }

    function showWarning(text) {
      $q.notify({
        color: 'red-5',
        textColor: 'white',
        icon: 'warning',
        message: text
      })
    }
    
    window.Telegram.WebApp.onEvent('mainButtonClicked', async function(){
      if (!correctAnswer.value && correctAnswer.value !== 0) {
        showWarning('Необходимо создать и выбрать как минимум один правильный ответ')
      }
      else if (!checkUniqueChoices()) {
        showWarning('Все варианты ответов должны быть разными')
      }
      
      else {
        questionForm.value.validate().then(async function(success){
          if (success) {
            Loading.show()  
            if (loaderModel.value) {
              let { data, error } = await uploadImageById(questionId.value, loaderModel.value)
              // console.log(data, error)
            }
            if (!imageURL.value) {
              let { data, error } = await removeOrIgnoreImageById(questionId.value)
              // console.log(data, error)
            }
            const response = {}
            response.question = question.value
            response.choices = choices.value
            response.correctAnswer = correctAnswer.value
            response.numberPoints = numberPoints.value
            console.log(response)
            window.Telegram.WebApp.sendData(JSON.stringify(response))
            $q.notify({
              color: 'green-5',
              textColor: 'white',
              icon: 'check',
              message: 'Сохранено'
            })
          }
        })
      }
    })

    return {
      loaderModel,
      imageURL,
      question,
      choices,
      correctAnswer: correctAnswer,
      questionId,
      numberPoints,
      questionForm,
      checkUniqueChoices,
      showWarning,

      async onImageLoaded(image) {
        if (image) {
          imageURL.value = URL.createObjectURL(image)
        }
        else {
          imageURL.value = ''
        }
      },
      clearImage() {
        imageURL.value = null
        loaderModel.value = null
      },
      hideLoading() {
        Loading.hide()
      },
      
      onChoiceAdd() {
        choices.value.push(ref(''))
      },
      onDeleteChoice(index) {
        choices.value.splice(index, 1)
        correctAnswer.value = null
      },
      onSelectCorrectAnswer(index) {
        correctAnswer.value = index
      }
    } 
  }
}
</script>

<style scoped> 
.image-loader {
  margin-bottom: 20px;
}
.choices-list {
  padding-left: 0px;
}
.choice {
  margin-bottom: 20px;
}


</style>