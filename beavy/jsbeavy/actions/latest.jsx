import { CALL_API } from 'middleware/api'
import { make_url } from 'utils'
import { LATEST } from 'reducers/latest'

export const LATEST_REQUEST = 'LATEST_REQUEST'
export const LATEST_SUCCESS = 'LATEST_SUCCESS'
export const LATEST_FAILURE = 'LATEST_FAILURE'

const fetchLatest = (page = 1) => {
  return {
    [CALL_API]: {
      types: [LATEST_REQUEST, LATEST_SUCCESS, LATEST_FAILURE],
      endpoint: '/latest?page=' + page,
      key: LATEST
    }
  }
}

export function loadLatest (page = 1) {
  return (dispatch, getState) => {
    return dispatch(fetchLatest(page = page))
  }
}

