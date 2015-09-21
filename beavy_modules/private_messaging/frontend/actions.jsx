
import { CALL_API } from 'middleware/api';
import { make_url } from 'utils';

export const PMS_REQUEST = 'PMS_REQUEST';
export const PMS_SUCCESS = 'PMS_SUCCESS';
export const PMS_FAILURE = 'PMS_FAILURE';

function fetchPMs(page=1) {
  return {
    [CALL_API]: {
      types: [PMS_REQUEST, PMS_SUCCESS, PMS_FAILURE],
      endpoint: make_url.account("private_messages/") + "?page=" + page,
      key: "private_messages"
    }
  };
}

export function loadPMs(page=1){
  return (dispatch, getState) => {
    return dispatch(fetchPMs(page=page));
  }
}