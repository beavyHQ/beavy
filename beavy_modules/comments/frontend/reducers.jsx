
import { addNamedExtension } from 'config/extensions';
import { COMMENTS_REQUEST, COMMENTS_SUCCESS, COMMENTS_FAILURE } from './actions';

import paginate from 'reducers/paginate';

export const COMMENTS = "comments";

addNamedExtension("reducers", COMMENTS, paginate({
  mapActionToKey: x => COMMENTS,
  types: [ COMMENTS_REQUEST, COMMENTS_SUCCESS, COMMENTS_FAILURE]
}));