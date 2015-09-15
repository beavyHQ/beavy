
import { addNamedExtension } from 'config/extensions';
import { USER_LIKES_SUCCESS } from './actions';

function userLikesMapper(state = {}, action) {
  console.log(state, action);
  if (action.type == USER_LIKES_SUCCESS)
    return action.response.entities.UserLikes[action.response.result];
  return state;
}

export const USER_LIKES = 'user_likes';

addNamedExtension("reducers", USER_LIKES, userLikesMapper)