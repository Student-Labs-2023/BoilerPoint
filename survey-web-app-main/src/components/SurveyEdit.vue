<template>
  <q-card class="survey-card" flat bordered>
    <img :src="imageURL">
    <q-form
      @submit="onSubmit"
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
        label="Заголовок опроса *"
        hint=""
        lazy-rules
        :rules="[ val => val && (val.length > 0 || val.value.length > 0) || 'Пожалуйста, введите что-нибудь']"
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
          class="choice"
        >
          <template v-slot:append>
            <q-btn round dense flat icon="close" @click="() => {onDeleteChoice(index)}"/>
          </template>
          <template v-slot:after>
            <q-btn :class="{'bg-green-3': index==correctAnswerIndex}" round dense flat icon="check" @click="() => {onSelectCorrectAnswer(index)}"/>
          </template>
        </q-input>
      </ul>
      <div class="column items-center">
        <q-btn label="Добавить ответ" color="secondary" class="center" @click="onChoiceAdd"/>
      </div>
      <q-separator />
      <div>
        <q-btn label="Сохранить" type="submit" color="primary"/>
      </div>
    </q-form>
  </q-card>
</template>


<script>
import { useQuasar, Loading, QSpinnerGears } from 'quasar'
import { ref, onMounted } from 'vue'
import { getImageUrlById, uploadImageById, removeOrIgnoreImageById } from 'src/services/imageService'


export default {
  name: 'SurveyEdit',
  emits: ['saveSurveyChanges'],
  props: {
    imageURL: String,
    question: String,
    choices: Array,
    correctAnswer: Number,
    surveyId: Number,
  }, 
  setup(props, context) {
    const imageURL = ref('')
    const question = ref(null)
    const choices = ref([])
    const correctAnswerIndex = ref(null)
    const surveyId = ref(null)
    const $q = useQuasar()
    // watch(() => props.question, () => {
    //   question.value = props.question
    // })
    // что-то типо того
    question.value = props.question 
    for (let choice of props.choices) {
      choices.value.push(choice)  
    };
    correctAnswerIndex.value = props.correctAnswer
    surveyId.value = props.surveyId

    Loading.show()
    getImageUrlById(surveyId.value) 
    .then((response) => {
      if (response.data) {
        const url = response.data.signedUrl
        imageURL.value = url
      }
      Loading.hide()
    })
    
    const loaderModel = ref(null)
    return {
      loaderModel,
      imageURL,
      question,
      choices,
      correctAnswerIndex,
      surveyId,
      
      async onImageLoaded(image) {
        console.log(image)
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
      async onSubmit() {
        if (!correctAnswerIndex.value && correctAnswerIndex.value != 0) {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: 'Необходимо создать и выбрать один правильный ответ'
          })
        }
        else {
          $q.notify({
            color: 'green-5',
            textColor: 'white',
            icon: 'check',
            message: 'Сохранено'
          })  
          if (loaderModel.value) {
            let { data, error } = await uploadImageById(surveyId.value, loaderModel.value)
            console.log(data, error)
          }
          else {
            let { data, error } = await removeOrIgnoreImageById(surveyId.value)
            console.log(data, error)
          }
          const response = {}
          response.question = question.value
          response.choices = choices.value
          response.correctAnswerIndex = correctAnswerIndex.value
          context.emit('saveSurveyChanges', response)
        }
      },
      onChoiceAdd() {
        choices.value.push(ref(''))
      },
      onDeleteChoice(index) {
        choices.value.splice(index, 1)
        correctAnswerIndex.value = null
      },
      onSelectCorrectAnswer(index) {
        correctAnswerIndex.value = index
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