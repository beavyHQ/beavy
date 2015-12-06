
import { CALL_API } from 'middleware/api'
import { make_url } from 'utils'

export const USER_REQUEST = 'USER_REQUEST'
export const USER_SUCCESS = 'USER_SUCCESS'
export const USER_FAILURE = 'USER_FAILURE'

function fetchUser (user_id) {
  return {
    [CALL_API]: {
      types: [USER_REQUEST, USER_SUCCESS, USER_FAILURE],
      endpoint: make_url.users(user_id),
      schema: 'users'
    }
  }
}

export function loadUser (user_id) {
  return (dispatch, getState) => {
    return dispatch(fetchUser(user_id))
  }
}
