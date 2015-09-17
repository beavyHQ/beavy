
import { CALL_API } from 'middleware/api';
import { privateMessage } from './schemas';
import { make_url } from 'utils';

export const PMS_REQUEST = 'PMS_REQUEST';
export const PMS_SUCCESS = 'PMS_SUCCESS';
export const PMS_FAILURE = 'PMS_FAILURE';

function fetchPMs(user_id) {
  return {
    [CALL_API]: {
      types: [PMS_REQUEST, PMS_SUCCESS, PMS_FAILURE],
      endpoint: make_url.account("private_messages/"),
      schema: privateMessage
    }
  };
}

export function loadPMs(){
  return (dispatch, getState) => {
    return dispatch(fetchPMs());
  }
}