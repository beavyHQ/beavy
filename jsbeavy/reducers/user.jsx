
import { addNamedExtension } from 'config/extensions';

function userMapper(state = {}, action) {
  return state;
}

export const USER = 'user';

addNamedExtension("reducers", "user", userMapper)