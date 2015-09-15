
import { CALL_API } from 'middleware/api';
import { userSchema } from 'schemas';
import config from 'config/config';

export const USER_REQUEST = 'USER_REQUEST';
export const USER_SUCCESS = 'USER_SUCCESS';
export const USER_FAILURE = 'USER_FAILURE';

function fetchUser(user_id) {
  return {
    [CALL_API]: {
      types: [USER_REQUEST, USER_SUCCESS, USER_FAILURE],
      endpoint: config.USERS_URL + "/" + user_id + "/",
      schema: userSchema
    }
  };
}

export function loadUser(user_id){
  console.log(user_id);
  return (dispatch, getState) => {
    console.log(dispatch, fetchUser(user_id));
    return dispatch(fetchUser(user_id));
  }
}