import { supabase } from 'src/services/supabaseClient'


export function getImageUrlById(surveyId) {
  return supabase.storage
  .from('survey-preview')
  .createSignedUrl(`previews/${surveyId}/preview`, 600)
}


export async function setQuestionImageUrl(question, questionId) {
  const response = await getImageUrlById(questionId)
  if (!response.data) {
    question.isLoading = false
  }
  question.imageUrl = response.data.signedUrl
}


export function uploadImageById(surveyId, image) {
  return supabase.storage
  .from('survey-preview')
  .upload(`previews/${surveyId}/preview`, image, { upsert: true })
}


export function removeOrIgnoreImageById(surveyId) {
  return supabase.storage
  .from('survey-preview')
  .remove([`previews/${surveyId}/preview`])
}

