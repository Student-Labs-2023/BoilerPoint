<template>
  <q-page class="bg-grey-3 column items-center">
    <SurveyEdit
    :surveyData="surveyData"
    @saveSurveyChanges="(changes) => sendSurveyChanges(changes)"
    />
  </q-page>
</template>

<script>
import SurveyEdit from 'src/components/SurveyEdit.vue'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
// import { WebApp } from "@grammyjs/web-app";
import { Loading } from 'quasar';

export default {
  name: 'EditPage',
  components: {
    SurveyEdit
  },
  setup() {
    const route = useRoute()
    const surveyData = ref(null)
    surveyData.value = JSON.parse(route.query.json).surveyData

    // mount происходит вначале в child, а потом в parent
    onMounted(() => {
      // console.log(WebApp.version)
      // WebApp.ready();
      window.Telegram.WebApp.MainButton.show()
      window.Telegram.WebApp.MainButton.text = "Сохранить вопрос"
      // WebApp.expand()
    })
    return {
      surveyData,

      sendSurveyChanges(changes) {
        // console.log(JSON.stringify(changes))
        Loading.hide()
        
        
      }
    }
  }
}
</script>