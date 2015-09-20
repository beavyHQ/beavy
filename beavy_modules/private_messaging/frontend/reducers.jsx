
import { addNamedExtension } from 'config/extensions';
import { PMS_REQUEST, PMS_SUCCESS, PMS_FAILURE } from './actions';

import paginate from 'reducers/paginate';

export const PRIVATE_MESSAGES = "private_messages";

addNamedExtension("reducers", PRIVATE_MESSAGES, paginate({
  mapActionToKey: x => PRIVATE_MESSAGES,
  types: [ PMS_REQUEST, PMS_SUCCESS, PMS_FAILURE]
}));