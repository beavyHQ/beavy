
import { addNamedExtension } from 'config/extensions';
import { USER_SUCCESS } from 'actions/user';

function userMapper(state = {}, action) {

  if (action.type == USER_SUCCESS)
    return action.response.entities.User[action.response.result];
  return state;
}

export const USER = 'user';

addNamedExtension("reducers", "user", userMapper);