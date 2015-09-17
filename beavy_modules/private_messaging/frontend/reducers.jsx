
import { addNamedExtension } from 'config/extensions';
import { PM_SUCCESS } from './actions';

function userLikesMapper(state = {}, action) {
  console.log(state, action);
  if (action.type == PM_SUCCESS)
    return action.response.entities.private_messages[action.response.result];
  return state;
}

export const PRIVATE_MESSAGES = 'private_messages';

addNamedExtension("reducers", PRIVATE_MESSAGES, userLikesMapper)