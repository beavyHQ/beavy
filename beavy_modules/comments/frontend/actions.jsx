
import { CALL_API } from 'middleware/api'
import { make_url } from 'utils'

export const COMMENTS_REQUEST = 'COMMENTS_REQUEST'
export const COMMENTS_SUCCESS = 'COMMENTS_SUCCESS'
export const COMMENTS_FAILURE = 'COMMENTS_FAILURE'

function fetchComments (page = 1) {
  return {
    [CALL_API]: {
      types: [COMMENTS_REQUEST, COMMENTS_SUCCESS, COMMENTS_FAILURE],
      endpoint: make_url.account('comments/') + '?page=' + page,
      key: 'comments'
    }
  }
}

export function loadComments (page = 1) {
  return (dispatch, getState) => {
    return dispatch(fetchComments(page = page))
  }
}
