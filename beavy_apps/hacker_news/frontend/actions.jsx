
import { CALL_API } from 'middleware/api'
import { STORY_SUBMIT, STORY_SUBMIT_REQUEST, STORY_SUBMIT_SUCCESS, STORY_SUBMIT_FAILURE } from './consts'

function submit_story (payload) {
  return {
    [CALL_API]: {
      types: [STORY_SUBMIT_REQUEST, STORY_SUBMIT_SUCCESS, STORY_SUBMIT_FAILURE],
      endpoint: '/submit/',
      key: STORY_SUBMIT,
      params: {
        method: 'POST',
        body: JSON.stringify(payload)
      }
    }
  }
}

export function submitStory (payload) {
  return (dispatch, getState) => {
    return dispatch(submit_story(payload))
  }
}
