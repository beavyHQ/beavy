
import { CALL_API } from 'middleware/api';
import { make_url } from 'utils';

export const STORY_SUBMIT_REQUEST = 'STORY_SUBMIT_REQUEST';
export const STORY_SUBMIT_SUCCESS = 'STORY_SUBMIT_SUCCESS';
export const STORY_SUBMIT_FAILURE = 'STORY_SUBMIT_FAILURE';

function submit_story(payload) {
  console.log("!!!!!!", payload);
  return {
    [CALL_API]: {
      types: [STORY_SUBMIT_REQUEST, STORY_SUBMIT_SUCCESS, STORY_SUBMIT_FAILURE],
      endpoint: '/submit/',
      key: "story",
      params: {
        method: 'POST',
        body: JSON.stringify(payload)
      }
    }
  };
}

export function submitStory(payload){
  return (dispatch, getState) => {
    return dispatch(submit_story(payload));
  }
}