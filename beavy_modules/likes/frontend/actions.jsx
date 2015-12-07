
import { CALL_API } from 'middleware/api'
import { make_url } from 'utils'

export const USER_LIKES_REQUEST = 'USER_LIKES_REQUEST'
export const USER_LIKES_SUCCESS = 'USER_LIKES_SUCCESS'
export const USER_LIKES_FAILURE = 'USER_LIKES_FAILURE'

function fetchUserLikes (user_id) {
  return {
    [CALL_API]: {
      types: [USER_LIKES_REQUEST, USER_LIKES_SUCCESS, USER_LIKES_FAILURE],
      endpoint: make_url.users(user_id + '/likes/'),
      key: 'userLikes'
    }
  }
}

export function loadUserLikes (user_id) {
  console.log(user_id)
  return (dispatch, getState) => {
    console.log(dispatch, fetchUserLikes(user_id))
    return dispatch(fetchUserLikes(user_id))
  }
}
